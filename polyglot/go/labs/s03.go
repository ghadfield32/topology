package labs

func init() { register("s03", run_s03) }
func run_s03(repo string) (Result, error) {
	return genericCase(repo, "s03", "Soccer profile topology", "sports_v8/data/skillcorner_selected_profiles.csv")
}
