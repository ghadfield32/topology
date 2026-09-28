package labs

func init() { register("r02", run_r02) }
func run_r02(repo string) (Result, error) {
	return genericStage("r02", "Projections, characteristic functions, and SIGReg")
}
