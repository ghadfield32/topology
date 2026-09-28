package engine

import (
	"math"
	"sort"
)

// Tape records a scalar reverse-mode computational graph. Node indices are stable.
type Node struct {
	V       float64
	Parents []int
	Weights []float64
}
type Tape struct{ Nodes []Node }

func NewTape() *Tape { return &Tape{} }
func (t *Tape) node(v float64, p []int, w []float64) int {
	require(finite(v), "nonfinite autodiff value")
	t.Nodes = append(t.Nodes, Node{v, p, w})
	return len(t.Nodes) - 1
}
func (t *Tape) Input(v float64) int { return t.node(v, nil, nil) }
func (t *Tape) Val(i int) float64   { return t.Nodes[i].V }
func (t *Tape) Add(a, b int) int    { return t.node(t.Val(a)+t.Val(b), []int{a, b}, []float64{1, 1}) }
func (t *Tape) Sub(a, b int) int    { return t.node(t.Val(a)-t.Val(b), []int{a, b}, []float64{1, -1}) }
func (t *Tape) Mul(a, b int) int {
	return t.node(t.Val(a)*t.Val(b), []int{a, b}, []float64{t.Val(b), t.Val(a)})
}
func (t *Tape) Div(a, b int) int {
	v := t.Val(b)
	require(v != 0, "autodiff division by zero")
	return t.node(t.Val(a)/v, []int{a, b}, []float64{1 / v, -t.Val(a) / (v * v)})
}
func (t *Tape) Tanh(a int) int {
	v := math.Tanh(t.Val(a))
	return t.node(v, []int{a}, []float64{1 - v*v})
}
func (t *Tape) Sin(a int) int {
	return t.node(math.Sin(t.Val(a)), []int{a}, []float64{math.Cos(t.Val(a))})
}
func (t *Tape) Exp(a int) int { v := math.Exp(t.Val(a)); return t.node(v, []int{a}, []float64{v}) }
func (t *Tape) Log(a int) int {
	require(t.Val(a) > 0, "log domain")
	return t.node(math.Log(t.Val(a)), []int{a}, []float64{1 / t.Val(a)})
}
func (t *Tape) Scale(a int, v float64) int { return t.Mul(a, t.Input(v)) }
func (t *Tape) Back(root int) []float64 {
	g := make([]float64, len(t.Nodes))
	g[root] = 1
	for i := root; i >= 0; i-- {
		n := t.Nodes[i]
		for j, p := range n.Parents {
			g[p] += g[i] * n.Weights[j]
		}
	}
	return g
}

// Jet contains value, first and second input derivatives; each remains on the tape.
type Jet struct{ V, D, D2 int }

