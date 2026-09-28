package labs

func init() { register("stage21", run_stage21) }
func run_stage21(repo string) (Result, error) {
	dt := 0.1
	ys := []float64{1, 1.21}
	return Result{Lab: "stage21", Title: "Finite differences", Metrics: map[string]any{"forward_derivative": (ys[1] - ys[0]) / dt}, Notes: []string{"Derivative estimate depends on spacing and noise."}}, nil
}
