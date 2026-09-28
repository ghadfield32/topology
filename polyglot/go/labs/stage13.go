package labs

import "math"

func init() { register("stage13", run_stage13) }
func run_stage13(repo string) (Result, error) {
	x := []float64{0.2, -0.1}
	r2 := x[0]*x[0] + x[1]*x[1]
	z := []float64{2 * x[0] / (1 + r2), 2 * x[1] / (1 + r2), (r2 - 1) / (1 + r2)}
	return Result{Lab: "stage13", Title: "Manifold chart", Metrics: map[string]any{"sphere_point": z, "norm": math.Sqrt(dot(z, z))}, Notes: []string{"Stereographic-style coordinates provide a local representation."}}, nil
}