func jconst(t *Tape, v float64) Jet { return Jet{t.Input(v), t.Input(0), t.Input(0)} }
func jvar(t *Tape, v float64, active bool) Jet {
	d := 0.
	if active {
		d = 1
	}
	return Jet{t.Input(v), t.Input(d), t.Input(0)}
}
func jadd(t *Tape, a, b Jet) Jet { return Jet{t.Add(a.V, b.V), t.Add(a.D, b.D), t.Add(a.D2, b.D2)} }
func jmul(t *Tape, a, b Jet) Jet {
	return Jet{t.Mul(a.V, b.V), t.Add(t.Mul(a.D, b.V), t.Mul(a.V, b.D)), t.Add(t.Add(t.Mul(a.D2, b.V), t.Scale(t.Mul(a.D, b.D), 2)), t.Mul(a.V, b.D2))}
}
func jtanh(t *Tape, a Jet) Jet {
	v := t.Tanh(a.V)
	f := t.Sub(t.Input(1), t.Mul(v, v))
	d := t.Mul(f, a.D)
	d2 := t.Mul(f, t.Sub(a.D2, t.Scale(t.Mul(v, t.Mul(a.D, a.D)), 2)))
	return Jet{v, d, d2}
}
func jetNetwork(t *Tape, params []int, input []Jet, h int) Jet {
	d := len(input)
	need := h*(d+2) + 1
	require(len(params) == need, "jet network parameter count")
	out := jconst(t, 0)
	for j := 0; j < h; j++ {
		z := Jet{params[h*d+j], t.Input(0), t.Input(0)}
		for k := 0; k < d; k++ {
			w := Jet{params[j*d+k], t.Input(0), t.Input(0)}
			z = jadd(t, z, jmul(t, w, input[k]))
		}
		a := jtanh(t, z)
		w := Jet{params[h*d+h+j], t.Input(0), t.Input(0)}
		out = jadd(t, out, jmul(t, w, a))
	}
	return jadd(t, out, Jet{params[len(params)-1], t.Input(0), t.Input(0)})
}
func TrainPhysics(kind string) map[string]any {
	d, h := 1, 8
	if kind == "hnn" {
		d = 2
	}
	r := RNG{17}
	weights := make([]float64, h*(d+2)+1)
	for i := range weights {
		weights[i] = r.Normal() * .25
	}
	losses := []float64{}
	epochs := 120
	lr := .015
	if kind == "pinn" {
		epochs = 180
		lr = .01
	}
	for ep := 0; ep < epochs; ep++ {
		t := NewTape()
		p := make([]int, len(weights))
		for i, w := range weights {
			p[i] = t.Input(w)
		}
		loss := t.Input(0)
		n := 24
		for i := 0; i < n; i++ {
			q := -1.2 + 2.4*float64(i)/float64(n-1)
			if kind == "pinn" {
				q = float64(i+1) / float64(n+1)
			}
			x := []Jet{jvar(t, q, true)}
			if d == 2 {
				x = append(x, jvar(t, math.Sin(float64(i)*1.7), false))
			}
			z := jetNetwork(t, p, x, h)
			var err int
			if kind == "pinn" {
				factor := jmul(t, x[0], jadd(t, jconst(t, 1), jmul(t, jconst(t, -1), x[0])))
				u := jmul(t, factor, z)
				err = t.Add(u.D2, t.Input(math.Pi*math.Pi*math.Sin(math.Pi*q)))
			} else {
				err = t.Sub(z.D, t.Input(q))
			}
			loss = t.Add(loss, t.Scale(t.Mul(err, err), 1/float64(n)))
			if kind == "hnn" {
				pp := math.Sin(float64(i) * 1.7)
				x2 := []Jet{jvar(t, q, false), jvar(t, pp, true)}
				v := jetNetwork(t, p, x2, h)
				e := t.Sub(v.D, t.Input(pp))
				loss = t.Add(loss, t.Scale(t.Mul(e, e), 1/float64(n)))
			}
		}
		losses = append(losses, t.Val(loss))
		g := t.Back(loss)
		gn := 0.
		for _, k := range p {
			gn += g[k] * g[k]
		}
		clip := 1.
		if math.Sqrt(gn) > 20 {
			clip = 20 / math.Sqrt(gn)
		}
		for i, k := range p {
			weights[i] -= lr * clip * g[k]
		}
	}
	grid, pred, truth := []float64{}, []float64{}, []float64{}
	for i := 0; i < 81; i++ {
		q := -1. + 2*float64(i)/80
		if kind == "pinn" {
			q = float64(i) / 80
		}
		t := NewTape()
		p := make([]int, len(weights))
		for j, w := range weights {
			p[j] = t.Input(w)
		}
		x := []Jet{jvar(t, q, true)}
		if d == 2 {
			x = append(x, jvar(t, .3, false))
		}
		z := jetNetwork(t, p, x, h)
		v, target := -t.Val(z.D), -q
		if kind == "pinn" {
			v = q * (1 - q) * t.Val(z.V)
			target = math.Sin(math.Pi * q)
		}
		grid = append(grid, q)
		pred = append(pred, v)
		truth = append(truth, target)
	}
	return map[string]any{"model": kind, "origin": "manufactured analytical system", "epochs": epochs, "hidden_width": h, "learning_rate": lr, "loss_history": losses, "grid": grid, "predictions": pred, "truth": truth, "rmse": RMSE(truth, pred), "weights": weights, "derivatives": "forward second-order jets over a reverse-mode parameter tape", "scope": "small native teaching architecture; LNN fixes unit mass and learns only potential"}
}

