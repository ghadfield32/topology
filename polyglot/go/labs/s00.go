package labs

func init() { register("s00", run_s00) }
func run_s00(repo string) (Result, error) {
	pts, err := loadSPLBall(repo)
	if err != nil {
		return Result{}, err
	}
	return Result{Lab: "s00", Title: "Sports observations and units", Metrics: map[string]any{"selected_ball_points": len(pts), "centroid_m": weightedMean([][][]float64{pts})}, Notes: []string{"Selected excerpt; not a full tracking corpus."}}, nil
}
