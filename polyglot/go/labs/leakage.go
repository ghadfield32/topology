package labs

func init() { register("leakage", run_leakage) }
func run_leakage(repo string) (Result, error) {
	return genericStage("leakage", "Identity leakage controls")
}
