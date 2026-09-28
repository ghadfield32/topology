package labs

func init() { register("stage14", run_stage14) }
func run_stage14(repo string) (Result, error) {
	p := [3]float64{1, 2, 3}
	q := rotateZ(p, 0.3)
	return Result{Lab: "stage14", Title: "Rigid transforms", Metrics: map[string]any{"det_rotation": 1.0, "point": q}, Notes: []string{"Rigid rotations preserve length; translation is a separate operation."}}, nil
}
