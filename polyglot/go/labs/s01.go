package labs

func init() { register("s01", run_s01) }
func run_s01(repo string) (Result, error) {
	pts, err := loadSPLBall(repo)
	if err != nil {
		return Result{}, err
	}
	return Result{Lab: "s01", Title: "Landmark angles and velocity", Metrics: map[string]any{"selected_ball_points": len(pts), "centroid_m": weightedMean([][][]float64{pts})}, Notes: []string{"Selected excerpt; not a full tracking corpus."}}, nil
}