type Classifier struct {
	W       [][]float64
	Classes []int
	Loss    []float64
}

func FitClassifier(x [][]float64, y []int, epochs int, lr, penalty float64) Classifier {
	n, d := shape(x)
	require(n == len(y), "classifier row mismatch")
	set := map[int]bool{}
	for _, v := range y {
		set[v] = true
	}
	classes := []int{}
	for k := range set {
		classes = append(classes, k)
	}
	sort.Ints(classes)
	require(len(classes) > 1, "classifier needs multiple classes")
	lookup := map[int]int{}
	for i, k := range classes {
		lookup[k] = i
	}
	k := len(classes)
	w := Zeros(k, d+1)
	hist := []float64{}
	for ep := 0; ep < epochs; ep++ {
		g := Zeros(k, d+1)
		loss := 0.
		for i, row := range x {
			logits := make([]float64, k)
			for c := 0; c < k; c++ {
				logits[c] = dot(w[c][:d], row) + w[c][d]
			}
			p := softmax(logits)
			loss -= math.Log(math.Max(p[lookup[y[i]]], 1e-300)) / float64(n)
			for c := 0; c < k; c++ {
				e := p[c]
				if c == lookup[y[i]] {
					e -= 1
				}
				for j, v := range row {
					g[c][j] += e * v / float64(n)
				}
				g[c][d] += e / float64(n)
			}
		}
		for c := 0; c < k; c++ {
			for j := 0; j < d; j++ {
				loss += penalty * w[c][j] * w[c][j] / 2
				g[c][j] += penalty * w[c][j]
			}
			for j := 0; j <= d; j++ {
				w[c][j] -= lr * g[c][j]
			}
		}
		hist = append(hist, loss)
	}
	return Classifier{w, classes, hist}
}
func (c Classifier) Predict(x [][]float64) ([]int, [][]float64) {
	_, d := shape(x)
	out := make([]int, len(x))
	probs := Zeros(len(x), len(c.Classes))
	for i, row := range x {
		z := make([]float64, len(c.Classes))
		for k := range z {
			z[k] = dot(c.W[k][:d], row) + c.W[k][d]
		}
		p := softmax(z)
		best := 0
		for k := range p {
			if p[k] > p[best] {
				best = k
			}
		}
		out[i] = c.Classes[best]
		probs[i] = p
	}
	return out, probs
}
func fitPredict(x [][]float64, y []int, tr, va, te []int) map[string]any {
	s := FitScaler(Rows(x, tr))
	m := FitClassifier(s.Transform(Rows(x, tr)), Labels(y, tr), 160, .15, .01)
	p, pr := m.Predict(s.Transform(Rows(x, te)))
	pv, _ := m.Predict(s.Transform(Rows(x, va)))
	return map[string]any{"accuracy": accuracy(Labels(y, te), p), "validation_accuracy": accuracy(Labels(y, va), pv), "truth": Labels(y, te), "predictions": p, "probabilities": pr, "scaler_mean": s.Mean, "scaler_scale": s.Scale, "weights": m.W, "loss_history": m.Loss}
}
func Ridge(x [][]float64, y []float64, lambda float64) ([]float64, float64) {
	n, d := shape(x)
	require(n == len(y) && finite(lambda) && lambda >= 0, "ridge input")
	mx := MeanRows(x)
	centered := clone(x)
	for i := range centered {
		for j := range centered[i] {
			centered[i][j] -= mx[j]
		}
	}
	mu := Mean(y)
	a := Zeros(d, d)
	b := make([]float64, d)
	for i, row := range centered {
		for j := 0; j < d; j++ {
			b[j] += row[j] * (y[i] - mu)
			for k := 0; k < d; k++ {
				a[j][k] += row[j] * row[k]
			}
		}
	}
	for j := range a {
		a[j][j] += lambda
	}
	w := Solve(a, b)
	return w, mu - dot(mx, w)
}
func predictRidge(x [][]float64, w []float64, b float64) []float64 {
	p := make([]float64, len(x))
	for i, row := range x {
		p[i] = dot(row, w) + b
	}
	return p
}
func regressionResult(x [][]float64, y []float64, tr, va, te []int, conformal bool) map[string]any {
	s := FitScaler(Rows(x, tr))
	w, b := Ridge(s.Transform(Rows(x, tr)), Values(y, tr), 1)
	p := predictRidge(s.Transform(Rows(x, te)), w, b)
	pv := predictRidge(s.Transform(Rows(x, va)), w, b)
	baseline := make([]float64, len(te))
	for i := range baseline {
		baseline[i] = b
	}
	out := map[string]any{"train_rows": tr, "validation_rows": va, "test_rows": te, "truth": Values(y, te), "predictions": p, "mae": MAE(Values(y, te), p), "rmse": RMSE(Values(y, te), p), "baseline_mae": MAE(Values(y, te), baseline), "scaler_mean": s.Mean, "scaler_scale": s.Scale, "weights": w, "intercept": b}
	if conformal {
		res := make([]float64, len(va))
		for i, k := range va {
			res[i] = math.Abs(y[k] - pv[i])
		}
		sort.Float64s(res)
		rank := int(math.Ceil(.9 * float64(len(va)+1)))
		require(rank <= len(res), "insufficient calibration size for finite 90% interval")
		q := res[rank-1]
		covered := 0
		bounds := Zeros(len(p), 2)
		for i, v := range p {
			bounds[i] = []float64{v - q, v + q}
			if math.Abs(y[te[i]]-v) <= q {
				covered++
			}
		}
		out["nominal_coverage"] = .9
		out["interval_radius"] = q
		out["intervals"] = bounds
		out["covered"] = covered
		out["calibration_rows"] = va
		out["interpretation"] = "marginal split-conformal illustration, no batch-conditional guarantee"
	}
	return out
}

