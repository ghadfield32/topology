package labs

import "fmt"

type Runner func(string) (Result, error)

var registry = map[string]Runner{}

func register(id string, fn Runner) { registry[id] = fn }
func Run(repo, id string) (Result, error) {
	fn, ok := registry[id]
	if !ok {
		return Result{}, fmt.Errorf("unknown lab %q", id)
	}
	return fn(repo)
}
func IDs() []string {
	out := make([]string, 0, len(registry))
	for k := range registry {
		out = append(out, k)
	}
	return out
}
