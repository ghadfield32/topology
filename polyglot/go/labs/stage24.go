package labs

func init() { register("stage24", run_stage24) }
func run_stage24(repo string) (Result, error) {
	q, p, h := 1.0, 0.0, 0.2
	p1 := p - h*q
	q1 := q + h*p1
	e0 := 0.5 * (q*q + p*p)
	e1 := 0.5 * (q1*q1 + p1*p1)
	return Result{Lab: "stage24", Title: "Symplectic counterexample", Metrics: map[string]any{"energy_before": e0, "energy_after": e1, "delta": e1 - e0}, Notes: []string{"Symplectic does not imply exact energy conservation at each discrete step."}}, nil
}
