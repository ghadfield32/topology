package labs

func init() { register("elnino", run_elnino) }
func run_elnino(repo string) (Result, error) {
	return genericCase(repo, "elnino", "Marine climate", "data/industries/elnino/data.csv")
}