// GaussianPenalty is an explicit finite-frequency characteristic-function penalty.
// It is related to SIGReg, not a byte-for-byte reproduction of LeJEPA training.
func GaussianPenalty(z, dirs [][]float64) (float64, [][]float64) {
	n, d := shape(z)
	k, _ := shape(dirs)
	g := Zeros(n, d)
	loss := 0.
	freq := []float64{.25, .5, 1, 1.5, 2}
	for _, dir := range dirs {
		require(len(dir) == d, "projection dimensions")
		u := make([]float64, n)
		for i := range z {
			u[i] = dot(z[i], dir)
		}
		for _, t := range freq {
			re, im := 0., 0.
			for _, v := range u {
				re += math.Cos(t*v) / float64(n)
				im += math.Sin(t*v) / float64(n)
			}
			target := math.Exp(-t * t / 2)
			w := math.Exp(-t*t/2) / float64(k*len(freq))
			loss += w * ((re-target)*(re-target) + im*im)
			for i, v := range u {
				du := 2 * w * t * (-(re-target)*math.Sin(t*v) + im*math.Cos(t*v)) / float64(n)
				for j := 0; j < d; j++ {
					g[i][j] += du * dir[j]
				}
			}
		}
	}
	return loss, g
}
func Directions(d, k int, seed uint32) [][]float64 {
	r := RNG{seed}
	a := Zeros(k, d)
	for i := range a {
		for j := range a[i] {
			a[i][j] = r.Normal()
		}
		s := norm(a[i])
		for j := range a[i] {
			a[i][j] /= s
		}
	}
	return a
}

type Encoder struct {
	W1, W2 [][]float64
	B1, B2 []float64
}

