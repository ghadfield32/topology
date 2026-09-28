package labs

func init() { register("concrete_slump", run_concrete_slump) }
func run_concrete_slump(repo string) (Result, error) {
	return genericCase(repo, "concrete_slump", "Materials measurements and intervals", "data/v7/concrete_slump/table.csv")
}
