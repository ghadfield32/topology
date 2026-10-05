package service

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func wait(t *testing.T, m *Manager, id string, desired string) {
	t.Helper()
	for i := 0; i < 200; i++ {
		s, _ := m.Get(id)
		if s.Status == desired {
			return
		}
		time.Sleep(time.Millisecond * 5)
	}
	s, _ := m.Get(id)
	t.Fatalf("wanted %s got %+v", desired, s)
}
func TestSuccess(t *testing.T) {
	m := New(1, 1, 10, time.Second, func(context.Context, string) (json.RawMessage, error) { return json.RawMessage(`{"answer":3}`), nil }, map[string]bool{"stage01": true})
	defer m.Close()
	s, e := m.Submit("stage01")
	if e != nil {
		t.Fatal(e)
	}
	wait(t, m, s.ID, "succeeded")
}
func TestUnknown(t *testing.T) {
	m := New(1, 1, 10, time.Second, nil, map[string]bool{})
	defer m.Close()
	if _, e := m.Submit("../../x"); e == nil {
		t.Fatal("accepted unknown lab")
	}
}
func TestCancel(t *testing.T) {
	m := New(1, 1, 10, time.Second, func(c context.Context, _ string) (json.RawMessage, error) { <-c.Done(); return nil, c.Err() }, map[string]bool{"a": true})
	defer m.Close()
	s, _ := m.Submit("a")
	m.Cancel(s.ID)
	wait(t, m, s.ID, "cancelled")
}
func TestTimeout(t *testing.T) {
	m := New(1, 1, 10, time.Millisecond*20, func(c context.Context, _ string) (json.RawMessage, error) { <-c.Done(); return nil, c.Err() }, map[string]bool{"a": true})
	defer m.Close()
	s, _ := m.Submit("a")
	wait(t, m, s.ID, "timed_out")
}
func TestQueueBound(t *testing.T) {
	started := make(chan struct{}, 1)
	m := New(1, 1, 10, time.Second, func(c context.Context, _ string) (json.RawMessage, error) {
		select {
		case started <- struct{}{}:
		default:
		}
		<-c.Done()
		return nil, c.Err()
	}, map[string]bool{"a": true})
	defer m.Close()
	if _, e := m.Submit("a"); e != nil {
		t.Fatal(e)
	}
	select {
	case <-started:
	case <-time.After(time.Second):
		t.Fatal("worker not started")
	}
	m.Submit("a")
	if _, e := m.Submit("a"); e == nil {
		t.Fatal("unbounded queue")
	}
}
func TestHTTPValidation(t *testing.T) {
	m := New(1, 1, 10, time.Second, nil, map[string]bool{})
	defer m.Close()
	for _, body := range []string{`{"lab":"bad"}`, `{"lab":"bad","cmd":"rm"}`, `{}junk`} {
		r := httptest.NewRequest(http.MethodPost, "/jobs", strings.NewReader(body))
		w := httptest.NewRecorder()
		m.Handler().ServeHTTP(w, r)
		if w.Code < 400 {
			t.Fatal(w.Code)
		}
	}
}
func TestCloseRefuses(t *testing.T) {
	m := New(1, 1, 10, time.Second, nil, map[string]bool{"a": true})
	m.Close()
	if _, e := m.Submit("a"); e == nil {
		t.Fatal("accepted after close")
	}
}
