package labs

func init() { register("stage17", run_stage17) }
func run_stage17(repo string) (Result, error) {
	a := [][]float64{{0, 0, 0}, {1, 0, 0}, {0, 1, 0}}
	b := [][]float64{{2, 3, 0}, {3, 3, 0}, {2, 4, 0}}
	ca := weightedMean([][][]float64{a})
	cb := weightedMean([][][]float64{b})
	return Result{Lab: "stage17", Title: "Registration", Metrics: map[string]any{"translation": []float64{cb[0] - ca[0], cb[1] - ca[1], cb[2] - ca[2]}}, Notes: []string{"Fit on one reference set and evaluate on different holdouts."}}, nil
}
