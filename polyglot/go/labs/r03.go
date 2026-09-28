package labs

func init() { register("r03", run_r03) }
func run_r03(repo string) (Result, error) {
	return genericStage("r03", "Anti-collapse objectives and gradient paths")
}
