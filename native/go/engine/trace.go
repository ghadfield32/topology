package engine

import "sync"

var inputAudit = struct {
	sync.Mutex
	values map[string]map[string]any
}{values: map[string]map[string]any{}}

func BeginAudit() {
	inputAudit.Lock()
	defer inputAudit.Unlock()
	inputAudit.values = map[string]map[string]any{}
}
func recordInput(path string, b []byte) {
	inputAudit.Lock()
	defer inputAudit.Unlock()
	inputAudit.values[path] = map[string]any{"sha256": SHA(b), "bytes": len(b)}
}
func InputAudit() map[string]map[string]any {
	inputAudit.Lock()
	defer inputAudit.Unlock()
	out := map[string]map[string]any{}
	for k, v := range inputAudit.values {
		out[k] = v
	}
	return out
}
func BoundaryMatrix(c []Simplex, k int) [][]float64 {
	require(k > 0, "positive boundary dimension")
	c = Ordered(c)
	rows := []Simplex{}
	cols := []Simplex{}
	for _, s := range c {
		if len(s.Vertices) == k {
			rows = append(rows, s)
		}
		if len(s.Vertices) == k+1 {
			cols = append(cols, s)
		}
	}
	index := map[string]int{}
	for i, s := range rows {
		index[simplexKey(s.Vertices)] = i
	}
	a := Zeros(len(rows), len(cols))
	for j, s := range cols {
		for q := range s.Vertices {
			f := append([]int(nil), s.Vertices[:q]...)
			f = append(f, s.Vertices[q+1:]...)
			a[index[simplexKey(f)]][j] = 1
		}
	}
	return a
}
func AlgebraControl() map[string]any {
	c := Triangle(true)
	b1, b2 := BoundaryMatrix(c, 1), BoundaryMatrix(c, 2)
	prod := MatMul(b1, b2)
	for i := range prod {
		for j := range prod[i] {
			prod[i][j] = float64(int(prod[i][j]) % 2)
		}
	}
	return map[string]any{"boundary_1": b1, "boundary_2": b2, "boundary_squared_mod2": prod, "rank_boundary_1": Rank2(b1), "rank_boundary_2": Rank2(b2), "cycle_dimension_1": len(b2) - Rank2(b1), "homology_dimension_1": len(b2) - Rank2(b1) - Rank2(b2)}
}