func NewEncoder(d, h, z int, seed uint32) Encoder {
	r := RNG{seed}
	e := Encoder{Zeros(h, d), Zeros(z, h), make([]float64, h), make([]float64, z)}
	for i := range e.W1 {
		for j := range e.W1[i] {
			e.W1[i][j] = r.Normal() / math.Sqrt(float64(d))
		}
	}
	for i := range e.W2 {
		for j := range e.W2[i] {
			e.W2[i][j] = r.Normal() / math.Sqrt(float64(h))
		}
	}
	return e
}
func (e Encoder) Forward(x [][]float64) ([][]float64, [][]float64) {
	h := Zeros(len(x), len(e.B1))
	z := Zeros(len(x), len(e.B2))
	for i, row := range x {
		for j := range e.B1 {
			h[i][j] = math.Tanh(dot(e.W1[j], row) + e.B1[j])
		}
		for j := range e.B2 {
			z[i][j] = dot(e.W2[j], h[i]) + e.B2[j]
		}
	}
	return h, z
}
func (e *Encoder) Update(x, h, g [][]float64, lr float64) {
	dw1, dw2 := Zeros(len(e.W1), len(e.W1[0])), Zeros(len(e.W2), len(e.W2[0]))
	db1, db2 := make([]float64, len(e.B1)), make([]float64, len(e.B2))
	for i, row := range x {
		dh := make([]float64, len(e.B1))
		for j := range e.B2 {
			db2[j] += g[i][j]
			for k := range e.B1 {
				dw2[j][k] += g[i][j] * h[i][k]
				dh[k] += g[i][j] * e.W2[j][k]
			}
		}
		for k := range e.B1 {
			v := dh[k] * (1 - h[i][k]*h[i][k])
			db1[k] += v
			for j := range row {
				dw1[k][j] += v * row[j]
			}
		}
	}
	for i := range e.W1 {
		e.B1[i] -= lr * db1[i]
		for j := range e.W1[i] {
			e.W1[i][j] -= lr * dw1[i][j]
		}
	}
	for i := range e.W2 {
		e.B2[i] -= lr * db2[i]
		for j := range e.W2[i] {
			e.W2[i][j] -= lr * dw2[i][j]
		}
	}
}
func TrainEncoder(x [][]float64, seed uint32, regularized bool) (Encoder, []float64) {
	_, d := shape(x)
	e := NewEncoder(d, 16, 8, seed)
	dirs := Directions(8, 6, 101)
	rng := RNG{seed + 44}
	losses := []float64{}
	order := make([]int, len(x))
	for i := range order {
		order[i] = i
	}
	for epoch := 0; epoch < 8; epoch++ {
		shuffle(order, seed+uint32(epoch+1))
		total := 0.
		for start := 0; start < len(order); start += 64 {
			idx := order[start:min(start+64, len(order))]
			batch := Rows(x, idx)
			aug := clone(batch)
			for i := range aug {
				for j := range aug[i] {
					aug[i][j] += .02 * rng.Normal()
				}
			}
			h, z := e.Forward(batch)
			h2, z2 := e.Forward(aug)
			g, g2 := Zeros(len(z), 8), Zeros(len(z), 8)
			loss := 0.
			for i := range z {
				for j := range z[i] {
					diff := z[i][j] - z2[i][j]
					loss += diff * diff / float64(len(z)*8)
					g[i][j] = 2 * diff / float64(len(z)*8)
					g2[i][j] = -g[i][j]
				}
			}
			if regularized {
				p, pg := GaussianPenalty(z, dirs)
				loss += p
				for i := range g {
					for j := range g[i] {
						g[i][j] += pg[i][j]
					}
				}
			}
			joinedX := append(batch, aug...)
			joinedH := append(h, h2...)
			joinedG := append(g, g2...)
			e.Update(joinedX, joinedH, joinedG, .08)
			total += loss * float64(len(batch)) / float64(len(x))
		}
		losses = append(losses, total)
	}
	return e, losses
}
