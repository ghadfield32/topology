// Package engine implements small, inspectable numerical algorithms.
// These are teaching implementations, not replacements for production solvers.
package engine

import (
	"fmt"
	"math"
	"sort"
)

func require(ok bool, message string) {
	if !ok {
		panic(message)
	}
}
func finite(v float64) bool { return !math.IsNaN(v) && !math.IsInf(v, 0) }
func clone(a [][]float64) [][]float64 {
	b := make([][]float64, len(a))
	for i := range a {
		b[i] = append([]float64(nil), a[i]...)
	}
	return b
}
func Zeros(n, m int) [][]float64 {
	a := make([][]float64, n)
	for i := range a {
		a[i] = make([]float64, m)
	}
	return a
}
func eye(n int) [][]float64 {
	a := Zeros(n, n)
	for i := range a {
		a[i][i] = 1
	}
	return a
}
func shape(a [][]float64) (int, int) {
	require(len(a) > 0 && len(a[0]) > 0, "empty matrix")
	m := len(a[0])
	for _, r := range a {
		require(len(r) == m, "ragged matrix")
		for _, v := range r {
			require(finite(v), "nonfinite matrix value")
		}
	}
	return len(a), m
}
func dot(a, b []float64) float64 {
	require(len(a) == len(b), "dot length mismatch")
	s := 0.
	for i, x := range a {
		s += x * b[i]
	}
	return s
}
func norm(a []float64) float64 { return math.Sqrt(dot(a, a)) }
func sub(a, b []float64) []float64 {
	require(len(a) == len(b), "vector length mismatch")
	c := make([]float64, len(a))
	for i := range a {
		c[i] = a[i] - b[i]
	}
	return c
}
func distance(a, b []float64) float64 { return norm(sub(a, b)) }
func Mean(xs []float64) float64 {
	require(len(xs) > 0, "empty mean")
	s := 0.
	for _, x := range xs {
		require(finite(x), "nonfinite mean input")
		s += x
	}
	return s / float64(len(xs))
}
func MeanRows(a [][]float64) []float64 {
	n, m := shape(a)
	v := make([]float64, m)
	for _, r := range a {
		for j, x := range r {
			v[j] += x / float64(n)
		}
	}
	return v
}
func Transpose(a [][]float64) [][]float64 {
	n, m := shape(a)
	b := Zeros(m, n)
	for i := range a {
		for j := range a[i] {
			b[j][i] = a[i][j]
		}
	}
	return b
}
func MatMul(a, b [][]float64) [][]float64 {
	n, k := shape(a)
	k2, m := shape(b)
	require(k == k2, "matrix product dimensions")
	c := Zeros(n, m)
	for i := 0; i < n; i++ {
		for h := 0; h < k; h++ {
			for j := 0; j < m; j++ {
				c[i][j] += a[i][h] * b[h][j]
			}
		}
	}
	return c
}
func MatVec(a [][]float64, b []float64) []float64 {
	_, m := shape(a)
	require(m == len(b), "matrix vector dimensions")
	v := make([]float64, len(a))
	for i := range a {
		v[i] = dot(a[i], b)
	}
	return v
}
func Rank(a [][]float64, tol float64) int {
	n, m := shape(a)
	require(tol > 0, "positive rank tolerance required")
	b := clone(a)
	r := 0
	for c := 0; c < m && r < n; c++ {
		p := r
		for i := r + 1; i < n; i++ {
			if math.Abs(b[i][c]) > math.Abs(b[p][c]) {
				p = i
			}
		}
		if math.Abs(b[p][c]) <= tol {
			continue
		}
		b[p], b[r] = b[r], b[p]
		pivot := b[r][c]
		for j := c; j < m; j++ {
			b[r][j] /= pivot
		}
		for i := 0; i < n; i++ {
			if i != r {
				f := b[i][c]
				for j := c; j < m; j++ {
					b[i][j] -= f * b[r][j]
				}
			}
		}
		r++
	}
	return r
}
func Rank2(a [][]float64) int {
	n, m := shape(a)
	b := make([][]uint8, n)
	for i := range a {
		b[i] = make([]uint8, m)
		for j, x := range a[i] {
			require(x == math.Trunc(x), "F2 requires integer entries")
			b[i][j] = uint8(int64(x) & 1)
		}
	}
	r := 0
	for c := 0; c < m && r < n; c++ {
		p := r
		for p < n && b[p][c] == 0 {
			p++
		}
		if p == n {
			continue
		}
		b[p], b[r] = b[r], b[p]
		for i := 0; i < n; i++ {
			if i != r && b[i][c] != 0 {
				for j := c; j < m; j++ {
					b[i][j] ^= b[r][j]
				}
			}
		}
		r++
	}
	return r
}
func Solve(a [][]float64, b []float64) []float64 {
	n, m := shape(a)
	require(n == m && len(b) == n, "square linear system required")
	z := clone(a)
	y := append([]float64(nil), b...)
	for c := 0; c < n; c++ {
		p := c
		for i := c + 1; i < n; i++ {
			if math.Abs(z[i][c]) > math.Abs(z[p][c]) {
				p = i
			}
		}
		require(math.Abs(z[p][c]) > 1e-13, "singular or ill-conditioned linear system")
		z[p], z[c] = z[c], z[p]
		y[p], y[c] = y[c], y[p]
		v := z[c][c]
		for j := c; j < n; j++ {
			z[c][j] /= v
		}
		y[c] /= v
		for i := 0; i < n; i++ {
			if i != c {
				f := z[i][c]
				for j := c; j < n; j++ {
					z[i][j] -= f * z[c][j]
				}
				y[i] -= f * y[c]
			}
		}
	}
	return y
}
func Cov(a [][]float64) [][]float64 {
	n, m := shape(a)
	require(n > 1, "sample covariance needs two rows")
	mu := MeanRows(a)
	c := Zeros(m, m)
	for _, r := range a {
		for i := 0; i < m; i++ {
			for j := 0; j < m; j++ {
				c[i][j] += (r[i] - mu[i]) * (r[j] - mu[j]) / float64(n-1)
			}
		}
	}
	return c
}

