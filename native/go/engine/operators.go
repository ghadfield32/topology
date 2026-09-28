package engine

import "math"

func tapeNet(t *Tape, p []int, x []float64, h, o int) []int {
	d := len(x)
	require(len(p) == h*d+h+o*h+o, "network parameter dimensions")
	a := make([]int, h)
	for j := 0; j < h; j++ {
		s := p[h*d+j]
		for k, v := range x {
			s = t.Add(s, t.Scale(p[j*d+k], v))
		}
		a[j] = t.Tanh(s)
	}
	out := make([]int, o)
	start := h*d + h
	for j := 0; j < o; j++ {
		s := p[start+o*h+j]
		for k := 0; k < h; k++ {
			s = t.Add(s, t.Mul(p[start+j*h+k], a[k]))
		}
		out[j] = s
	}
	return out
}
func trainOperator(kind string) map[string]any {
	rng := RNG{99}
	sensors := 8
	inputs := [][]float64{}
	coeffs := [][]float64{}
	for n := 0; n < 24; n++ {
		c := []float64{rng.Normal(), rng.Normal() * .5, rng.Normal() * .25}
		v := make([]float64, sensors)
		for j := range v {
			x := float64(j) / float64(sensors)
			for k, a := range c {
				v[j] += a * math.Sin(2*math.Pi*float64(k+1)*x)
			}
		}
		inputs = append(inputs, v)
		coeffs = append(coeffs, c)
	}
	truth := func(c []float64, x float64) float64 {
		v := 0.
		for k, a := range c {
			freq := 2 * math.Pi * float64(k+1)
			v += a * math.Exp(-.005*freq*freq) * math.Sin(freq*x)
		}
		return v
	}
	nb := 8*8 + 8 + 4*8 + 4
	nt := 8 + 8 + 4*8 + 4
	nparams := nb + nt
	if kind == "fno" {
		nparams = 4
	}
	w := make([]float64, nparams)
	for i := range w {
		w[i] = .2 * rng.Normal()
	}
	predict := func(t *Tape, p []int, input []float64, x float64) int {
		if kind == "deeponet" {
			b := tapeNet(t, p[:nb], input, 8, 4)
			tr := tapeNet(t, p[nb:], []float64{x}, 8, 4)
			v := t.Input(0)
			for k := range b {
				v = t.Add(v, t.Mul(b[k], tr[k]))
			}
			return v
		}
		v := p[3]
		for k := 1; k <= 3; k++ {
			re, im := 0., 0.
			for j, u := range input {
				angle := 2 * math.Pi * float64(k*j) / float64(len(input))
				re += u * math.Cos(angle) / float64(len(input))
				im -= u * math.Sin(angle) / float64(len(input))
			}
			basis := 2 * (re*math.Cos(2*math.Pi*float64(k)*x) - im*math.Sin(2*math.Pi*float64(k)*x))
			v = t.Add(v, t.Scale(p[k-1], basis))
		}
		return v
	}
	history := []float64{}
	epochs := 80
	lr := .03
	for ep := 0; ep < epochs; ep++ {
		t := NewTape()
		p := make([]int, len(w))
		for i, v := range w {
			p[i] = t.Input(v)
		}
		loss := t.Input(0)
		for n := 0; n < 16; n++ {
			for j := 0; j < 8; j++ {
				x := float64(j) / 8
				v := predict(t, p, inputs[n], x)
				e := t.Sub(v, t.Input(truth(coeffs[n], x)))
				loss = t.Add(loss, t.Scale(t.Mul(e, e), 1./128))
			}
		}
		history = append(history, t.Val(loss))
		g := t.Back(loss)
		gn := 0.
		for _, i := range p {
			gn += g[i] * g[i]
		}
		factor := 1.
		if math.Sqrt(gn) > 10 {
			factor = 10 / math.Sqrt(gn)
		}
		for i, k := range p {
			w[i] -= lr * factor * g[k]
		}
	}
	actual, pred := []float64{}, []float64{}
	for n := 16; n < 24; n++ {
		for j := 0; j < 16; j++ {
			x := float64(j) / 16
			t := NewTape()
			p := make([]int, len(w))
			for i, v := range w {
				p[i] = t.Input(v)
			}
			pred = append(pred, t.Val(predict(t, p, inputs[n], x)))
			actual = append(actual, truth(coeffs[n], x))
		}
	}
	scope := "two trained tanh branch/trunk networks"
	if kind == "fno" {
		scope = "single learned real spectral multiplier layer; not a multilayer FNO benchmark"
	}
	return map[string]any{"model": kind, "origin": "manufactured periodic heat equation, diffusion*time=0.005", "train_function_ids": rangeInts(0, 16), "test_function_ids": rangeInts(16, 24), "epochs": epochs, "loss_history": history, "truth": actual, "predictions": pred, "rmse": RMSE(actual, pred), "weights": w, "scope": scope}
}
func dampingFit() map[string]any {
	trueGamma := .3
	dt := .05
	observed := make([]float64, 41)
	for i := range observed {
		observed[i] = math.Exp(-trueGamma * float64(i) * dt)
	}
	gamma := 1.
	hist := []float64{}
	for it := 0; it < 100; it++ {
		t := NewTape()
		g := t.Input(gamma)
		state := t.Input(1)
		loss := t.Input(0)
		for i := 1; i < len(observed); i++ {
			state = t.Mul(state, t.Exp(t.Scale(g, -dt)))
			e := t.Sub(state, t.Input(observed[i]))
			loss = t.Add(loss, t.Scale(t.Mul(e, e), 1/40.))
		}
		hist = append(hist, t.Val(loss))
		grad := t.Back(loss)
		gamma -= .2 * grad[g]
	}
	return map[string]any{"origin": "manufactured exact damped scalar flow", "true_gamma": trueGamma, "fitted_gamma": gamma, "loss_history": hist, "observations": observed, "time_step": dt, "scope": "no noisy real-system parameter-identification claim"}
}
