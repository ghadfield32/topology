package labs

func init() { register("stage30", run_stage30) }
func run_stage30(repo string) (Result, error) {
	pts, err := loadSPLBall(repo)
	if err != nil {
		return Result{}, err
	}
	return Result{Lab: "stage30", Title: "An independent world-model study: evidence before adoption", Metrics: map[string]any{"selected_ball_points": len(pts), "centroid_m": weightedMean([][][]float64{pts})}, Notes: []string{"Selected excerpt; not a full tracking corpus."}}, nil
}
