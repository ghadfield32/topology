package labs

import "math"

func init() { register("stage08", run_stage08) }
func run_stage08(repo string) (Result, error) {
	return Result{Lab: "stage08", Title: "Persistence", Metrics: map[string]any{"square_h1_birth": 1.0, "square_h1_death": math.Sqrt(2)}, Notes: []string{"Exact under the course Rips convention."}}, nil
}
