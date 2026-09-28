package labs

func init() { register("stage03", run_stage03) }
func run_stage03(repo string) (Result, error) {
	p := []float64{2, 3, 9}
	q := []float64{2, 3, -4}
	return Result{Lab: "stage03", Title: "Continuity and maps", Metrics: map[string]any{"projection_same": p[0] == q[0] && p[1] == q[1]}, Notes: []string{"Projection can be continuous while losing information."}}, nil
}
