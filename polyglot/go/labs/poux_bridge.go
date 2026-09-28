package labs

import "fmt"

func init() { register("poux_bridge", run_poux_bridge) }
func run_poux_bridge(repo string) (Result, error) {
	pts, err := loadSPLBall(repo)
	if err != nil {
		return Result{}, err
	}
	if len(pts) < 2 {
		return Result{}, fmt.Errorf("need >=2 points")
	}
	chunks := [][][]float64{pts[:1], pts[1:]}
	w := weightedMean(chunks)
	e := equalMeanOfChunkMeans(chunks)
	return Result{Lab: "poux_bridge", Title: "Poux weighted streaming bridge", Metrics: map[string]any{"points": len(pts), "weighted_mean_m": w, "equal_chunk_mean_m": e, "centroid_shift_m": l2(w, e)}, Notes: []string{"Selected nonuniform frames: centroid is not a time average or release point."}}, nil
}
