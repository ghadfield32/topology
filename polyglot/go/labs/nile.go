package labs

func init() { register("nile", run_nile) }
func run_nile(repo string) (Result, error) {
	return genericCase(repo, "nile", "Water-infrastructure time series", "data/industries/nile/data.csv")
}
