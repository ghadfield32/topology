package engine

import (
	"archive/zip"
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/csv"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"io"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"unicode/utf8"
)

const maxDataBytes = 256 * 1024 * 1024

func SHA(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func pathIn(repo, path string) string {
	require(path != "" && !filepath.IsAbs(path), "relative data path required")
	root, e := filepath.Abs(repo)
	require(e == nil, "invalid repo root")
	p := filepath.Join(root, filepath.FromSlash(path))
	rel, e := filepath.Rel(root, p)
	require(e == nil && rel != ".." && !strings.HasPrefix(rel, ".."+string(filepath.Separator)), "path escapes repository")
	resolved, e := filepath.EvalSymlinks(p)
	require(e == nil, "missing input: "+path)
	rr, e := filepath.Rel(root, resolved)
	require(e == nil && rr != ".." && !strings.HasPrefix(rr, ".."+string(filepath.Separator)), "symlink escapes repository")
	return resolved
}
func ReadBytes(repo, path string) []byte {
	p := pathIn(repo, path)
	st, e := os.Stat(p)
	require(e == nil && st.Mode().IsRegular() && st.Size() <= maxDataBytes, "input is not a bounded regular file")
	b, e := os.ReadFile(p)
	require(e == nil, "cannot read "+path)
	recordInput(path, b)
	return b
}
func ReadJSON(repo, path string) any {
	b := ReadBytes(repo, path)
	var j any
	d := json.NewDecoder(bytes.NewReader(b))
	d.UseNumber()
	e := d.Decode(&j)
	require(e == nil, "invalid JSON: "+path)
	var trailing any
	require(d.Decode(&trailing) == io.EOF, "trailing JSON values")
	return j
}
func num(a any) float64 {
	switch v := a.(type) {
	case float64:
		return v
	case int:
		return float64(v)
	case json.Number:
		x, e := v.Float64()
		require(e == nil, "not numeric")
		return x
	case string:
		x, e := strconv.ParseFloat(v, 64)
		require(e == nil, "not numeric")
		return x
	}
	panic("not a JSON number")
}
func obj(a any) map[string]any { v, ok := a.(map[string]any); require(ok, "object required"); return v }
func arr(a any) []any          { v, ok := a.([]any); require(ok, "array required"); return v }
func fvec(a any) []float64 {
	v := arr(a)
	o := make([]float64, len(v))
	for i, x := range v {
		o[i] = num(x)
	}
	return o
}
func ReadCSV(repo, path string, sep rune) [][]string {
	b := ReadBytes(repo, path)
	require(utf8.Valid(b), "CSV must be UTF-8")
	r := csv.NewReader(strings.NewReader(strings.TrimPrefix(string(b), "\ufeff")))
	r.Comma = sep
	r.FieldsPerRecord = -1
	v, e := r.ReadAll()
	require(e == nil, "invalid CSV: "+path)
	return v
}
func column(header []string, name string) int {
	for i, h := range header {
		if h == name {
			return i
		}
	}
	panic("missing column: " + name)
}
func numeric(rows [][]string, names []string) ([][]float64, []int) {
	require(len(rows) > 1, "empty table")
	cols := make([]int, len(names))
	for i, n := range names {
		cols[i] = column(rows[0], n)
	}
	out := [][]float64{}
	kept := []int{}
	for i, row := range rows[1:] {
		require(len(row) == len(rows[0]), "ragged semantic table")
		v := make([]float64, len(cols))
		valid := true
		for j, k := range cols {
			s := strings.TrimSpace(row[k])
			if s == "" || strings.EqualFold(s, "NA") || strings.EqualFold(s, "NaN") {
				valid = false
				continue
			}
			x, e := strconv.ParseFloat(s, 64)
			require(e == nil, "invalid numeric value in "+names[j])
			require(finite(x), "infinite selected numeric value")
			v[j] = x
		}
		if valid {
			out = append(out, v)
			kept = append(kept, i)
		}
	}
	return out, kept
}

type Array struct {
	Shape   []int
	DType   string
	Data    []float64
	Text    []string
	Fortran bool
	RawSHA  string
}

func (a Array) Audit() map[string]any {
	out := map[string]any{"shape": a.Shape, "dtype": a.DType, "fortran_order": a.Fortran, "payload_sha256": a.RawSHA}
	if a.Text != nil {
		out["values"] = a.Text
	} else {
		v := make([]any, len(a.Data))
		for i, x := range a.Data {
			if len(a.DType) > 1 && (a.DType[1] == 'b' || a.DType[1] == '?') {
				v[i] = x != 0
			} else {
				v[i] = safeNumber(x)
			}
		}
		out["values"] = v
	}
	return out
}

var descrRe = regexp.MustCompile(`['"]descr['"]\s*:\s*['"]([^'"]+)['"]`)
var shapeRe = regexp.MustCompile(`['"]shape['"]\s*:\s*\(([^)]*)\)`)
var orderRe = regexp.MustCompile(`['"]fortran_order['"]\s*:\s*(True|False)`)

func ReadNPY(b []byte) Array {
	require(len(b) >= 10 && string(b[:6]) == "\x93NUMPY", "invalid NPY magic")
	major := b[6]
	offset, hl := 0, 0
	if major == 1 {
		hl = int(binary.LittleEndian.Uint16(b[8:10]))
		offset = 10
	} else if major == 2 || major == 3 {
		require(len(b) >= 12, "truncated NPY header")
		hl = int(binary.LittleEndian.Uint32(b[8:12]))
		offset = 12
	} else {
		panic("unsupported NPY version")
	}
	require(hl > 0 && hl <= 1<<20 && offset+hl <= len(b), "invalid NPY header size")
	header := string(b[offset : offset+hl])
	d := descrRe.FindStringSubmatch(header)
	s := shapeRe.FindStringSubmatch(header)
	f := orderRe.FindStringSubmatch(header)
	require(len(d) == 2 && len(s) == 2 && len(f) == 2, "NPY structured/object dtype or malformed header not supported")
	dtype := d[1]
	require(len(dtype) >= 3, "invalid NPY dtype")
	item, e := strconv.Atoi(dtype[2:])
	require(e == nil && item > 0, "invalid NPY item size")
	shape := []int{}
	total := 1
	for _, part := range strings.Split(s[1], ",") {
		part = strings.TrimSpace(part)
		if part == "" {
			continue
		}
		n, e := strconv.Atoi(part)
		require(e == nil && n >= 0, "invalid array dimension")
		shape = append(shape, n)
		require(n == 0 || total <= maxDataBytes/n, "array dimension overflow")
		total *= n
	}
	kind := dtype[1]
	width := item
	if kind == 'U' {
		width *= 4
	}
	require(width > 0 && total <= maxDataBytes/width, "array too large")
	raw := b[offset+hl:]
	require(len(raw) == total*width, "NPY payload length mismatch")
	a := Array{Shape: shape, DType: dtype, Fortran: f[1] == "True", RawSHA: SHA(raw)}
	var order binary.ByteOrder = binary.LittleEndian
	if dtype[0] == '>' {
		order = binary.BigEndian
	}
	if kind == 'U' || kind == 'S' {
		a.Text = make([]string, total)
	} else {
		a.Data = make([]float64, total)
	}
	for i := 0; i < total; i++ {
		q := raw[i*width : (i+1)*width]
		switch kind {
		case 'f':
			if item == 4 {
				a.Data[i] = float64(math.Float32frombits(order.Uint32(q)))
			} else if item == 8 {
				a.Data[i] = math.Float64frombits(order.Uint64(q))
			} else {
				panic("unsupported float width")
			}
		case 'i':
			switch item {
			case 1:
				a.Data[i] = float64(int8(q[0]))
			case 2:
				a.Data[i] = float64(int16(order.Uint16(q)))
			case 4:
				a.Data[i] = float64(int32(order.Uint32(q)))
			case 8:
				v := int64(order.Uint64(q))
				require(v >= -(1<<53) && v <= 1<<53, "integer exceeds exact JSON numeric range")
				a.Data[i] = float64(v)
			default:
				panic("unsupported signed width")
			}
		case 'u':
			switch item {
			case 1:
				a.Data[i] = float64(q[0])
			case 2:
				a.Data[i] = float64(order.Uint16(q))
			case 4:
				a.Data[i] = float64(order.Uint32(q))
			case 8:
				v := order.Uint64(q)
				require(v <= 1<<53, "integer exceeds exact JSON numeric range")
				a.Data[i] = float64(v)
			default:
				panic("unsupported unsigned width")
			}
		case 'b':
			require(item == 1 && q[0] <= 1, "invalid boolean")
			a.Data[i] = float64(q[0])
		case 'U':
			r := []rune{}
			for j := 0; j < item; j++ {
				v := order.Uint32(q[j*4 : j*4+4])
				require(v <= utf8.MaxRune && !(v >= 0xd800 && v <= 0xdfff), "invalid Unicode scalar")
				r = append(r, rune(v))
			}
			a.Text[i] = strings.TrimRight(string(r), "\x00")
		case 'S':
			a.Text[i] = strings.TrimRight(string(q), "\x00")
		default:
			panic("unsupported NPY dtype " + dtype)
		}
	}
	if a.Fortran && len(shape) > 1 {
		nd := append([]float64(nil), a.Data...)
		nt := append([]string(nil), a.Text...)
		for i := 0; i < total; i++ {
			rem := i
			coords := make([]int, len(shape))
			for j := len(shape) - 1; j >= 0; j-- {
				coords[j] = rem % shape[j]
				rem /= shape[j]
			}
			src, stride := 0, 1
			for j, n := range shape {
				src += coords[j] * stride
				stride *= n
			}
			if a.Data != nil {
				a.Data[i] = nd[src]
			} else {
				a.Text[i] = nt[src]
			}
		}
	}
	return a
}
func ReadNPZ(repo, path string) map[string]Array {
	b := ReadBytes(repo, path)
	zr, e := zip.NewReader(bytes.NewReader(b), int64(len(b)))
	require(e == nil, "invalid NPZ zip")
	out := map[string]Array{}
	sum := uint64(0)
	for _, f := range zr.File {
		require(strings.HasSuffix(f.Name, ".npy") && !strings.Contains(f.Name, "/") && !strings.Contains(f.Name, "\\"), "unexpected NPZ member")
		sum += f.UncompressedSize64
		require(f.UncompressedSize64 <= maxDataBytes && sum <= maxDataBytes, "NPZ decoded size limit")
		key := strings.TrimSuffix(f.Name, ".npy")
		_, exists := out[key]
		require(!exists, "duplicate NPZ key")
		r, e := f.Open()
		require(e == nil, "NPZ member open failed")
		data, e := io.ReadAll(io.LimitReader(r, maxDataBytes+1))
		r.Close()
		require(e == nil && len(data) <= maxDataBytes, "NPZ member read or CRC failed")
		out[key] = ReadNPY(data)
	}
	return out
}
func ReadPNG(repo, path string) Array {
	b := ReadBytes(repo, path)
	require(len(b) >= 33, "truncated PNG")
	cfg, e := png.DecodeConfig(bytes.NewReader(b))
	require(e == nil && cfg.Width > 0 && cfg.Height > 0 && cfg.Width*cfg.Height <= maxDataBytes/8, "invalid/large PNG")
	im, e := png.Decode(bytes.NewReader(b))
	require(e == nil, "PNG decode failed")
	typ, depth := b[25], b[24]
	channels := 4
	switch typ {
	case 0:
		channels = 1
	case 2:
		channels = 3
	case 4:
		channels = 2
	case 6:
		channels = 4
	case 3:
		channels = 4
	default:
		panic("unsupported PNG color")
	}
	for pos := 8; pos+12 <= len(b); {
		length := int(binary.BigEndian.Uint32(b[pos : pos+4]))
		require(length <= len(b)-pos-12, "PNG chunk bounds")
		if string(b[pos+4:pos+8]) == "tRNS" {
			if typ == 0 {
				channels = 2
			}
			if typ == 2 {
				channels = 4
			}
		}
		pos += length + 12
	}
	dtype := "|u1"
	if depth == 16 {
		dtype = "<u2"
	}
	a := Array{Shape: []int{cfg.Height, cfg.Width, channels}, DType: dtype, Data: make([]float64, 0, cfg.Height*cfg.Width*channels), RawSHA: SHA(b)}
	for y := 0; y < cfg.Height; y++ {
		for x := 0; x < cfg.Width; x++ {
			// Preserve unassociated color values. RGBA() premultiplies by alpha and can lose a unit.
			var c color.NRGBA64
			switch v := im.At(x, y).(type) {
			case color.NRGBA:
				c = color.NRGBA64{uint16(v.R) * 257, uint16(v.G) * 257, uint16(v.B) * 257, uint16(v.A) * 257}
			case color.NRGBA64:
				c = v
			default:
				c = color.NRGBA64Model.Convert(v).(color.NRGBA64)
			}
			v := []uint16{c.R, c.G, c.B, c.A}
			if channels == 1 {
				v = []uint16{c.R}
			}
			if channels == 2 {
				v = []uint16{c.R, c.A}
			}
			for j := 0; j < channels; j++ {
				z := float64(v[j])
				if depth != 16 {
					z = math.Floor(z / 257)
				}
				a.Data = append(a.Data, z)
			}
		}
	}
	return a
}
func ReadPFM(repo, path string) Array {
	b := ReadBytes(repo, path)
	parts := bytes.SplitN(b, []byte("\n"), 4)
	require(len(parts) == 4, "invalid PFM header")
	kind := strings.TrimSpace(string(parts[0]))
	c := 1
	if kind == "PF" {
		c = 3
	} else {
		require(kind == "Pf", "invalid PFM magic")
	}
	var w, h int
	_, e := fmt.Sscanf(string(parts[1]), "%d %d", &w, &h)
	require(e == nil && w > 0 && h > 0, "invalid PFM dimensions")
	scale, e := strconv.ParseFloat(strings.TrimSpace(string(parts[2])), 64)
	require(e == nil && scale != 0, "invalid PFM scale")
	raw := parts[3]
	require(w*h*c <= maxDataBytes/4 && len(raw) == w*h*c*4, "PFM data length")
	var bo binary.ByteOrder = binary.BigEndian
	if scale < 0 {
		bo = binary.LittleEndian
	}
	a := Array{Shape: []int{h, w, c}, DType: "<f4", Data: make([]float64, h*w*c), RawSHA: SHA(raw)}
	for y := 0; y < h; y++ {
		for x := 0; x < w*c; x++ {
			k := ((h-1-y)*w*c + x) * 4
			a.Data[y*w*c+x] = float64(math.Float32frombits(bo.Uint32(raw[k:k+4]))) * math.Abs(scale)
		}
	}
	return a
}
func Decode(repo, path string) map[string]any {
	b := ReadBytes(repo, path)
	out := map[string]any{"path": path, "bytes": len(b), "sha256": SHA(b)}
	switch strings.ToLower(filepath.Ext(path)) {
	case ".json":
		out["kind"] = "json"
		out["value"] = ReadJSON(repo, path)
	case ".csv":
		sep := ','
		if strings.Contains(strings.SplitN(string(b), "\n", 2)[0], ";") {
			sep = ';'
		}
		out["kind"] = "table"
		out["rows"] = ReadCSV(repo, path, sep)
	case ".npy":
		out["kind"] = "array"
		out["array"] = ReadNPY(b).Audit()
	case ".npz":
		out["kind"] = "arrays"
		a := ReadNPZ(repo, path)
		vals := map[string]any{}
		for k, v := range a {
			vals[k] = v.Audit()
		}
		out["arrays"] = vals
	case ".png":
		out["kind"] = "array"
		out["array"] = ReadPNG(repo, path).Audit()
	case ".pfm":
		out["kind"] = "array"
		out["array"] = ReadPFM(repo, path).Audit()
	default:
		require(utf8.Valid(b), "unknown binary format")
		out["kind"] = "text"
		out["text"] = string(b)
	}
	return out
}
func sortedKeys[V any](m map[string]V) []string {
	k := make([]string, 0, len(m))
	for x := range m {
		k = append(k, x)
	}
	sort.Strings(k)
	return k
}

var _ image.Image
