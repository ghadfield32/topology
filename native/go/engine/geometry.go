package engine

import (
	"math"
	"sort"
)

func cross(a, b []float64) []float64 {
	require(len(a) == 3 && len(b) == 3, "cross requires 3-vectors")
	return []float64{a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]}
}
func RotateZ(x []float64, a float64) []float64 {
	require(len(x) == 3, "3D point required")
	c, s := math.Cos(a), math.Sin(a)
	return []float64{c*x[0] - s*x[1], s*x[0] + c*x[1], x[2]}
}
func angle(a, b, c []float64) float64 {
	u, v := sub(a, b), sub(c, b)
	n := norm(u) * norm(v)
	require(n > 1e-15, "degenerate joint angle")
	return math.Acos(math.Max(-1, math.Min(1, dot(u, v)/n))) * 180 / math.Pi
}
func spl(repo string) ([][]float64, []float64, []map[string]any) {
	j := obj(ReadJSON(repo, "sports_v8/data/spl_selected_frames.json"))
	require(j["xyz_unit"] == "ft", "SPL feet convention changed")
	fps := num(j["sampling_rate"])
	require(fps > 0, "invalid sampling rate")
	x := [][]float64{}
	ts := []float64{}
	records := []map[string]any{}
	for _, r := range arr(j["records"]) {
		m := obj(r)
		p := fvec(m["ball"])
		require(len(p) == 3, "ball vector")
		for i := range p {
			p[i] *= .3048
		}
		x = append(x, p)
		ts = append(ts, num(m["frame"])/fps)
		records = append(records, m)
	}
	for i := 1; i < len(ts); i++ {
		require(ts[i] > ts[i-1], "nonincreasing timestamps")
	}
	return x, ts, records
}
func Stereo(repo string) map[string]any {
	left := ReadPNG(repo, "data/stereo/left.png")
	right := ReadPNG(repo, "data/stereo/right.png")
	ref := ReadNPZ(repo, "data/stereo/motorcycle.npz")["disparity_px"]
	cal := obj(ReadJSON(repo, "data/stereo/calibration.json"))
	h, w := left.Shape[0], left.Shape[1]
	require(right.Shape[0] == h && right.Shape[1] == w && left.Shape[2] == 3 && right.Shape[2] == 3, "stereo shape mismatch")
	gray := func(a Array) []float64 {
		v := make([]float64, h*w)
		for i := range v {
			v[i] = (a.Data[3*i] + a.Data[3*i+1] + a.Data[3*i+2]) / 3
		}
		return v
	}
	l, r := gray(left), gray(right)
	obs := []map[string]any{}
	errors, depthErrors := []float64{}, []float64{}
	requested := 0
	for y := 30; y < h-30; y += 55 {
		for x := 110; x < w-30; x += 61 {
			requested++
			truth := ref.Data[y*w+x]
			if !finite(truth) || truth+num(cal["doffs_px"]) <= 0 {
				continue
			}
			best, bestD := math.Inf(1), 0
			for d := 0; d <= 90; d++ {
				cost := 0.
				for dy := -2; dy <= 2; dy++ {
					for dx := -2; dx <= 2; dx++ {
						cost += math.Abs(l[(y+dy)*w+x+dx] - r[(y+dy)*w+x-d+dx])
					}
				}
				if cost < best {
					best = cost
					bestD = d
				}
			}
			pred := float64(bestD)
			factor := num(cal["focal_px"]) * num(cal["baseline_m"])
			z := factor / (pred + num(cal["doffs_px"]))
			zt := factor / (truth + num(cal["doffs_px"]))
			errors = append(errors, math.Abs(pred-truth))
			depthErrors = append(depthErrors, math.Abs(z-zt))
			obs = append(obs, map[string]any{"u": x, "v": y, "truth_disparity_px": truth, "predicted_disparity_px": pred, "truth_depth_m": zt, "predicted_depth_m": z})
		}
	}
	bad := 0
	for _, e := range errors {
		if e > 2 {
			bad++
		}
	}
	return map[string]any{"requested_pixels": requested, "eligible_pixels": len(obs), "patch_width": 5, "max_disparity_px": 90, "disparity_mae_px": Mean(errors), "disparity_median_abs_px": median(errors), "bad_over_2px_fraction": float64(bad) / float64(len(errors)), "depth_mae_m": Mean(depthErrors), "predictions": obs, "convention": "Z=fB/(d+doffs); rectified positive optical-axis depth", "scope": "fixed selected pixels, not full-image or camera-calibration validation"}
}
func QuaternionMatrix(q []float64) [][]float64 {
	require(len(q) == 4, "quaternion shape")
	n := norm(q)
	require(n > 1e-14, "zero quaternion")
	w, x, y, z := q[0]/n, q[1]/n, q[2]/n, q[3]/n
	return [][]float64{{1 - 2*(y*y+z*z), 2 * (x*y - z*w), 2 * (x*z + y*w)}, {2 * (x*y + z*w), 1 - 2*(x*x+z*z), 2 * (y*z - x*w)}, {2 * (x*z - y*w), 2 * (y*z + x*w), 1 - 2*(x*x+y*y)}}
}
func Register(a, b [][]float64) (float64, [][]float64, []float64) {
	n, d := shape(a)
	nb, db := shape(b)
	require(n == nb && d == 3 && db == 3 && n >= 3, "paired 3D registration input")
	ma, mb := MeanRows(a), MeanRows(b)
	s := Zeros(3, 3)
	energy := 0.
	for i := range a {
		u, v := sub(a[i], ma), sub(b[i], mb)
		energy += dot(u, u)
		for j := 0; j < 3; j++ {
			for k := 0; k < 3; k++ {
				s[j][k] += u[j] * v[k]
			}
		}
	}
	require(energy > 1e-12, "degenerate registration")
	xx, xy, xz := s[0][0], s[0][1], s[0][2]
	yx, yy, yz := s[1][0], s[1][1], s[1][2]
	zx, zy, zz := s[2][0], s[2][1], s[2][2]
	N := [][]float64{{xx + yy + zz, yz - zy, zx - xz, xy - yx}, {yz - zy, xx - yy - zz, xy + yx, zx + xz}, {zx - xz, xy + yx, -xx + yy - zz, yz + zy}, {xy - yx, zx + xz, yz + zy, -xx - yy + zz}}
	_, V := EigenSym(N)
	q := []float64{V[0][0], V[1][0], V[2][0], V[3][0]}
	R := QuaternionMatrix(q)
	score := 0.
	for i := range a {
		score += dot(sub(b[i], mb), MatVec(R, sub(a[i], ma)))
	}
	scale := score / energy
	require(scale > 0, "nonpositive similarity scale")
	t := sub(mb, MatVec(R, ma))
	for i := range t {
		t[i] = mb[i] - scale*MatVec(R, ma)[i]
	}
	return scale, R, t
}
func RegistrationControl() map[string]any {
	rng := RNG{34}
	a, b := [][]float64{}, [][]float64{}
	for i := 0; i < 24; i++ {
		p := []float64{rng.Normal(), rng.Normal(), rng.Normal()}
		q := RotateZ(p, .4)
		for j := range q {
			q[j] = 2.5*q[j] + []float64{3, -2, 1}[j]
		}
		a = append(a, p)
		b = append(b, q)
	}
	s, R, t := Register(a[:12], b[:12])
	errors := []float64{}
	for i := 12; i < len(a); i++ {
		p := MatVec(R, a[i])
		for j := range p {
			p[j] = s*p[j] + t[j]
		}
		errors = append(errors, distance(p, b[i]))
	}
	return map[string]any{"scale": s, "rotation": R, "translation": t, "fit_indices": rangeInts(0, 12), "holdout_indices": rangeInts(12, 24), "holdout_errors": errors, "max_holdout_error": maxFloat(errors), "origin": "manufactured paired nondegenerate cloud; not a learned reconstruction"}
}
func maxFloat(a []float64) float64 {
	require(len(a) > 0, "empty maximum")
	v := a[0]
	for _, x := range a {
		v = math.Max(v, x)
	}
	return v
}
func rangeInts(a, b int) []int {
	r := []int{}
	for i := a; i < b; i++ {
		r = append(r, i)
	}
	return r
}
func Flight(repo string) map[string]any {
	x, t, _ := spl(repo)
	ids := []int{3, 4, 5, 6, 7}
	hold := []int{8, 9}
	base := t[ids[0]]
	A := Zeros(len(ids), 3)
	y := make([]float64, len(ids))
	for i, k := range ids {
		dt := t[k] - base
		A[i] = []float64{1, dt, dt * dt}
		y[i] = x[k][2]
	}
	ATA := MatMul(Transpose(A), A)
	w := Solve(ATA, MatVec(Transpose(A), y))
	p, truth := []float64{}, []float64{}
	for _, k := range hold {
		dt := t[k] - base
		p = append(p, dot(w, []float64{1, dt, dt * dt}))
		truth = append(truth, x[k][2])
	}
	fixed := Zeros(len(ids), 2)
	yf := make([]float64, len(ids))
	for i, k := range ids {
		dt := t[k] - base
		fixed[i] = []float64{1, dt}
		yf[i] = y[i] + .5*9.80665*dt*dt
	}
	wf := Solve(MatMul(Transpose(fixed), fixed), MatVec(Transpose(fixed), yf))
	pf, pc := []float64{}, []float64{}
	for _, k := range hold {
		dt := t[k] - base
		pf = append(pf, wf[0]+wf[1]*dt-.5*9.80665*dt*dt)
		pc = append(pc, Mean(y))
	}
	return map[string]any{"fit_rows": ids, "later_same_trial_rows": hold, "coefficients": w, "fitted_acceleration_m_s2": 2 * w[2], "truth": truth, "quadratic_predictions": p, "quadratic_mae_m": MAE(truth, p), "fixed_gravity_predictions": pf, "fixed_gravity_mae_m": MAE(truth, pf), "constant_predictions": pc, "constant_mae_m": MAE(truth, pc), "scope": "selected frames, no release annotation and no independent athlete test"}
}
func Motion(repo string) map[string]any {
	x, t, rs := spl(repo)
	angles := []float64{}
	vel := []map[string]any{}
	for _, r := range rs {
		angles = append(angles, angle(fvec(r["right_shoulder"]), fvec(r["right_elbow"]), fvec(r["right_wrist"])))
	}
	for i := 1; i < len(x); i++ {
		dt := t[i] - t[i-1]
		if dt > .1 {
			vel = append(vel, map[string]any{"row": i, "valid": false, "reason": "gap exceeds 0.1 seconds"})
			continue
		}
		v := sub(x[i], x[i-1])
		for j := range v {
			v[j] /= dt
		}
		vel = append(vel, map[string]any{"row": i, "valid": true, "velocity_m_s": v, "dt": dt})
	}
	return map[string]any{"joint_angles_deg": angles, "interval_velocities": vel, "time_seconds": t, "scope": "interval estimates on selected samples; not camera PTS or ground-truth release"}
}
func Integrators() map[string]any {
	methods := []string{"explicit_euler", "symplectic_euler", "verlet", "implicit_midpoint", "rk4"}
	out := map[string]any{}
	dt := .05
	n := 400
	for _, method := range methods {
		q, p := 1., 0.
		trace := [][]float64{{0, q, p, .5}}
		maxErr := 0.
		for i := 0; i < n; i++ {
			switch method {
			case "explicit_euler":
				q, p = q+dt*p, p-dt*q
			case "symplectic_euler":
				p -= dt * q
				q += dt * p
			case "verlet":
				p -= dt * q / 2
				q += dt * p
				p -= dt * q / 2
			case "implicit_midpoint":
				den := 1 + dt*dt/4
				q, p = ((1-dt*dt/4)*q+dt*p)/den, ((1-dt*dt/4)*p-dt*q)/den
			case "rk4":
				a, b := q, p
				aq, ap := b, -a
				bq, bp := b+dt*ap/2, -(a + dt*aq/2)
				cq, cp := b+dt*bp/2, -(a + dt*bq/2)
				dq, dp := b+dt*cp, -(a + dt*cq)
				q += dt * (aq + 2*bq + 2*cq + dq) / 6
				p += dt * (ap + 2*bp + 2*cp + dp) / 6
			}
			energy := (q*q + p*p) / 2
			maxErr = math.Max(maxErr, math.Abs(energy-.5))
			if i%10 == 9 {
				trace = append(trace, []float64{float64(i+1) * dt, q, p, energy})
			}
		}
		out[method] = map[string]any{"max_energy_error": maxErr, "state_error": math.Hypot(q-math.Cos(float64(n)*dt), p+math.Sin(float64(n)*dt)), "trace": trace}
	}
	out["symplectic_one_step_control"] = map[string]any{"dt": .2, "q": .96, "p": -.2, "energy": .4808}
	return out
}
func ConstraintControl() map[string]any {
	x := []float64{2, 0}
	res := []float64{}
	trajectory := [][]float64{append([]float64(nil), x...)}
	for i := 0; i < 7; i++ {
		c := dot(x, x) - 1
		den := 4 * dot(x, x)
		require(den > 1e-14, "singular constraint Jacobian")
		for j := range x {
			x[j] -= 2 * x[j] * c / den
		}
		res = append(res, dot(x, x)-1)
		trajectory = append(trajectory, append([]float64(nil), x...))
	}
	return map[string]any{"constraint_residuals": res, "trajectory": trajectory, "first_residual": res[0], "scope": "Newton-like normal corrections, not an exact one-step projection or a geodesic"}
}
func GradientControl() map[string]any {
	gs := [][]float64{{1, 0}, {-.4, 1}, {.2, -.6}}
	out := [][]float64{}
	for i, g := range gs {
		v := append([]float64(nil), g...)
		for j, h := range gs {
			if i != j && dot(v, h) < 0 {
				f := dot(v, h) / dot(h, h)
				for k := range v {
					v[k] -= f * h[k]
				}
			}
		}
		out = append(out, v)
	}
	normed := clone(out)
	for i := range normed {
		n := norm(normed[i])
		if n > 1e-12 {
			for j := range normed[i] {
				normed[i][j] /= n
			}
		}
	}
	return map[string]any{"input_gradients": gs, "projected_gradients": out, "mean_projected": MeanRows(out), "mean_normalized_after_projection": MeanRows(normed), "opposite_gradients": [][]float64{{1, 0}, {-1, 0}}, "zero_sum": []float64{0, 0}, "scope": "ordered gradient operations, not a reproduction of full domain-decomposition benchmarks"}
}
func temporal() map[string]any {
	d := []float64{.04, .05, .06, .2, .3, .4, .1}
	visible := []bool{true, true, true, true, false, true, true}
	events := []int{}
	for i := 2; i < len(d); i++ {
		if visible[i] && visible[i-1] && d[i] > .15 && d[i-1] > .15 && d[i-2] <= .15 {
			events = append(events, i)
		}
	}
	return map[string]any{"distance_m": d, "visible": visible, "confirmed_candidate_frames": events, "scope": "manufactured thresholds; proximity is not contact, gaps break confirmation"}
}
func profileRows(repo string) ([][]string, [][]float64, []string) {
	rows := ReadCSV(repo, "sports_v8/data/skillcorner_selected_profiles.csv", ',')
	cols := []string{"total_distance_full_all", "total_metersperminute_full_all", "running_distance_full_all", "hsr_distance_full_all", "sprint_distance_full_all"}
	x, idx := numeric(rows, cols)
	require(len(idx) == len(rows)-1, "unexpected missing profile fields")
	return rows, x, cols
}
func GroupSplit(groups []string) ([]int, []int, []int) {
	uniq := map[string]bool{}
	for _, g := range groups {
		uniq[g] = true
	}
	keys := sortedKeys(uniq)
	order := rangeInts(0, len(keys))
	shuffle(order, 73)
	bucket := map[string]int{}
	for i, j := range order {
		b := 0
		if i >= len(keys)*8/10 {
			b = 2
		} else if i >= len(keys)*6/10 {
			b = 1
		}
		bucket[keys[j]] = b
	}
	tr, va, te := []int{}, []int{}, []int{}
	for i, g := range groups {
		switch bucket[g] {
		case 0:
			tr = append(tr, i)
		case 1:
			va = append(va, i)
		case 2:
			te = append(te, i)
		}
	}
	return tr, va, te
}
func Profile(repo string, topology bool) map[string]any {
	rows, x, cols := profileRows(repo)
	groups := []string{}
	j := column(rows[0], "player_id")
	for _, row := range rows[1:] {
		groups = append(groups, row[j])
	}
	tr, va, te := GroupSplit(groups)
	s := FitScaler(Rows(x, tr))
	z := s.Transform(x)
	out := map[string]any{"features": cols, "train_rows": tr, "validation_rows": va, "test_rows": te, "athlete_ids": groups, "train_scaler_mean": s.Mean, "train_scaler_scale": s.Scale, "scaled_profiles": z, "scope": "selected season profiles, not chronological tracks or a representative player ranking"}
	if topology {
		out["diagram"] = ReportH01(Persistence(Rips(z, math.Inf(1), 2)))
		out["mst_edges"] = MST(z)
	}
	return out
}
func ACB(repo string) map[string]any {
	a := arr(ReadJSON(repo, "sports_v9/data/matches.json"))
	sort.SliceStable(a, func(i, j int) bool { return obj(a[i])["date_time"].(string) < obj(a[j])["date_time"].(string) })
	ids, scores := []int{}, []float64{}
	homeWins := 0
	for _, v := range a {
		o := obj(v)
		ids = append(ids, int(num(o["id"])))
		scores = append(scores, num(o["home_score"])+num(o["away_score"]))
		if num(o["home_score"]) > num(o["away_score"]) {
			homeWins++
		}
	}
	return map[string]any{"chronological_match_ids": ids, "train_match_ids": ids[:6], "validation_match_ids": ids[6:8], "test_match_ids": ids[8:], "total_points": scores, "home_wins": homeWins, "mean_total_points": Mean(scores), "scope": "ten selected metadata records, not all-season tracking or forecasting"}
}
