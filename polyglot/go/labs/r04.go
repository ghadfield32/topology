package labs

func init() { register("r04", run_r04) }
func run_r04(repo string) (Result, error) {
	return genericStage("r04", "Train a representation and evaluate frozen probes")
}
