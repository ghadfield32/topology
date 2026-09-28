package labs

import "math"

func init() { register("stage22", run_stage22) }
func run_stage22(repo string) (Result, error) {
	x0 := 2.0
	t := 0.5
	return Result{Lab: "stage22", Title: "Smooth flows", Metrics: map[string]any{"x_t": x0 * math.Exp(t), "inverse": x0 * math.Exp(t) * math.Exp(-t)}, Notes: []string{"The exact flow of x'=x is invertible for finite t."}}, nil
}
