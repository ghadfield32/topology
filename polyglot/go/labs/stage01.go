package labs

func init() { register("stage01", run_stage01) }
func run_stage01(repo string) (Result, error) {
	a := [][]int{{1, 1, 0}, {1, 0, 1}, {0, 1, 1}}
	r := rankMod2(a)
	return Result{Lab: "stage01", Title: "Mathematical language, proofs, and linear algebra", Metrics: map[string]any{"f2_rank": r, "kernel_check": matVec([][]float64{{1, 1}, {0, 0}}, []float64{1, -1})}, Notes: []string{"Same stored matrix can have different rank over R and F2."}}, nil
}
