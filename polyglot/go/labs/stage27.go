package labs

func init() { register("stage27", run_stage27) }
func run_stage27(repo string) (Result, error) {
	g1 := []float64{1, 0}
	g2 := []float64{-1, 0}
	conflict := dot(g1, g2) < 0
	return Result{Lab: "stage27", Title: "Gradient conflict", Metrics: map[string]any{"dot": dot(g1, g2), "conflict": conflict}, Notes: []string{"Opposite gradients expose an incompatible first-order objective pair."}}, nil
}