// EigenSym uses Jacobi rotations. Columns of v are eigenvectors, sorted descending.
func EigenSym(a [][]float64) ([]float64, [][]float64) {
	n, m := shape(a)
	require(n == m, "symmetric eigensystem needs square matrix")
	b := clone(a)
	v := eye(n)
	for i := range a {
		for j := range a {
			require(math.Abs(a[i][j]-a[j][i]) < 1e-8, "matrix is not symmetric")
		}
	}
	for it := 0; it < 100*n*n; it++ {
		p, q := 0, 0
		mx := 0.
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				if math.Abs(b[i][j]) > mx {
					mx = math.Abs(b[i][j])
					p = i
					q = j
				}
			}
		}
		if mx < 1e-12 {
			break
		}
		theta := .5 * math.Atan2(2*b[p][q], b[q][q]-b[p][p])
		c, s := math.Cos(theta), math.Sin(theta)
		app, aqq, apq := b[p][p], b[q][q], b[p][q]
		for k := 0; k < n; k++ {
			if k != p && k != q {
				x, y := b[k][p], b[k][q]
				b[k][p] = c*x - s*y
				b[p][k] = b[k][p]
				b[k][q] = s*x + c*y
				b[q][k] = b[k][q]
			}
			x, y := v[k][p], v[k][q]
			v[k][p] = c*x - s*y
			v[k][q] = s*x + c*y
		}
		b[p][p] = c*c*app - 2*s*c*apq + s*s*aqq
		b[q][q] = s*s*app + 2*s*c*apq + c*c*aqq
		b[p][q] = 0
		b[q][p] = 0
	}
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(i, j int) bool { return b[order[i]][order[i]] > b[order[j]][order[j]] })
	e := make([]float64, n)
	w := Zeros(n, n)
	for j, k := range order {
		e[j] = b[k][k]
		for i := 0; i < n; i++ {
			w[i][j] = v[i][k]
		}
	}
	return e, w
}

type Scaler struct{ Mean, Scale []float64 }

func FitScaler(a [][]float64) Scaler {
	n, m := shape(a)
	mu := MeanRows(a)
	s := make([]float64, m)
	for _, r := range a {
		for j, x := range r {
			s[j] += (x - mu[j]) * (x - mu[j]) / float64(n)
		}
	}
	for j := range s {
		s[j] = math.Sqrt(s[j])
		if s[j] < 1e-12 {
			s[j] = 1
		}
	}
	return Scaler{mu, s}
}
func (s Scaler) Transform(a [][]float64) [][]float64 {
	_, m := shape(a)
	require(m == len(s.Mean), "scaler columns")
	b := clone(a)
	for i := range b {
		for j := range b[i] {
			b[i][j] = (b[i][j] - s.Mean[j]) / s.Scale[j]
		}
	}
	return b
}

