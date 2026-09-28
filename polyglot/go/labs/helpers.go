package labs

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func mean(xs []float64) float64 {
	var s float64
	for _, x := range xs {
		s += x
	}
	if len(xs) == 0 {
		return math.NaN()
	}
	return s / float64(len(xs))
}
func l2(a, b []float64) float64 {
	var s float64
	for i := range a {
		d := a[i] - b[i]
		s += d * d
	}
	return math.Sqrt(s)
}
func dot(a, b []float64) float64 {
	var s float64
	for i := range a {
		s += a[i] * b[i]
	}
	return s
}
func matVec(a [][]float64, x []float64) []float64 {
	y := make([]float64, len(a))
	for i := range a {
		y[i] = dot(a[i], x)
	}
	return y
}
func rankMod2(a [][]int) int {
	if len(a) == 0 {
		return 0
	}
	m := make([][]int, len(a))
	for i := range a {
		m[i] = append([]int(nil), a[i]...)
	}
	r := 0
	cols := len(m[0])
	for c := 0; c < cols && r < len(m); c++ {
		p := -1
		for i := r; i < len(m); i++ {
			if m[i][c]&1 == 1 {
				p = i
				break
			}
		}
		if p < 0 {
			continue
		}
		m[r], m[p] = m[p], m[r]
		for i := 0; i < len(m); i++ {
			if i != r && m[i][c]&1 == 1 {
				for j := c; j < cols; j++ {
					m[i][j] = (m[i][j] ^ m[r][j]) & 1
				}
			}
		}
		r++
	}
	return r
}
func det3(a [3][3]float64) float64 {
	return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0]) + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
}
func rotateZ(p [3]float64, theta float64) [3]float64 {
	c, s := math.Cos(theta), math.Sin(theta)
	return [3]float64{c*p[0] - s*p[1], s*p[0] + c*p[1], p[2]}
}
func csvRows(path string) ([][]string, error) {
	f, e := os.Open(path)
	if e != nil {
		return nil, e
	}
	defer f.Close()
	r := csv.NewReader(f)
	return r.ReadAll()
}
func numericCSV(path string) ([][]float64, error) {
	rows, e := csvRows(path)
	if e != nil {
		return nil, e
	}
	out := [][]float64{}
	for i, row := range rows {
		if i == 0 {
			continue
		}
		vals := []float64{}
		for _, s := range row {
			v, er := strconv.ParseFloat(strings.TrimSpace(s), 64)
			if er == nil {
				vals = append(vals, v)
			}
		}
		if len(vals) > 0 {
			out = append(out, vals)
		}
	}
	return out, nil
}
func weightedMean(chunks [][][]float64) []float64 {
	if len(chunks) == 0 {
		return nil
	}
	d := len(chunks[0][0])
	sum := make([]float64, d)
	n := 0
	for _, ch := range chunks {
		for _, p := range ch {
			for j := 0; j < d; j++ {
				sum[j] += p[j]
			}
			n++
		}
	}
	for j := range sum {
		sum[j] /= float64(n)
	}
	return sum
}
func equalMeanOfChunkMeans(chunks [][][]float64) []float64 {
	d := len(chunks[0][0])
	out := make([]float64, d)
	for _, ch := range chunks {
		m := weightedMean([][][]float64{ch})
		for j := range out {
			out[j] += m[j]
		}
	}
	for j := range out {
		out[j] /= float64(len(chunks))
	}
	return out
}
func repoPath(repo string, parts ...string) string {
	all := append([]string{repo}, parts...)
	return filepath.Join(all...)
}
func loadSPLBall(repo string) ([][]float64, error) {
	b, e := os.ReadFile(repoPath(repo, "sports_v8", "data", "spl_selected_frames.json"))
	if e != nil {
		return nil, e
	}
	var raw map[string]any
	if e = json.Unmarshal(b, &raw); e != nil {
		return nil, e
	}
	records, ok := raw["records"].([]any)
	if !ok {
		return nil, errors.New("unexpected SPL JSON: missing records")
	}
	pts := [][]float64{}
	for _, it := range records {
		m, _ := it.(map[string]any)
		ball, _ := m["ball"].([]any)
		if len(ball) != 3 {
			continue
		}
		x, xok := ball[0].(float64)
		y, yok := ball[1].(float64)
		z, zok := ball[2].(float64)
		if xok && yok && zok {
			pts = append(pts, []float64{x * 0.3048, y * 0.3048, z * 0.3048})
		}
	}
	if len(pts) == 0 {
		return nil, errors.New("no ball points")
	}
	return pts, nil
}
func readJSONLines(path string) ([]map[string]any, error) {
	f, e := os.Open(path)
	if e != nil {
		return nil, e
	}
	defer f.Close()
	s := bufio.NewScanner(f)
	out := []map[string]any{}
	for s.Scan() {
		var m map[string]any
		if json.Unmarshal(s.Bytes(), &m) == nil {
			out = append(out, m)
		}
	}
	return out, s.Err()
}
func genericCase(repo, id, title, path string) (Result, error) {
	rows, e := csvRows(repoPath(repo, strings.Split(path, "/")...))
	if e != nil {
		return Result{}, e
	}
	return Result{Lab: id, Title: title, Metrics: map[string]any{"rows_including_header": len(rows), "data_rows": max(0, len(rows)-1), "columns": func() int {
		if len(rows) > 0 {
			return len(rows[0])
		}
		return 0
	}()}, Notes: []string{"Schema/count check only; use the Python reference for the complete statistical protocol."}}, nil
}
func genericStage(id, title string) (Result, error) {
	return Result{Lab: id, Title: title, Metrics: map[string]any{"implemented": true}, Notes: []string{"Dependency-light companion; see the lab README for the Python parity boundary."}}, nil
}
func ensureFinite(x float64) error {
	if math.IsNaN(x) || math.IsInf(x, 0) {
		return fmt.Errorf("non-finite result")
	}
	return nil
}
