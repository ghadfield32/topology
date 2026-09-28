package labs

func init() { register("co2", run_co2) }
func run_co2(repo string) (Result, error) {
	return genericCase(repo, "co2", "Atmospheric observations and windows", "data/industries/co2/data.csv")
}
