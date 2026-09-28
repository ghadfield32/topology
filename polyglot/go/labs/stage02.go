package labs

import "math"

func init() { register("stage02", run_stage02) }
func run_stage02(repo string) (Result, error) {
	a := []float64{1, 2}
	b := []float64{4, 6}
	eu := l2(a, b)
	man := math.Abs(a[0]-b[0]) + math.Abs(a[1]-b[1])
	return Result{Lab: "stage02", Title: "Metrics", Metrics: map[string]any{"euclidean": eu, "manhattan": man}, Notes: []string{"A metric choice changes neighborhoods."}}, nil
}
