// Package service owns a bounded queue. Each production job is a separate native process.
package service

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
	"sync"
	"time"
)

type Snapshot struct {
	ID        string          `json:"id"`
	Lab       string          `json:"lab"`
	Status    string          `json:"status"`
	Submitted time.Time       `json:"submitted"`
	Started   *time.Time      `json:"started,omitempty"`
	Finished  *time.Time      `json:"finished,omitempty"`
	Result    json.RawMessage `json:"result,omitempty"`
	Error     string          `json:"error,omitempty"`
}
type work struct {
	s      Snapshot
	ctx    context.Context
	cancel context.CancelFunc
}
type Engine func(context.Context, string) (json.RawMessage, error)
type Manager struct {
	mu      sync.Mutex
	root    context.Context
	stop    context.CancelFunc
	queue   chan *work
	jobs    map[string]*work
	allowed map[string]bool
	engine  Engine
	wg      sync.WaitGroup
	limit   int
	timeout time.Duration
	next    uint64
	closed  bool
}

var ErrFull = errors.New("bounded queue or retention limit reached")
var ErrUnknown = errors.New("unknown lab")
var ErrClosed = errors.New("service closed")

func New(workers, capacity, retention int, timeout time.Duration, engine Engine, allowed map[string]bool) *Manager {
	if workers < 1 || capacity < 1 || retention < 1 || timeout <= 0 {
		panic("positive bounds required")
	}
	c, stop := context.WithCancel(context.Background())
	a := map[string]bool{}
	for k, v := range allowed {
		a[k] = v
	}
	m := &Manager{root: c, stop: stop, queue: make(chan *work, capacity), jobs: map[string]*work{}, allowed: a, engine: engine, limit: retention, timeout: timeout}
	for i := 0; i < workers; i++ {
		m.wg.Add(1)
		go m.worker()
	}
	return m
}
func (m *Manager) Submit(lab string) (Snapshot, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.closed {
		return Snapshot{}, ErrClosed
	}
	if !m.allowed[lab] {
		return Snapshot{}, ErrUnknown
	}
	if len(m.jobs) >= m.limit {
		return Snapshot{}, ErrFull
	}
	m.next++
	id := fmt.Sprintf("job-%06d", m.next)
	ctx, cancel := context.WithTimeout(m.root, m.timeout)
	w := &work{s: Snapshot{ID: id, Lab: lab, Status: "queued", Submitted: time.Now().UTC()}, ctx: ctx, cancel: cancel}
	select {
	case m.queue <- w:
		m.jobs[id] = w
		return w.s, nil
	default:
		cancel()
		return Snapshot{}, ErrFull
	}
}
func (m *Manager) Get(id string) (Snapshot, bool) {
	m.mu.Lock()
	defer m.mu.Unlock()
	w, ok := m.jobs[id]
	if !ok {
		return Snapshot{}, false
	}
	s := w.s
	s.Result = append(json.RawMessage(nil), s.Result...)
	return s, true
}
func (m *Manager) Cancel(id string) bool {
	m.mu.Lock()
	defer m.mu.Unlock()
	w, ok := m.jobs[id]
	if ok {
		w.cancel()
	}
	return ok
}
func (m *Manager) worker() {
	defer m.wg.Done()
	for {
		select {
		case <-m.root.Done():
			return
		case w := <-m.queue:
			m.mu.Lock()
			now := time.Now().UTC()
			w.s.Started = &now
			w.s.Status = "running"
			m.mu.Unlock()
			var result json.RawMessage
			var e error
			if w.ctx.Err() != nil {
				e = w.ctx.Err()
			} else if m.engine == nil {
				e = errors.New("no engine configured")
			} else {
				result, e = m.engine(w.ctx, w.s.Lab)
			}
			m.mu.Lock()
			end := time.Now().UTC()
			w.s.Finished = &end
			switch {
			case errors.Is(w.ctx.Err(), context.DeadlineExceeded):
				w.s.Status = "timed_out"
			case errors.Is(w.ctx.Err(), context.Canceled):
				w.s.Status = "cancelled"
			case e != nil:
				w.s.Status = "failed"
				w.s.Error = e.Error()
			case !json.Valid(result):
				w.s.Status = "failed"
				w.s.Error = "invalid result JSON"
			default:
				w.s.Status = "succeeded"
				w.s.Result = append(json.RawMessage(nil), result...)
			}
			w.cancel()
			m.mu.Unlock()
		}
	}
}
func (m *Manager) Close() {
	m.mu.Lock()
	if m.closed {
		m.mu.Unlock()
		return
	}
	m.closed = true
	m.stop()
	m.mu.Unlock()
	m.wg.Wait()
	m.mu.Lock()
	defer m.mu.Unlock()
	for _, w := range m.jobs {
		if w.s.Status == "queued" || w.s.Status == "running" {
			w.s.Status = "cancelled"
			now := time.Now().UTC()
			w.s.Finished = &now
		}
		w.cancel()
	}
}
func reply(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}
func (m *Manager) Handler() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/health" && r.Method == http.MethodGet {
			reply(w, 200, map[string]bool{"ok": true})
			return
		}
		if r.URL.Path == "/jobs" && r.Method == http.MethodPost {
			var req struct {
				Lab string `json:"lab"`
			}
			d := json.NewDecoder(http.MaxBytesReader(w, r.Body, 65536))
			d.DisallowUnknownFields()
			if e := d.Decode(&req); e != nil {
				reply(w, 400, map[string]string{"error": "invalid request"})
				return
			}
			var extra any
			if d.Decode(&extra) != io.EOF {
				reply(w, 400, map[string]string{"error": "trailing input"})
				return
			}
			s, e := m.Submit(req.Lab)
			if e != nil {
				code := 400
				if errors.Is(e, ErrFull) || errors.Is(e, ErrClosed) {
					code = 503
				}
				reply(w, code, map[string]string{"error": e.Error()})
				return
			}
			reply(w, 202, s)
			return
		}
		if strings.HasPrefix(r.URL.Path, "/jobs/") {
			id := strings.TrimPrefix(r.URL.Path, "/jobs/")
			if r.Method == http.MethodDelete {
				if !m.Cancel(id) {
					reply(w, 404, map[string]string{"error": "unknown job"})
					return
				}
				reply(w, 202, map[string]string{"status": "cancellation_requested"})
				return
			}
			if r.Method == http.MethodGet {
				s, ok := m.Get(id)
				if !ok {
					reply(w, 404, map[string]string{"error": "unknown job"})
					return
				}
				reply(w, 200, s)
				return
			}
		}
		reply(w, 404, map[string]string{"error": "unknown route"})
	})
}
