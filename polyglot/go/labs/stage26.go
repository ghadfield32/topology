package labs

import "math"

func init() { register("stage26", run_stage26) }
func run_stage26(repo string) (Result, error) {
	x := 0.4
	u := math.Sin(math.Pi * x)
	uxx := -math.Pi * math.Pi * u
	res := uxx + math.Pi*math.Pi*u
	return Result{Lab: "stage26", Title: "PINN residual control", Metrics: map[string]any{"analytic_residual": res}, Notes: []string{"Known solution provides a control before neural optimization."}}, nil
}
