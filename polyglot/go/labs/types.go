package labs

type Result struct {
	Lab     string         `json:"lab"`
	Title   string         `json:"title"`
	Metrics map[string]any `json:"metrics"`
	Notes   []string       `json:"notes"`
}
