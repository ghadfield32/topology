package labs

func init() { register("grunfeld", run_grunfeld) }
func run_grunfeld(repo string) (Result, error) {
	return genericCase(repo, "grunfeld", "Firm-year panel measurements", "data/industries/grunfeld/data.csv")
}
