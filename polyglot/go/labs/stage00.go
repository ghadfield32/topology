package labs

func init() { register("stage00", run_stage00) }
func run_stage00(repo string) (Result, error) {
	rows, err := csvRows(repoPath(repo, "data", "raw", "iris.csv"))
	if err != nil {
		return Result{}, err
	}
	return Result{Lab: "stage00", Title: "Start here", Metrics: map[string]any{"iris_rows": len(rows) - 1, "iris_columns": len(rows[0])}, Notes: []string{"One row is one measured flower record in this snapshot."}}, nil
}
