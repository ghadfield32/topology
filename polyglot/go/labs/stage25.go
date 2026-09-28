package labs

func init() { register("stage25", run_stage25) }
func run_stage25(repo string) (Result, error) {
	x, y := 2.0, 0.0
	c := x*x + y*y - 1
	gx, gy := 2*x, 2*y
	den := gx*gx + gy*gy
	x1 := x - gx*c/den
	y1 := y - gy*c/den
	return Result{Lab: "stage25", Title: "Constraint projection", Metrics: map[string]any{"residual_after": x1*x1 + y1*y1 - 1}, Notes: []string{"One linearized correction need not satisfy a nonlinear constraint exactly."}}, nil
}
