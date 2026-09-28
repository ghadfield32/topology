package labs

func init() { register("stage23", run_stage23) }
func run_stage23(repo string) (Result, error) {
	q, p := 1.0, 0.5
	h := 0.5 * (q*q + p*p)
	return Result{Lab: "stage23", Title: "Hamiltonian mechanics", Metrics: map[string]any{"energy": h, "dqdt": p, "dpdt": -q}, Notes: []string{"This harmonic oscillator is a manufactured control."}}, nil
}
