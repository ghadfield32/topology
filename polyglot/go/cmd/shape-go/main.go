package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"listening-to-shape/polyglot/go/labs"
	"os"
	"sort"
)

func main() {
	repo := flag.String("repo", "../..", "course repository root")
	lab := flag.String("lab", "stage01", "lab id")
	list := flag.Bool("list", false, "list labs")
	flag.Parse()
	if *list {
		ids := labs.IDs()
		sort.Strings(ids)
		for _, id := range ids {
			fmt.Println(id)
		}
		return
	}
	r, err := labs.Run(*repo, *lab)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	b, _ := json.MarshalIndent(r, "", "  ")
	fmt.Println(string(b))
}
