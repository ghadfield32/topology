package labs

func init() { register("stage29", run_stage29) }
func run_stage29(repo string) (Result, error) {
	theta := 0.3
	dt := 0.1
	x := 1.0
	steps := 10
	for i := 0; i < steps; i++ {
		x = x + dt*(-theta*x)
	}
	eps := 1e-5
	xp := 1.0
	for i := 0; i < steps; i++ {
		xp = xp + dt*(-(theta+eps)*xp)
	}
	sens := (xp - x) / eps
	return Result{Lab: "stage29", Title: "Differentiable simulation", Metrics: map[string]any{"final_state": x, "fd_sensitivity": sens}, Notes: []string{"Finite-difference sensitivity is a check, not automatic autodiff validation."}}, nil
}
