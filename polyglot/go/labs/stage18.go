package labs

func init() { register("stage18", run_stage18) }
func run_stage18(repo string) (Result, error) {
	pts := [][]float64{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
	m := weightedMean([][][]float64{pts[:1], pts[1:]})
	return Result{Lab: "stage18", Title: "Streaming", Metrics: map[string]any{"mean": m}, Notes: []string{"Count-weighted streaming summaries must match whole-data summaries."}}, nil
}
