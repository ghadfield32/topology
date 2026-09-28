package engine

import (
	"math"
	"reflect"
	"testing"
)

func closeTo(t *testing.T, a, b float64) {
	t.Helper()
	if !finite(a) || math.Abs(a-b) > 1e-9 {
		t.Fatalf("%.17g != %.17g", a, b)
	}
}
func rejects(t *testing.T, f func()) {
	t.Helper()
	defer func() {
		if recover() == nil {
			t.Fatal("invalid input accepted")
		}
	}()
	f()
}
func TestMatrixContracts(t *testing.T) {
	for name, f := range map[string]func(){"ragged": func() { shape([][]float64{{1}, {1, 2}}) }, "nonfinite": func() { shape([][]float64{{math.NaN()}}) }, "product": func() { MatMul([][]float64{{1, 2}}, [][]float64{{1}}) }, "singular": func() { Solve([][]float64{{1, 2}, {2, 4}}, []float64{1, 2}) }, "f2_noninteger": func() { Rank2([][]float64{{.5}}) }} {
		t.Run(name, func(t *testing.T) { rejects(t, f) })
	}
}
func TestRankPreservesInput(t *testing.T) {
	a := [][]float64{{1, 2}, {2, 4}}
	b := clone(a)
	if Rank(a, 1e-12) != 1 || !reflect.DeepEqual(a, b) {
		t.Fatal(a)
	}
}
func TestBoundarySquared(t *testing.T) {
	a := MatMul(BoundaryMatrix(Triangle(true), 1), BoundaryMatrix(Triangle(true), 2))
	for _, r := range a {
		for _, v := range r {
			if int(v)%2 != 0 {
				t.Fatal(a)
			}
		}
	}
}
func TestKnownBetti(t *testing.T) {
	for _, c := range []struct {
		c    []Simplex
		want []int
	}{{Triangle(false), []int{1, 1}}, {Triangle(true), []int{1, 0, 0}}, {Tetra(false), []int{1, 0, 1}}, {Tetra(true), []int{1, 0, 0, 0}}} {
		if !reflect.DeepEqual(Betti(c.c), c.want) {
			t.Fatal(Betti(c.c), c.want)
		}
	}
}
func TestInvalidComplexes(t *testing.T) {
	for n, c := range map[string][]Simplex{"missing_face": {{[]int{0, 1}, 0}}, "repeated_vertex": {{[]int{0, 0}, 0}}, "duplicate": {{[]int{0}, 0}, {[]int{0}, 0}}, "backwards": {{[]int{0}, 1}, {[]int{1}, 0}, {[]int{0, 1}, 0}}} {
		t.Run(n, func(t *testing.T) { rejects(t, func() { Ordered(c) }) })
	}
}
func TestSquareInvariances(t *testing.T) {
	x := [][]float64{{0, 0}, {1, 0}, {1, 1}, {0, 1}}
	a := Persistence(Rips(x, 2, 2))
	y := [][]float64{{4, 6}, {4, 5}, {5, 5}, {5, 6}}
	b := Persistence(Rips(y, 2, 2))
	if !reflect.DeepEqual(a, b) {
		t.Fatal(a, b)
	}
	c := Persistence(Rips(x, 1, 2))
	h := DiagramDimension(c, 1)
	if len(h) != 1 || h[0].Death != nil {
		t.Fatal("truncation did not retain essential-at-cutoff", c)
	}
}
func TestMSTMatchesH0(t *testing.T) {
	x := [][]float64{{0, 0}, {.7, 0}, {2, 1}, {3, 2}}
	d := DiagramDimension(Persistence(Rips(x, math.Inf(1), 1)), 0)
	want := MST(x)
	got := []float64{}
	for _, v := range d {
		if v.Death != nil {
			got = append(got, *v.Death)
		}
	}
	if !reflect.DeepEqual(got, want) {
		t.Fatal(got, want)
	}
}
func TestBottleneckDiagonal(t *testing.T) {
	death := 4.
	d := []Interval{{1, 0, &death}}
	closeTo(t, Bottleneck(d, nil), 2)
	closeTo(t, Bottleneck(d, d), 0)
}
func TestBottleneckEssential(t *testing.T) {
	if !math.IsInf(Bottleneck([]Interval{{0, 0, nil}}, nil), 1) {
		t.Fatal("essential count mismatch must be infinite")
	}
}
func TestClosedPixels(t *testing.T) {
	p := []float64{1, 0, 0, 1}
	if !reflect.DeepEqual(PixelBetti(p, 2, 2, .5), []int{1, 0}) {
		t.Fatal("closed diagonal squares meet at vertex")
	}
	q := []float64{1, 1, 1, 1, 0, 1, 1, 1, 1}
	if !reflect.DeepEqual(PixelBetti(q, 3, 3, .5), []int{1, 1}) {
		t.Fatal("ring")
	}
}
func TestScalerTrainingOnly(t *testing.T) {
	s := FitScaler([][]float64{{0, 2}, {2, 2}})
	v := s.Transform([][]float64{{100, 2}})
	closeTo(t, v[0][0], 99)
	closeTo(t, v[0][1], 0)
}
func TestEigenResidual(t *testing.T) {
	a := [][]float64{{3, 1}, {1, 3}}
	v, q := EigenSym(a)
	for k := range v {
		for i := range a {
			z := 0.
			for j := range a {
				z += a[i][j] * q[j][k]
			}
			closeTo(t, z, v[k]*q[i][k])
		}
	}
}
func TestCovariance(t *testing.T) {
	v := Cov([][]float64{{1, 2}, {2, 4}, {3, 6}})
	closeTo(t, v[0][0], 1)
	closeTo(t, v[0][1], 2)
	closeTo(t, v[1][1], 4)
}
func TestADCompositeFiniteDifference(t *testing.T) {
	for _, x := range []float64{-.7, .1, .9} {
		tape := NewTape()
		v := tape.Input(x)
		r := tape.Add(tape.Sin(v), tape.Log(tape.Exp(tape.Mul(v, v))))
		g := tape.Back(r)
		closeTo(t, g[v], math.Cos(x)+2*x)
	}
}
func TestJetSecondDerivativeAndParameter(t *testing.T) {
	tape := NewTape()
	w := tape.Input(.4)
	x := jvar(tape, .7, true)
	z := jtanh(tape, jmul(tape, Jet{w, tape.Input(0), tape.Input(0)}, x))
	u := math.Tanh(.28)
	closeTo(t, tape.Val(z.D), .4*(1-u*u))
	closeTo(t, tape.Val(z.D2), -2*.4*.4*u*(1-u*u))
	g := tape.Back(z.D2)
	f := func(w float64) float64 { u := math.Tanh(w * .7); return -2 * w * w * u * (1 - u*u) }
	closeTo(t, g[w], (f(.400001)-f(.399999))/.000002)
}
func TestGaussianGradient(t *testing.T) {
	z := [][]float64{{-.2, .8}, {.3, -.6}, {1., .4}}
	d := Directions(2, 3, 7)
	_, g := GaussianPenalty(z, d)
	eps := 1e-6
	for i := range z {
		for j := range z[i] {
			a, b := clone(z), clone(z)
			a[i][j] += eps
			b[i][j] -= eps
			u, _ := GaussianPenalty(a, d)
			v, _ := GaussianPenalty(b, d)
			closeTo(t, g[i][j], (u-v)/(2*eps))
		}
	}
}
func TestRidgeControl(t *testing.T) {
	x := [][]float64{{-1}, {0}, {1}}
	w, b := Ridge(x, []float64{-1, 1, 3}, 0)
	closeTo(t, w[0], 2)
	closeTo(t, b, 1)
}
func TestClassifierProbabilities(t *testing.T) {
	c := FitClassifier([][]float64{{-2}, {-1}, {1}, {2}}, []int{0, 0, 1, 1}, 200, .15, .01)
	p, q := c.Predict([][]float64{{-2}, {2}})
	if !reflect.DeepEqual(p, []int{0, 1}) {
		t.Fatal(p)
	}
	for _, r := range q {
		closeTo(t, r[0]+r[1], 1)
	}
}
func TestGroupSeparation(t *testing.T) {
	g := []string{"a", "a", "b", "b", "c", "d", "e", "f", "g", "h"}
	a, b, c := GroupSplit(g)
	seen := map[string]int{}
	for p, ids := range [][]int{a, b, c} {
		for _, i := range ids {
			if prev, ok := seen[g[i]]; ok && prev != p {
				t.Fatal("leaked group")
			}
			seen[g[i]] = p
		}
	}
	if len(a)+len(b)+len(c) != len(g) {
		t.Fatal("lost rows")
	}
}
func TestReportedHomologyDimension(t *testing.T) {
	d := Persistence(Rips(square(), 2, 2))
	reported := ReportH01(d)
	for _, v := range reported {
		if v.Dim > 1 {
			t.Fatal("unvalidated top dimension reported")
		}
	}
	if len(reported) >= len(d) {
		t.Fatal("control should remove truncated H2")
	}
}