type RNG struct{ State uint32 }

func (r *RNG) Next() uint32 {
	if r.State == 0 {
		r.State = 1
	}
	x := r.State
	x ^= x << 13
	x ^= x >> 17
	x ^= x << 5
	r.State = x
	return x
}
func (r *RNG) Uniform() float64 { return (float64(r.Next()) + .5) / 4294967296. }
func (r *RNG) Normal() float64 {
	return math.Sqrt(-2*math.Log(r.Uniform())) * math.Cos(2*math.Pi*r.Uniform())
}
func shuffle(a []int, seed uint32) {
	r := RNG{seed}
	for i := len(a) - 1; i > 0; i-- {
		j := int(r.Next() % uint32(i+1))
		a[i], a[j] = a[j], a[i]
	}
}
func Rows(a [][]float64, idx []int) [][]float64 {
	b := make([][]float64, len(idx))
	for i, k := range idx {
		require(k >= 0 && k < len(a), "row out of range")
		b[i] = append([]float64(nil), a[k]...)
	}
	return b
}
func Values(a []float64, idx []int) []float64 {
	b := make([]float64, len(idx))
	for i, k := range idx {
		b[i] = a[k]
	}
	return b
}
func Labels(a []int, idx []int) []int {
	b := make([]int, len(idx))
	for i, k := range idx {
		b[i] = a[k]
	}
	return b
}
func Stratified(y []int, seed uint32) ([]int, []int, []int) {
	groups := map[int][]int{}
	keys := []int{}
	for i, k := range y {
		if _, ok := groups[k]; !ok {
			keys = append(keys, k)
		}
		groups[k] = append(groups[k], i)
	}
	sort.Ints(keys)
	tr, va, te := []int{}, []int{}, []int{}
	for h, k := range keys {
		a := groups[k]
		shuffle(a, seed+uint32(31*h))
		n1 := len(a) * 6 / 10
		n2 := len(a) * 8 / 10
		require(n1 > 0 && n2 > n1 && len(a) > n2, "class too small for 60/20/20 split")
		tr = append(tr, a[:n1]...)
		va = append(va, a[n1:n2]...)
		te = append(te, a[n2:]...)
	}
	sort.Ints(tr)
	sort.Ints(va)
	sort.Ints(te)
	return tr, va, te
}
func accuracy(y, p []int) float64 {
	require(len(y) == len(p) && len(y) > 0, "invalid accuracy input")
	n := 0
	for i := range y {
		if y[i] == p[i] {
			n++
		}
	}
	return float64(n) / float64(len(y))
}
func MAE(y, p []float64) float64 {
	require(len(y) == len(p) && len(y) > 0, "invalid MAE input")
	s := 0.
	for i := range y {
		s += math.Abs(y[i] - p[i])
	}
	return s / float64(len(y))
}
func RMSE(y, p []float64) float64 {
	require(len(y) == len(p) && len(y) > 0, "invalid RMSE input")
	s := 0.
	for i := range y {
		s += (y[i] - p[i]) * (y[i] - p[i])
	}
	return math.Sqrt(s / float64(len(y)))
}
func softmax(a []float64) []float64 {
	require(len(a) > 0, "empty softmax")
	mx := a[0]
	for _, x := range a {
		if x > mx {
			mx = x
		}
	}
	p := make([]float64, len(a))
	s := 0.
	for i, x := range a {
		p[i] = math.Exp(x - mx)
		s += p[i]
	}
	for i := range p {
		p[i] /= s
	}
	return p
}
func median(a []float64) float64 {
	require(len(a) > 0, "empty median")
	b := append([]float64(nil), a...)
	sort.Float64s(b)
	return (b[(len(b)-1)/2] + b[len(b)/2]) / 2
}
func describe(a []float64) map[string]any {
	require(len(a) > 0, "empty describe")
	b := append([]float64(nil), a...)
	sort.Float64s(b)
	return map[string]any{"n": len(a), "mean": Mean(a), "median": median(a), "min": b[0], "max": b[len(b)-1]}
}
func safeNumber(x float64) any {
	if math.IsNaN(x) {
		return "NaN"
	}
	if math.IsInf(x, 1) {
		return "+Inf"
	}
	if math.IsInf(x, -1) {
		return "-Inf"
	}
	return x
}
func vectorKey(a []float64) string { return fmt.Sprint(a) }
