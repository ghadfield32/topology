package engine

import (
	"math"
	"testing"
)

func TestRankField(t *testing.T) {
	a := [][]float64{{1, 1, 0}, {1, 0, 1}, {0, 1, 1}}
	if Rank(a, 1e-10) != 3 || Rank2(a) != 2 {
		t.Fatal("field rank")
	}
}
func TestSolve(t *testing.T) {
	x := Solve([][]float64{{2, 1}, {1, 3}}, []float64{5, 7})
	if math.Abs(x[0]-1.6) > 1e-12 || math.Abs(x[1]-1.8) > 1e-12 {
		t.Fatal(x)
	}
}
func TestSquare(t *testing.T) {
	d := Persistence(Rips([][]float64{{0, 0}, {1, 0}, {1, 1}, {0, 1}}, 2, 2))
	n := 0
	for _, v := range d {
		if v.Dim == 1 && v.Death != nil && *v.Death > v.Birth+1e-9 {
			n++
			if math.Abs(v.Birth-1) > 1e-10 || math.Abs(*v.Death-math.Sqrt(2)) > 1e-10 {
				t.Fatal(v)
			}
		}
	}
	if n != 1 {
		t.Fatal(n)
	}
}
func TestEmptyRejected(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Fatal("expected rejection")
		}
	}()
	MeanRows(nil)
}
func TestAD(t *testing.T) {
	a := NewTape()
	x := a.Input(0.7)
	y := a.Mul(a.Tanh(x), a.Tanh(x))
	g := a.Back(y)
	expected := 2 * math.Tanh(.7) * (1 - math.Pow(math.Tanh(.7), 2))
	if math.Abs(g[x]-expected) > 1e-12 {
		t.Fatal(g[x], expected)
	}
}
