package labs

import "math"

func init() { register("stage10", run_stage10) }
func run_stage10(repo string) (Result, error) {
	a := []float64{0, 0}
	b := []float64{0.01, -0.02}
	return Result{Lab: "stage10", Title: "Stability", Metrics: map[string]any{"perturbation_linf": math.Max(math.Abs(b[0]-a[0]), math.Abs(b[1]-a[1]))}, Notes: []string{"A perturbation magnitude is not by itself a significance statement."}}, nil
}
