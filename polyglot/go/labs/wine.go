package labs

func init() { register("wine", run_wine) }
func run_wine(repo string) (Result, error) {
	return genericCase(repo, "wine", "Food chemistry and topology", "data/industries/wine/data.csv")
}
