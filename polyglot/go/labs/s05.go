package labs

func init() { register("s05", run_s05) }
func run_s05(repo string) (Result, error) {
	return genericCase(repo, "s05", "Athlete-group evaluation", "sports_v8/data/skillcorner_selected_profiles.csv")
}
