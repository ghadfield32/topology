package labs

func init() { register("acb", run_acb) }
func run_acb(repo string) (Result, error) {
	return genericStage("acb", "ACB 2025–26 source and identity readiness")
}
