package engine

import (
	"fmt"
	"math"
	"sort"
	"strings"
)

type Simplex struct {
	Vertices []int   `json:"vertices"`
	Value    float64 `json:"value"`
}
type Interval struct {
	Dim   int      `json:"dimension"`
	Birth float64  `json:"birth"`
	Death *float64 `json:"death"`
}

func simplexKey(v []int) string {
	s := make([]string, len(v))
	for i, x := range v {
		s[i] = fmt.Sprint(x)
	}
	return strings.Join(s, ",")
}
func lexLess(a, b []int) bool {
	for i := 0; i < len(a) && i < len(b); i++ {
		if a[i] != b[i] {
			return a[i] < b[i]
		}
	}
	return len(a) < len(b)
}
func Ordered(c []Simplex) []Simplex {
	d := make([]Simplex, len(c))
	copy(d, c)
	for i := range d {
		d[i].Vertices = append([]int(nil), d[i].Vertices...)
		sort.Ints(d[i].Vertices)
		require(len(d[i].Vertices) > 0 && finite(d[i].Value), "invalid simplex")
		for j := 1; j < len(d[i].Vertices); j++ {
			require(d[i].Vertices[j] != d[i].Vertices[j-1], "repeated simplex vertex")
		}
	}
	sort.SliceStable(d, func(i, j int) bool {
		a, b := d[i], d[j]
		if a.Value != b.Value {
			return a.Value < b.Value
		}
		if len(a.Vertices) != len(b.Vertices) {
			return len(a.Vertices) < len(b.Vertices)
		}
		return lexLess(a.Vertices, b.Vertices)
	})
	seen := map[string]int{}
	for i, s := range d {
		k := simplexKey(s.Vertices)
		_, ok := seen[k]
		require(!ok, "duplicate simplex")
		if len(s.Vertices) > 1 {
			for q := range s.Vertices {
				face := append([]int(nil), s.Vertices[:q]...)
				face = append(face, s.Vertices[q+1:]...)
				j, ok := seen[simplexKey(face)]
				require(ok && d[j].Value <= s.Value, "missing face or decreasing filtration")
			}
		}
		seen[k] = i
	}
	return d
}
func Rips(x [][]float64, epsilon float64, maxdim int) []Simplex {
	n, _ := shape(x)
	require(n <= 96 && maxdim >= 0 && maxdim <= 3 && epsilon >= 0, "Rips teaching bound: <=96 points, dimensions 0..3")
	d := Zeros(n, n)
	for i := 0; i < n; i++ {
		for j := 0; j < i; j++ {
			d[i][j] = distance(x[i], x[j])
			d[j][i] = d[i][j]
		}
	}
	c := []Simplex{}
	var rec func([]int, int, float64)
	rec = func(v []int, start int, birth float64) {
		if len(v) > 0 {
			c = append(c, Simplex{append([]int(nil), v...), birth})
			require(len(c) <= 200000, "Rips simplex budget exceeded")
		}
		if len(v) >= maxdim+1 {
			return
		}
		for j := start; j < n; j++ {
			b := birth
			ok := true
			for _, i := range v {
				if d[i][j] > epsilon {
					ok = false
					break
				}
				b = math.Max(b, d[i][j])
			}
			if ok {
				rec(append(v, j), j+1, b)
			}
		}
	}
	rec(nil, 0, 0)
	return Ordered(c)
}
func xorSorted(a, b []int) []int {
	r := []int{}
	i, j := 0, 0
	for i < len(a) || j < len(b) {
		if j == len(b) || (i < len(a) && a[i] < b[j]) {
			r = append(r, a[i])
			i++
		} else if i == len(a) || b[j] < a[i] {
			r = append(r, b[j])
			j++
		} else {
			i++
			j++
		}
	}
	return r
}
func Persistence(c []Simplex) []Interval {
	c = Ordered(c)
	idx := map[string]int{}
	for i, s := range c {
		idx[simplexKey(s.Vertices)] = i
	}
	reduced := make([][]int, len(c))
	pivots := map[int]int{}
	birth := map[int]bool{}
	out := []Interval{}
	for j, s := range c {
		col := []int{}
		if len(s.Vertices) > 1 {
			for q := range s.Vertices {
				face := append([]int(nil), s.Vertices[:q]...)
				face = append(face, s.Vertices[q+1:]...)
				col = append(col, idx[simplexKey(face)])
			}
			sort.Ints(col)
		}
		for len(col) > 0 {
			lo := col[len(col)-1]
			k, ok := pivots[lo]
			if !ok {
				break
			}
			col = xorSorted(col, reduced[k])
		}
		reduced[j] = col
		if len(col) == 0 {
			birth[j] = true
		} else {
			lo := col[len(col)-1]
			pivots[lo] = j
			delete(birth, lo)
			death := s.Value
			if death > c[lo].Value+1e-12 {
				out = append(out, Interval{len(c[lo].Vertices) - 1, c[lo].Value, &death})
			}
		}
	}
	for i := range birth {
		out = append(out, Interval{len(c[i].Vertices) - 1, c[i].Value, nil})
	}
	sort.Slice(out, func(i, j int) bool {
		a, b := out[i], out[j]
		if a.Dim != b.Dim {
			return a.Dim < b.Dim
		}
		if a.Birth != b.Birth {
			return a.Birth < b.Birth
		}
		if a.Death == nil {
			return false
		}
		if b.Death == nil {
			return true
		}
		return *a.Death < *b.Death
	})
	return out
}
func Betti(c []Simplex) []int {
	c = Ordered(c)
	dims := 0
	for _, s := range c {
		dims = max(dims, len(s.Vertices))
	}
	b := make([]int, dims)
	for _, v := range Persistence(c) {
		if v.Death == nil {
			b[v.Dim]++
		}
	}
	return b
}
func Triangle(filled bool) []Simplex {
	c := []Simplex{{[]int{0}, 0}, {[]int{1}, 0}, {[]int{2}, 0}, {[]int{0, 1}, 0}, {[]int{0, 2}, 0}, {[]int{1, 2}, 0}}
	if filled {
		c = append(c, Simplex{[]int{0, 1, 2}, 0})
	}
	return c
}
func Tetra(filled bool) []Simplex {
	c := []Simplex{}
	for mask := 1; mask < 16; mask++ {
		v := []int{}
		for j := 0; j < 4; j++ {
			if mask&(1<<j) != 0 {
				v = append(v, j)
			}
		}
		if len(v) < 4 || filled {
			c = append(c, Simplex{v, 0})
		}
	}
	return Ordered(c)
}
func MST(x [][]float64) []float64 {
	n, _ := shape(x)
	dist := make([]float64, n)
	used := make([]bool, n)
	for i := range dist {
		dist[i] = math.Inf(1)
	}
	dist[0] = 0
	edges := []float64{}
	for k := 0; k < n; k++ {
		v := -1
		for i := 0; i < n; i++ {
			if !used[i] && (v < 0 || dist[i] < dist[v]) {
				v = i
			}
		}
		used[v] = true
		if k > 0 {
			edges = append(edges, dist[v])
		}
		for j := 0; j < n; j++ {
			if !used[j] {
				dist[j] = math.Min(dist[j], distance(x[v], x[j]))
			}
		}
	}
	sort.Float64s(edges)
	return edges
}
func Components(x [][]float64, radius float64) [][]int {
	n, _ := shape(x)
	require(radius >= 0, "negative radius")
	seen := make([]bool, n)
	out := [][]int{}
	for start := 0; start < n; start++ {
		if seen[start] {
			continue
		}
		q := []int{start}
		seen[start] = true
		for h := 0; h < len(q); h++ {
			i := q[h]
			for j := 0; j < n; j++ {
				if !seen[j] && distance(x[i], x[j]) <= radius {
					seen[j] = true
					q = append(q, j)
				}
			}
		}
		sort.Ints(q)
		out = append(out, q)
	}
	return out
}

