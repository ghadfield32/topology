package labs

import "math"

func init() { register("stage16", run_stage16) }
func run_stage16(repo string) (Result, error) {
	logits := []float64{1, 2, 3}
	mx := 3.0
	ws := make([]float64, 3)
	var s float64
	for i, v := range logits {
		ws[i] = math.Exp(v - mx)
		s += ws[i]
	}
	for i := range ws {
		ws[i] /= s
	}
	return Result{Lab: "stage16", Title: "Attention", Metrics: map[string]any{"softmax": ws, "sum": ws[0] + ws[1] + ws[2]}, Notes: []string{"Attention weights are normalized affinities, not calibrated geometric truth."}}, nil
}
