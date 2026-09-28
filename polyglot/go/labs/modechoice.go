package labs

func init() { register("modechoice", run_modechoice) }
func run_modechoice(repo string) (Result, error) {
	return genericCase(repo, "modechoice", "Traveler-level choice sets", "data/industries/modechoice/data.csv")
}
