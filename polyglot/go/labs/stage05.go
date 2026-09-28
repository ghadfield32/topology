package labs

func init() { register("stage05", run_stage05) }
func run_stage05(repo string) (Result, error) {
	vertices := 3
	edges := 3
	faces := 0
	if "stage05" == "stage06" {
		faces = 1
	}
	euler := vertices - edges + faces
	return Result{Lab: "stage05", Title: "Simplicial structure", Metrics: map[string]any{"vertices": vertices, "edges": edges, "faces": faces, "euler": euler}, Notes: []string{"Triangle boundary and filled triangle are different complexes."}}, nil
}