// PixelBetti models each foreground pixel as a closed unit square, including all faces.
func PixelBetti(pixels []float64, h, w int, threshold float64) []int {
	require(h*w == len(pixels), "pixel shape")
	v := map[int]bool{}
	edges := map[[2]int]bool{}
	faces := 0
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			if pixels[y*w+x] < threshold {
				continue
			}
			faces++
			a := y*(w+1) + x
			pts := []int{a, a + 1, a + w + 1, a + w + 2}
			for _, p := range pts {
				v[p] = true
			}
			for _, e := range [][2]int{{pts[0], pts[1]}, {pts[0], pts[2]}, {pts[1], pts[3]}, {pts[2], pts[3]}} {
				edges[e] = true
			}
		}
	}
	parent := map[int]int{}
	for p := range v {
		parent[p] = p
	}
	var find func(int) int
	find = func(x int) int {
		for parent[x] != x {
			parent[x] = parent[parent[x]]
			x = parent[x]
		}
		return x
	}
	for e := range edges {
		a, b := find(e[0]), find(e[1])
		parent[a] = b
	}
	roots := map[int]bool{}
	for p := range v {
		roots[find(p)] = true
	}
	b0 := len(roots)
	chi := len(v) - len(edges) + faces
	return []int{b0, b0 - chi}
}
func PixelFiltration(pixels []float64, h, w int) []Simplex {
	require(h*w == len(pixels), "pixel filtration shape")
	faces := map[string]Simplex{}
	add := func(v []int, val float64) {
		sort.Ints(v)
		k := simplexKey(v)
		old, ok := faces[k]
		if !ok || val < old.Value {
			faces[k] = Simplex{append([]int(nil), v...), val}
		}
	}
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			a := y*(w+1) + x
			val := -pixels[y*w+x]
			tris := [][]int{{a, a + 1, a + w + 2}, {a, a + w + 1, a + w + 2}}
			for _, t := range tris {
				for mask := 1; mask < 8; mask++ {
					v := []int{}
					for j := 0; j < 3; j++ {
						if mask&(1<<j) != 0 {
							v = append(v, t[j])
						}
					}
					add(v, val)
				}
			}
		}
	}
	c := []Simplex{}
	for _, s := range faces {
		c = append(c, s)
	}
	return Ordered(c)
}
func DiagramDimension(d []Interval, k int) []Interval {
	o := []Interval{}
	for _, x := range d {
		if x.Dim == k {
			o = append(o, x)
		}
	}
	return o
}
func Bottleneck(a, b []Interval) float64 {
	dim := -1
	for _, set := range [][]Interval{a, b} {
		for _, v := range set {
			require(finite(v.Birth) && (v.Death == nil || (finite(*v.Death) && *v.Death >= v.Birth)), "invalid persistence interval")
			if dim < 0 {
				dim = v.Dim
			}
			require(v.Dim == dim, "compare one homology dimension at a time")
		}
	}
	af, bf := []Interval{}, []Interval{}
	ae, be := []float64{}, []float64{}
	for _, v := range a {
		if v.Death == nil {
			ae = append(ae, v.Birth)
		} else {
			af = append(af, v)
		}
	}
	for _, v := range b {
		if v.Death == nil {
			be = append(be, v.Birth)
		} else {
			bf = append(bf, v)
		}
	}
	if len(ae) != len(be) {
		return math.Inf(1)
	}
	sort.Float64s(ae)
	sort.Float64s(be)
	essential := 0.
	for i := range ae {
		essential = math.Max(essential, math.Abs(ae[i]-be[i]))
	}
	n, m := len(af), len(bf)
	N := n + m
	if N == 0 {
		return essential
	}
	cost := Zeros(N, N)
	candidates := []float64{0}
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			d := 0.
			if i < n && j < m {
				d = math.Max(math.Abs(af[i].Birth-bf[j].Birth), math.Abs(*af[i].Death-*bf[j].Death))
			} else if i < n {
				d = (*af[i].Death - af[i].Birth) / 2
			} else if j < m {
				d = (*bf[j].Death - bf[j].Birth) / 2
			}
			cost[i][j] = d
			candidates = append(candidates, d)
		}
	}
	sort.Float64s(candidates)
	match := func(e float64) bool {
		p := make([]int, N)
		for i := range p {
			p[i] = -1
		}
		var visit func(int, []bool) bool
		visit = func(i int, seen []bool) bool {
			for j := 0; j < N; j++ {
				if !seen[j] && cost[i][j] <= e+1e-12 {
					seen[j] = true
					if p[j] < 0 || visit(p[j], seen) {
						p[j] = i
						return true
					}
				}
			}
			return false
		}
		for i := 0; i < N; i++ {
			if !visit(i, make([]bool, N)) {
				return false
			}
		}
		return true
	}
	lo, hi := 0, len(candidates)-1
	for lo < hi {
		mid := (lo + hi) / 2
		if match(candidates[mid]) {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return math.Max(essential, candidates[lo])
}
func TopoFeature(query []float64, refs [][]float64) []float64 {
	require(len(refs) >= 4, "need reference points")
	order := make([]int, len(refs))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(i, j int) bool { return distance(query, refs[order[i]]) < distance(query, refs[order[j]]) })
	k := min(7, len(refs))
	cloud := [][]float64{query}
	dists := []float64{}
	for _, i := range order[:k] {
		cloud = append(cloud, refs[i])
		dists = append(dists, distance(query, refs[i]))
	}
	h0 := MST(cloud)
	ints := Persistence(Rips(cloud, math.Inf(1), 2))
	life := []float64{}
	for _, v := range ints {
		if v.Dim == 1 && v.Death != nil {
			life = append(life, *v.Death-v.Birth)
		}
	}
	m1, total := 0., 0.
	for _, x := range life {
		m1 = math.Max(m1, x)
		total += x
	}
	return []float64{Mean(dists), dists[0], dists[len(dists)-1], Mean(h0), h0[len(h0)-1], m1, total}
}
func Mapper(x [][]float64, lens []float64, bins int, overlap, radius float64) map[string]any {
	n, _ := shape(x)
	require(len(lens) == n && bins >= 2 && overlap >= 0 && overlap < 1, "mapper inputs")
	mn, mx := lens[0], lens[0]
	for _, v := range lens {
		mn = math.Min(mn, v)
		mx = math.Max(mx, v)
	}
	width := (mx - mn) / (float64(bins) - float64(bins-1)*overlap)
	require(width > 0, "constant mapper lens")
	step := width * (1 - overlap)
	nodes := [][]int{}
	for b := 0; b < bins; b++ {
		lo := mn + float64(b)*step
		hi := lo + width
		idx := []int{}
		for i, v := range lens {
			if v >= lo-1e-12 && v <= hi+1e-12 {
				idx = append(idx, i)
			}
		}
		if len(idx) == 0 {
			continue
		}
		for _, cl := range Components(Rows(x, idx), radius) {
			node := []int{}
			for _, j := range cl {
				node = append(node, idx[j])
			}
			nodes = append(nodes, node)
		}
	}
	edges := [][2]int{}
	for i := range nodes {
		set := map[int]bool{}
		for _, k := range nodes[i] {
			set[k] = true
		}
		for j := 0; j < i; j++ {
			for _, k := range nodes[j] {
				if set[k] {
					edges = append(edges, [2]int{j, i})
					break
				}
			}
		}
	}
	return map[string]any{"nodes": nodes, "edges": edges, "cover_bins": bins, "overlap_fraction": overlap, "cluster_radius": radius}
}

// ReportH01 omits unvalidated top-dimensional classes of a 2-skeleton.
func ReportH01(d []Interval) []Interval {
	r := []Interval{}
	for _, v := range d {
		if v.Dim <= 1 {
			r = append(r, v)
		}
	}
	return r
}
