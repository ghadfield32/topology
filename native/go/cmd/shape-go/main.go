package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"shape-native/engine"
)

func main() { os.Exit(run()) }
func run() (code int) {
	defer func() {
		if e := recover(); e != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", e)
			code = 1
		}
	}()
	repo := flag.String("repo", ".", "course root")
	lab := flag.String("lab", "", "lab key")
	decode := flag.String("decode", "", "decode a repo-relative source file")
	out := flag.String("output", "", "NEW evidence directory")
	list := flag.Bool("list", false, "list lab keys")
	flag.Parse()
	var result any
	if *list {
		result = engine.LabKeys(*repo)
	} else if *decode != "" {
		result = engine.Decode(*repo, *decode)
	} else {
		var e error
		result, e = engine.Run(*repo, *lab)
		if e != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", e)
			return 1
		}
	}
	data, e := json.MarshalIndent(result, "", "  ")
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		return 1
	}
	if *out != "" {
		if _, e := os.Stat(*out); !os.IsNotExist(e) {
			fmt.Fprintln(os.Stderr, "output exists or cannot be checked; choose a new directory")
			return 1
		}
		if e := os.MkdirAll(filepath.Dir(*out), 0755); e != nil {
			fmt.Fprintln(os.Stderr, e)
			return 1
		}
		if e := os.Mkdir(*out, 0755); e != nil {
			fmt.Fprintln(os.Stderr, e)
			return 1
		}
		p := filepath.Join(*out, "result.json")
		if e := os.WriteFile(p, append(data, '\n'), 0644); e != nil {
			fmt.Fprintln(os.Stderr, e)
			return 1
		}
		fmt.Println(p)
	} else {
		fmt.Println(string(data))
	}
	return 0
}
