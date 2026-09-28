package labs

func init() { register("seeds", run_seeds) }
func run_seeds(repo string) (Result, error) {
	return genericCase(repo, "seeds", "Agriculture feature-space geometry", "data/v7/seeds/table.csv")
}
