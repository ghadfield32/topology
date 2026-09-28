package labs

import (
	"math"
	"path/filepath"
	"testing"
)

func TestRankMod2(t *testing.T) {
	if rankMod2([][]int{{1, 1, 0}, {1, 0, 1}, {0, 1, 1}}) != 2 {
		t.Fatal("rank")
	}
}
func TestRotation(t *testing.T) {
	q := rotateZ([3]float64{1, 0, 0}, math.Pi/2)
	if math.Abs(q[0]) > 1e-12 || math.Abs(q[1]-1) > 1e-12 {
		t.Fatalf("%v", q)
	}
}
func TestWeightedMean(t *testing.T) {
	w := weightedMean([][][]float64{{{0}}, {{3}, {6}, {9}}})
	if math.Abs(w[0]-4.5) > 1e-12 {
		t.Fatal(w)
	}
}
func TestAllRegistered(t *testing.T) {
	if len(registry) != 57 {
		t.Fatalf("got %d", len(registry))
	}
}
func TestStage00Data(t *testing.T) {
	repo := filepath.Join("..", "..", "..")
	r, e := Run(repo, "stage00")
	if e != nil {
		t.Fatal(e)
	}
	if r.Metrics["iris_rows"].(int) != 150 {
		t.Fatal(r.Metrics)
	}
}
func TestPouxBridge(t *testing.T) {
	repo := filepath.Join("..", "..", "..")
	r, e := Run(repo, "poux_bridge")
	if e != nil {
		t.Fatal(e)
	}
	x := r.Metrics["centroid_shift_m"].(float64)
	if x <= 1.0 || x >= 1.3 {
		t.Fatalf("shift=%v", x)
	}
}
