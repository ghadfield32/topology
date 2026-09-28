package labs

func init() { register("stage07", run_stage07) }
func run_stage07(repo string) (Result, error) {
	pts := [][]float64{{0, 0}, {1, 0}, {1, 1}, {0, 1}}
	eps := 1.01
	edges := 0
	for i := 0; i < len(pts); i++ {
		for j := i + 1; j < len(pts); j++ {
			if l2(pts[i], pts[j]) <= eps {
				edges++
			}
		}
	}
	return Result{Lab: "stage07", Title: "Rips", Metrics: map[string]any{"epsilon": eps, "edges": edges}, Notes: []string{"At this scale the unit square has perimeter edges but no diagonals."}}, nil
}
