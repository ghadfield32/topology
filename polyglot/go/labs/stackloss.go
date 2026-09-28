package labs

func init() { register("stackloss", run_stackloss) }
func run_stackloss(repo string) (Result, error) {
	return genericCase(repo, "stackloss", "Manufacturing regression", "data/industries/stackloss/data.csv")
}
