package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"shape-job-service/service"
	"syscall"
	"time"
)

type limitedBuffer struct {
	bytes.Buffer
	limit int
}

func (b *limitedBuffer) Write(p []byte) (int, error) {
	if len(p) > b.limit-b.Len() {
		return 0, fmt.Errorf("native output exceeds bound")
	}
	return b.Buffer.Write(p)
}
func main() {
	repo := flag.String("repo", ".", "course root")
	binary := flag.String("binary", "", "explicit compiled native Go executable")
	listen := flag.String("listen", "127.0.0.1:8090", "loopback by default; no authentication provided")
	workers := flag.Int("workers", 2, "bounded workers")
	capacity := flag.Int("capacity", 4, "queue bound")
	flag.Parse()
	if *binary == "" {
		fmt.Fprintln(os.Stderr, "--binary is required; arbitrary commands are not accepted over HTTP")
		os.Exit(2)
	}
	full, e := filepath.Abs(*repo)
	if e != nil {
		panic(e)
	}
	exe, e := filepath.Abs(*binary)
	if e != nil {
		panic(e)
	}
	b, e := os.ReadFile(filepath.Join(full, "native/protocols/labs.json"))
	if e != nil {
		panic(e)
	}
	var reg struct {
		Labs []struct {
			Key string `json:"key"`
		} `json:"labs"`
	}
	if e = json.Unmarshal(b, &reg); e != nil {
		panic(e)
	}
	allowed := map[string]bool{}
	for _, l := range reg.Labs {
		allowed[l.Key] = true
	}
	engine := func(c context.Context, lab string) (json.RawMessage, error) {
		cmd := exec.CommandContext(c, exe, "--repo", full, "--lab", lab)
		var out, errout limitedBuffer
		out.limit = 8 << 20
		errout.limit = 1 << 20
		cmd.Stdout = &out
		cmd.Stderr = &errout
		err := cmd.Run()
		if err != nil {
			return nil, fmt.Errorf("native process failed: %v: %s", err, errout.String())
		}
		return json.RawMessage(out.Bytes()), nil
	}
	m := service.New(*workers, *capacity, 128, 2*time.Minute, engine, allowed)
	defer m.Close()
	server := &http.Server{Addr: *listen, Handler: m.Handler(), ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 10 * time.Second, WriteTimeout: 10 * time.Second, IdleTimeout: 30 * time.Second}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	go func() {
		<-ctx.Done()
		c, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		server.Shutdown(c)
	}()
	fmt.Printf("Local teaching service %s (in-memory results, bounded retention=128)\n", *listen)
	if e := server.ListenAndServe(); e != nil && e != http.ErrServerClosed {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}
