package engine

import (
	"encoding/json"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
)

func corePoints(repo string) [][]float64 {
	x := Iris(repo)
	s := FitScaler(x[:90])
	return s.Transform(x[:24])
}
func square() [][]float64         { return [][]float64{{0, 0}, {1, 0}, {1, 1}, {0, 1}} }
func digit(repo string) []float64 { x, _, tr, _, _ := DigitData(repo); return x[tr[0]] }
func centroidBridge(repo string) map[string]any {
	x, _, _ := spl(repo)
	whole := MeanRows(x)
	a, b := MeanRows(x[:1]), MeanRows(x[1:])
	weighted, equal := make([]float64, 3), make([]float64, 3)
	for j := range whole {
		weighted[j] = (a[j] + float64(len(x)-1)*b[j]) / float64(len(x))
		equal[j] = (a[j] + b[j]) / 2
	}
	rev := clone(x)
	for i, j := 0, len(rev)-1; i < j; i, j = i+1, j-1 {
		rev[i], rev[j] = rev[j], rev[i]
	}
	return map[string]any{"rows": len(x), "centroid_m": whole, "weighted_centroid_m": weighted, "equal_chunk_centroid_m": equal, "equal_chunk_displacement_m": distance(whole, equal), "order_reversal_error": distance(whole, MeanRows(rev)), "scope": "selected nonuniform rows, not time average, release point, or static LiDAR scan"}
}
func whiten(x [][]float64) map[string]any {
	mu := MeanRows(x)
	cov := Cov(x)
	eig, v := EigenSym(cov)
	keep := []int{}
	for i, e := range eig {
		if e > 1e-8 {
			keep = append(keep, i)
		}
	}
	require(len(keep) > 0, "zero covariance rank")
	out := Zeros(len(x), len(keep))
	for i, row := range x {
		for q, k := range keep {
			for j := range row {
				out[i][q] += (row[j] - mu[j]) * v[j][k] / math.Sqrt(eig[k])
			}
		}
	}
	return map[string]any{"mean": mu, "covariance": cov, "eigenvalues": eig, "retained_components": keep, "whitened_covariance": Cov(out), "whitened": out, "scope": "nonzero covariance directions only; whitening is not Gaussianity or semantic quality"}
}
func representationTraining(repo string) map[string]any {
	x, y, tr, va, te := DigitData(repo)
	scaled := clone(x)
	for i := range scaled {
		for j := range scaled[i] {
			scaled[i][j] /= 16
		}
	}
	runs := []map[string]any{}
	for _, seed := range []uint32{11, 23} {
		for _, reg := range []bool{false, true} {
			e, h := TrainEncoder(Rows(scaled, tr), seed, reg)
			_, z := e.Forward(scaled)
			r := fitPredict(z, y, tr, va, te)
			r["seed"] = seed
			r["regularized"] = reg
			r["encoder_loss"] = h
			r["encoder_weights"] = e
			r["training_embedding_covariance"] = Cov(Rows(z, tr))
			runs = append(runs, r)
		}
	}
	return map[string]any{"train_rows": tr, "validation_rows": va, "test_rows": te, "pixel_baseline": fitPredict(x, y, tr, va, te), "runs": runs, "protocol": "native16 64-16-8 tanh encoder;8 epochs;batch64;SGD.08;fixed projected CF penalty;fixed linear probe", "scope": "new exposed image-level teaching protocol; not LeJEPA reproduction or athlete generalization"}
}
func lossControls() map[string]any {
	a := [][]float64{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	b := [][]float64{{.9, .1}, {.1, .9}, {-.9, -.1}, {-.1, -.9}}
	inv := 0.
	for i := range a {
		for j := range a[i] {
			inv += (a[i][j] - b[i][j]) * (a[i][j] - b[i][j]) / 8
		}
	}
	ca, cb := Cov(a), Cov(b)
	variance, covpen := 0., 0.
	for _, c := range [][][]float64{ca, cb} {
		for i := range c {
			variance += math.Max(0, 1-math.Sqrt(c[i][i]+1e-4)) / 4
			for j := range c {
				if i != j {
					covpen += c[i][j] * c[i][j] / 4
				}
			}
		}
	}
	zero := Zeros(8, 2)
	p, g := GaussianPenalty(zero, Directions(2, 4, 55))
	flat := []float64{}
	for _, row := range g {
		flat = append(flat, row...)
	}
	return map[string]any{"invariance_mse": inv, "variance_hinge": variance, "offdiagonal_covariance_penalty": covpen, "collapsed_projection_penalty": p, "collapsed_gradient_norm": norm(flat), "scope": "finite objective controls; positive penalty can have zero gradient at collapse"}
}
func Leakage(repo string) map[string]any {
	x, y, _ := ClassificationData(repo, "seeds")
	z := FitScaler(x).Transform(x)
	copies := [][]float64{}
	labels := []int{}
	g := []string{}
	for i := range z {
		for j := 0; j < 3; j++ {
			copies = append(copies, z[i])
			labels = append(labels, y[i])
			g = append(g, fmt.Sprint(i))
		}
	}
	idx := rangeInts(0, len(copies))
	shuffle(idx, 54)
	tr, te := idx[:len(idx)*7/10], idx[len(idx)*7/10:]
	gtr, _, gte := GroupSplit(g)
	score := func(a, b []int) map[string]any {
		p := []int{}
		overlap := 0
		set := map[string]bool{}
		for _, i := range a {
			set[g[i]] = true
		}
		for _, i := range b {
			best := a[0]
			for _, j := range a {
				if distance(copies[i], copies[j]) < distance(copies[i], copies[best]) {
					best = j
				}
			}
			p = append(p, labels[best])
			if set[g[i]] {
				overlap++
			}
		}
		return map[string]any{"test_rows": b, "predictions": p, "truth": Labels(labels, b), "accuracy": accuracy(Labels(labels, b), p), "shared_source_test_rows": overlap}
	}
	return map[string]any{"observed_kernels": len(x), "constructed_rows": len(copies), "row_split": score(tr, te), "source_group_split": score(gtr, gte), "scope": "intentional copied-row leakage demonstration; scaler fit globally to isolate duplication, not a valid evaluation protocol"}
}
func finiteTopologies() map[string]any {
	count := 0
	for family := 0; family < 256; family++ {
		if family&1 == 0 || family&128 == 0 {
			continue
		}
		good := true
		for a := 0; a < 8; a++ {
			if family&(1<<a) == 0 {
				continue
			}
			for b := 0; b < 8; b++ {
				if family&(1<<b) == 0 {
					continue
				}
				if family&(1<<(a|b)) == 0 || family&(1<<(a&b)) == 0 {
					good = false
				}
			}
		}
		if good {
			count++
		}
	}
	return map[string]any{"three_point_topologies": count, "domain": "all 256 candidate collections of subsets of a labeled three-element set", "identity_map_indiscrete_to_discrete_continuous": false, "identity_map_discrete_to_indiscrete_continuous": true}
}
func NativeLab(repo, key string) map[string]any {
	switch key {
	case "stage00":
		x, y, features := ClassificationData(repo, "seeds")
		uniq := map[string]bool{}
		counts := map[string]int{}
		for i, r := range x {
			uniq[vectorKey(r)] = true
			counts[strconv.Itoa(y[i])]++
		}
		return map[string]any{"observations": len(x), "features": features, "distinct_vectors": len(uniq), "label_counts": counts, "column_means": MeanRows(x), "scope": "observed kernels; feature rows are not photographs"}
	case "stage01":
		x := Iris(repo)
		centered := FitScaler(x).Transform(x)
		aug := clone(x)
		for i := range aug {
			aug[i] = append(aug[i], 2*x[i][0]-3*x[i][1])
		}
		a := [][]float64{{1, 1, 0}, {1, 0, 1}, {0, 1, 1}}
		return map[string]any{"real_rank": Rank(a, 1e-10), "f2_rank": Rank2(a), "iris_rank": Rank(x, 1e-10), "centered_scaled_rank": Rank(centered, 1e-10), "augmented_rank": Rank(aug, 1e-10), "known_kernel": []float64{-2, 3, 0, 0, 1}, "kernel_residual_max": maxAbs(MatVec(aug, []float64{-2, 3, 0, 0, 1})), "finite_preimage_of_square_1_to_9": []int{-3, -2, -1, 1, 2, 3}}
	case "stage02":
		x := corePoints(repo)
		radii := []float64{.2, .5, 1, 2}
		counts := []int{}
		for _, r := range radii {
			counts = append(counts, len(Components(x, r)))
		}
		d := [][]float64{}
		for i := 1; i < min(8, len(x)); i++ {
			diff := sub(x[0], x[i])
			l1, linf := 0., 0.
			for _, v := range diff {
				l1 += math.Abs(v)
				linf = math.Max(linf, math.Abs(v))
			}
			d = append(d, []float64{l1, norm(diff), linf})
		}
		return map[string]any{"radii": radii, "component_counts": counts, "distances_L1_L2_Linf": d, "squared_distance_counterexample": []float64{4, 1 + 1}, "scope": "scaled sample geometry, not biological topology proof"}
	case "stage03":
		out := finiteTopologies()
		x := Iris(repo)
		ids := map[string]bool{}
		for _, row := range x {
			ids[vectorKey(row[:2])] = true
		}
		out["projected_distinct_vectors"] = len(ids)
		out["original_rows"] = len(x)
		out["scope"] = "finite checks and a noninjective projection; not a general continuity theorem"
		return out
	case "stage04":
		p := digit(repo)
		rot := make([]float64, 64)
		for i := 0; i < 8; i++ {
			for j := 0; j < 8; j++ {
				rot[j*8+7-i] = p[i*8+j]
			}
		}
		return map[string]any{"rotation_pixel_distance": distance(p, rot), "original_betti": PixelBetti(p, 8, 8, 8), "rotated_betti": PixelBetti(rot, 8, 8, 8), "dihedral_square_group_size": 8, "scope": "rotation preserves this pixel-complex topology, not necessarily the digit class label"}
	case "stage06":
		out := AlgebraControl()
		out["observed_digit_diagram"] = Persistence(PixelFiltration(digit(repo), 8, 8))
		return out
	case "stage05":
		p := digit(repo)
		return map[string]any{"triangle_boundary_betti": Betti(Triangle(false)), "filled_triangle_betti": Betti(Triangle(true)), "tetrahedron_surface_betti": Betti(Tetra(false)), "filled_tetrahedron_betti": Betti(Tetra(true)), "real_digit_closed_pixel_betti": PixelBetti(p, 8, 8, 8), "real_digit_persistence": Persistence(PixelFiltration(p, 8, 8)), "coefficient_field": "F2", "scope": "explicit finite complexes and an observed image; interpretation requires pixel convention"}
	case "stage07":
		x := corePoints(repo)
		return map[string]any{"point_rows": len(x), "rips_diagram": ReportH01(Persistence(Rips(x, 1.5, 2))), "equilateral_side": 2, "cech_common_radius": 2 / math.Sqrt(3), "cech_pair_radius": 1, "rips_filled_triangle_edge_threshold": 2, "scope": "Rips plus exact Cech control; general alpha/Delaunay implementation remains in Python reference"}
	case "stage08", "stage09":
		x := corePoints(repo)
		return map[string]any{"square_diagram": ReportH01(Persistence(Rips(square(), 2, 2))), "data_diagram": ReportH01(Persistence(Rips(x, math.Inf(1), 2))), "independent_H0_mst": MST(x), "coefficient_field": "F2", "maximum_simplex_dimension": 2, "scope": "H0 and H1; unfilled top-dimensional classes not an H2 inference"}
	case "stage10":
		p := digit(repo)
		q := append([]float64(nil), p...)
		delta := 0.
		for i := range q {
			q[i] += .05 * math.Sin(float64(i))
			delta = math.Max(delta, math.Abs(q[i]-p[i]))
		}
		a, b := Persistence(PixelFiltration(p, 8, 8)), Persistence(PixelFiltration(q, 8, 8))
		d := []float64{}
		for k := 0; k < 2; k++ {
			d = append(d, Bottleneck(DiagramDimension(a, k), DiagramDimension(b, k)))
		}
		return map[string]any{"input_linf": delta, "bottleneck_by_dimension": d, "bound_holds": d[0] <= delta+1e-8 && d[1] <= delta+1e-8, "scope": "same pixel complex, sublevel functions of negative intensity; not arbitrary pipeline stability"}
	case "stage11":
		x := corePoints(repo)
		lens := []float64{}
		for _, r := range x {
			lens = append(lens, r[0])
		}
		return Mapper(x, lens, 5, .3, .5)
	case "stage12":
		return DigitCase(repo)
	case "stage13":
		errs := []float64{}
		coords := [][]float64{}
		for i := 0; i < 12; i++ {
			u, v := .1*float64(i), .3
			den := 1 + u*u + v*v
			p := []float64{2 * u / den, 2 * v / den, (u*u + v*v - 1) / den}
			q := []float64{p[0] / (1 - p[2]), p[1] / (1 - p[2])}
			errs = append(errs, distance([]float64{u, v}, q))
			coords = append(coords, p)
		}
		return map[string]any{"sphere_points": coords, "chart_roundtrip_errors": errs, "scope": "stereographic chart excludes north pole; camera projection is not such a chart"}
	case "stage14":
		q := []float64{math.Cos(.2), 0, 0, math.Sin(.2)}
		R := QuaternionMatrix(q)
		identity := MatMul(Transpose(R), R)
		cal := obj(ReadJSON(repo, "data/stereo/calibration.json"))
		p := []float64{.2, -.1, 3}
		f, cx, cy := num(cal["focal_px"]), num(cal["cx_left_px"]), num(cal["cy_px"])
		uv := []float64{f*p[0]/p[2] + cx, f*p[1]/p[2] + cy}
		back := []float64{(uv[0] - cx) * p[2] / f, (uv[1] - cy) * p[2] / f, p[2]}
		return map[string]any{"rotation": R, "RtR": identity, "pixel_uv": uv, "unprojected": back, "roundtrip_error": distance(p, back), "scope": "synthetic point with supplied camera intrinsics; depth is an input, not recovered from one pixel"}
	case "stage15":
		return Stereo(repo)
	case "stage16":
		x := corePoints(repo)[:6]
		scores := MatMul(x, Transpose(x))
		weights := make([][]float64, len(x))
		for i := range scores {
			for j := range scores[i] {
				scores[i][j] /= math.Sqrt(float64(len(x[0])))
			}
			weights[i] = softmax(scores[i])
		}
		return map[string]any{"attention_weights": weights, "attended_features": MatMul(weights, x), "scope": "native attention calculation, not pretrained VGGT inference"}
	case "stage17":
		return RegistrationControl()
	case "stage18", "poux_bridge":
		return centroidBridge(repo)
	case "stage19":
		return temporal()
	case "stage20":
		return map[string]any{"registration_control": RegistrationControl(), "sports_motion": Motion(repo), "source_coordinates": "separate controls; no forced alignment between these objects", "scope": "spatial-capstone prerequisites, not an independently acquired reconstruction"}
	case "stage21":
		out := RegressionCase(repo, "hahn1")
		err := []float64{}
		for _, h := range []float64{.1, .01, .001} {
			d := (math.Sin(.4+h) - math.Sin(.4-h)) / (2 * h)
			err = append(err, math.Abs(d-math.Cos(.4)))
		}
		out["manufactured_derivative_errors"] = err
		return out
	case "stage22":
		x, t := .2, 2.
		y := x / (1 - t*x)
		back := y / (1 + t*y)
		return map[string]any{"initial": x, "time": t, "flow": y, "inverse": back, "finite_blowup_time": 1 / x, "scope": "x'=x² exact local flow, defined only before blowup"}
	case "stage23":
		return map[string]any{"hnn": TrainPhysics("hnn"), "lnn_restricted": TrainPhysics("lnn")}
	case "stage24":
		return Integrators()
	case "stage25":
		return ConstraintControl()
	case "stage26":
		return TrainPhysics("pinn")
	case "stage27":
		return GradientControl()
	case "stage28":
		return map[string]any{"deeponet": trainOperator("deeponet"), "spectral_operator": trainOperator("fno")}
	case "stage29":
		return map[string]any{"differentiable_scalar_flow_fit": dampingFit(), "row_stochastic_matrix": [][]float64{{1, 0}, {1, 0}}, "input": []float64{1, 3}, "output": []float64{1, 1}, "input_sum": 4, "output_sum": 2, "scope": "row-stochastic attention alone is not a mass-conservation law"}
	case "stage30":
		return map[string]any{"native_training": dampingFit(), "nonlinear_constraint": ConstraintControl(), "requirement": "independent observed-system capstone still required", "scope": "manufactured verification controls do not validate a physical world model"}
	case "wine", "wdbc", "seeds":
		return Classification(repo, key)
	case "stackloss", "concrete_slump":
		return RegressionCase(repo, key)
	case "co2", "nile", "elnino":
		return TimeCase(repo, key)
	case "grunfeld":
		return Grunfeld(repo)
	case "modechoice":
		return ModeChoice(repo)
	case "leakage":
		return Leakage(repo)
	case "claims":
		return map[string]any{"integration": Integrators(), "projection": ConstraintControl(), "gradient_conflicts": GradientControl()}
	case "s00":
		x, t, _ := spl(repo)
		return map[string]any{"centroid_m": MeanRows(x), "selected_frames": len(x), "independent_trials": 1, "time_seconds": t, "landing_offset_m": []float64{num(obj(ReadJSON(repo, "sports_v8/data/spl_selected_frames.json"))["landing_x"]) * .0254, num(obj(ReadJSON(repo, "sports_v8/data/spl_selected_frames.json"))["landing_y"]) * .0254}, "scope": "mixed units converted, selected observations remain one trial"}
	case "s01":
		return Motion(repo)
	case "s02":
		return Flight(repo)
	case "s03":
		return Profile(repo, true)
	case "s04":
		x, t, _ := spl(repo)
		values := []map[string]any{}
		for i := 0; i < 6; i++ {
			query := float64(i) * .5
			last := -1
			for j, tm := range t {
				if tm <= query {
					last = j
				}
			}
			if last >= 0 {
				values = append(values, map[string]any{"time": query, "source_row": last, "age": query - t[last], "position_m": x[last]})
			}
		}
		return map[string]any{"past_only_holds": values, "scope": "zero-order hold labels age and does not interpolate future measurements"}
	case "s05":
		return Profile(repo, false)
	case "s06":
		return map[string]any{"observations": Motion(repo), "flight_diagnostic": Flight(repo), "protocol_requirement": "new independent athlete/session measurements and event labels", "scope": "no held-out athlete benchmark in the excerpt"}
	case "acb":
		return ACB(repo)
	case "r01":
		return whiten(Iris(repo)[:90])
	case "r02":
		rng := RNG{7}
		z := Zeros(128, 4)
		for i := range z {
			for j := range z[i] {
				z[i][j] = rng.Normal()
			}
		}
		dirs := Directions(4, 16, 11)
		loss, g := GaussianPenalty(z, dirs)
		collapsed := Zeros(128, 4)
		cl, cg := GaussianPenalty(collapsed, dirs)
		return map[string]any{"normal_control_penalty": loss, "normal_control_gradient_first_row": g[0], "collapsed_penalty": cl, "collapsed_gradient_first_row": cg[0], "scope": "finite-frequency/projection diagnostics, not proof of multivariate Gaussianity"}
	case "r03":
		return lossControls()
	case "r04":
		return representationTraining(repo)
	case "r05":
		rows, x, _ := profileRows(repo)
		g := []string{}
		j := column(rows[0], "player_id")
		for _, r := range rows[1:] {
			g = append(g, r[j])
		}
		tr, va, te := GroupSplit(g)
		out := whiten(Rows(x, tr))
		out["train_rows"] = tr
		out["validation_rows"] = va
		out["test_rows"] = te
		out["scope"] = "training-group covariance only, small selected profiles; no semantic validation"
		return out
	}
	panic("unknown native lab: " + key)
}
func maxAbs(v []float64) float64 {
	m := 0.
	for _, x := range v {
		m = math.Max(m, math.Abs(x))
	}
	return m
}
func LabKeys(repo string) []string {
	m := obj(ReadJSON(repo, "native/protocols/labs.json"))
	out := []string{}
	for _, v := range arr(m["labs"]) {
		out = append(out, obj(v)["key"].(string))
	}
	sort.Strings(out)
	return out
}
func Run(repo, key string) (result map[string]any, err error) {
	defer func() {
		if v := recover(); v != nil {
			err = fmt.Errorf("%v", v)
			result = nil
		}
	}()
	BeginAudit()
	keys := LabKeys(repo)
	found := false
	for _, k := range keys {
		if key == k {
			found = true
		}
	}
	require(found, "unknown native lab")
	metrics := NativeLab(repo, key)
	_, e := json.Marshal(metrics)
	require(e == nil, "nonfinite or unsupported result")
	return map[string]any{"schema": "shape.native.v16", "lab": key, "language": "go", "implementation": "native; no Python calls or reference-result reads", "protocol": "native16 shared teaching adaptation", "metrics": metrics, "original_notebook_parity": "not_certified; see native/COVERAGE.md", "status": "completed", "inputs": InputAudit()}, nil
}

var _ = strings.Compare
