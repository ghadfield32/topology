package labs

func init() { register("r01", run_r01) }
func run_r01(repo string) (Result, error) {
	return genericStage("r01", "Distributions, moments, and whitening")
}
