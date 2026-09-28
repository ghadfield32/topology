package labs

func init() { register("wdbc", run_wdbc) }
func run_wdbc(repo string) (Result, error) {
	return genericCase(repo, "wdbc", "Healthcare image-summary classification", "data/industries/wdbc/data.csv")
}
