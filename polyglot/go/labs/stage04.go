package labs

import "math"

func init() { register("stage04", run_stage04) }
func run_stage04(repo string) (Result, error) {
	p := [3]float64{1, 0, 0}
	q := rotateZ(p, math.Pi/2)
	return Result{Lab: "stage04", Title: "Symmetry", Metrics: map[string]any{"rotated": q, "norm": math.Sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2])}, Notes: []string{"Rotation preserves Euclidean length."}}, nil
}
