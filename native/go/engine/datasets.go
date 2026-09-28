package engine

import (
	"fmt"
	"math"
	"sort"
	"strconv"
)

func Iris(repo string) [][]float64 {
	r := ReadCSV(repo, "data/raw/iris.csv", ',')
	x, _ := numeric(r, []string{"sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm"})
	return x
}
func ClassificationData(repo, id string) ([][]float64, []int, []string) {
	path := "data/industries/" + id + "/data.csv"
	label := "label"
	start := 1
	if id == "seeds" {
		path = "data/v7/seeds/table.csv"
		label = "variety"
	}
	rows := ReadCSV(repo, path, ',')
	target := column(rows[0], label)
	features := []string{}
	for j := start; j < target; j++ {
		features = append(features, rows[0][j])
	}
	x, idx := numeric(rows, features)
	require(len(idx) == len(rows)-1, "classification missing values require explicit policy")
	y := make([]int, len(x))
	for i := range y {
		v, e := strconv.Atoi(rows[i+1][target])
		require(e == nil, "invalid classification label")
		y[i] = v
	}
	return x, y, features
}
func Classification(repo, id string) map[string]any {
	x, y, features := ClassificationData(repo, id)
	tr, va, te := Stratified(y, 42)
	raw := fitPredict(x, y, tr, va, te)
	s := FitScaler(Rows(x, tr))
	z := s.Transform(x)
	nref := min(24, len(tr)/3)
	refs := Rows(z, tr[:nref])
	supervised := tr[nref:]
	require(len(supervised) > 0, "not enough nonreference training rows")
	tf := make([][]float64, len(x))
	for i := range x {
		tf[i] = TopoFeature(z[i], refs)
	}
	combo := clone(x)
	for i := range combo {
		combo[i] = append(combo[i], tf[i]...)
	}
	return map[string]any{"features": features, "train_rows": tr, "validation_rows": va, "test_rows": te, "fixed_reference_rows": tr[:nref], "supervised_rows": supervised, "raw_all_training": raw, "raw_same_supervised_rows": fitPredict(x, y, supervised, va, te), "topology": fitPredict(tf, y, supervised, va, te), "combined": fitPredict(combo, y, supervised, va, te), "topological_features": tf, "protocol": "native-16: stratified xorshift split; fixed unlabelled training reference; softmax GD,160 epochs,lr=.15,L2=.01", "scope": "new common native protocol, not the original scikit-learn optimizer/protocol"}
}
func DigitData(repo string) ([][]float64, []int, []int, []int, []int) {
	a := ReadNPZ(repo, "data/raw/digits.npz")
	im := a["images"]
	labels := a["labels"]
	require(len(im.Shape) == 3 && im.Shape[1] == 8 && im.Shape[2] == 8, "digit image contract")
	x := Zeros(im.Shape[0], 64)
	y := make([]int, len(x))
	for i := range x {
		copy(x[i], im.Data[i*64:(i+1)*64])
		y[i] = int(labels.Data[i])
	}
	sp := obj(ReadJSON(repo, "data/splits.json"))
	convert := func(v any) []int {
		a := arr(v)
		out := make([]int, len(a))
		for i, x := range a {
			out[i] = int(num(x))
		}
		return out
	}
	return x, y, convert(sp["train"]), convert(sp["validation"]), convert(sp["test"])
}
func DigitFeatures(x [][]float64) [][]float64 {
	o := make([][]float64, len(x))
	for i, p := range x {
		v := []float64{}
		for _, threshold := range []float64{4, 8, 12} {
			b := PixelBetti(p, 8, 8, threshold)
			v = append(v, float64(b[0]), float64(b[1]))
		}
		v = append(v, Mean(p))
		o[i] = v
	}
	return o
}
func DigitCase(repo string) map[string]any {
	x, y, tr, va, te := DigitData(repo)
	tf := DigitFeatures(x)
	combo := clone(x)
	for i := range combo {
		combo[i] = append(combo[i], tf[i]...)
	}
	return map[string]any{"train_rows": tr, "validation_rows": va, "test_rows": te, "raw": fitPredict(x, y, tr, va, te), "topology": fitPredict(tf, y, tr, va, te), "combined": fitPredict(combo, y, tr, va, te), "topology_definition": "closed-pixel Betti0/1 at 4,8,12 plus mean intensity", "scope": "native softmax protocol on supplied exposed per-image partition; writer IDs unavailable"}
}
func RegressionCase(repo, id string) map[string]any {
	path := "data/industries/" + id + "/data.csv"
	features := []string{"AIRFLOW", "WATERTEMP", "ACIDCONC"}
	target := "STACKLOSS"
	if id == "concrete_slump" {
		path = "data/v7/concrete_slump/table.csv"
		features = []string{"cement_kg_m3", "slag_kg_m3", "fly_ash_kg_m3", "water_kg_m3", "sp_kg_m3", "coarse_aggregate_kg_m3", "fine_aggregate_kg_m3"}
		target = "strength_mpa"
	}
	if id == "hahn1" {
		path = "data/physics/hahn1_excerpt.csv"
		features = []string{"temperature_K"}
		target = "expansion_response"
	}
	rows := ReadCSV(repo, path, ',')
	all := append(append([]string(nil), features...), target)
	values, idx := numeric(rows, all)
	require(len(idx) == len(rows)-1, "unexpected missing regression data")
	x := make([][]float64, len(values))
	y := make([]float64, len(values))
	for i, r := range values {
		x[i] = r[:len(features)]
		y[i] = r[len(features)]
	}
	ids := rangeInts(0, len(x))
	shuffle(ids, 53)
	n1, n2 := len(ids)*6/10, len(ids)*8/10
	if id == "concrete_slump" {
		n1 = 52
		n2 = 77
	}
	out := regressionResult(x, y, ids[:n1], ids[n1:n2], ids[n2:], id == "concrete_slump")
	out["features"] = features
	out["target"] = target
	out["source_rows"] = idx
	out["scope"] = "fixed native ridge protocol; random split does not establish future-batch performance"
	return out
}
func TimeCase(repo, id string) map[string]any {
	series := []float64{}
	times := []string{}
	if id == "sunspots" {
		r := ReadCSV(repo, "data/time_series/sunspots_yearly.csv", ',')
		for _, row := range r[1:] {
			x, e := strconv.ParseFloat(row[1], 64)
			require(e == nil, "invalid sunspot value")
			series = append(series, x)
			times = append(times, row[0])
		}
	} else {
		rows := ReadCSV(repo, "data/industries/"+id+"/data.csv", ',')
		if id == "elnino" {
			for _, row := range rows[1:] {
				for j := 2; j < 14; j++ {
					v, e := strconv.ParseFloat(row[j], 64)
					require(e == nil, "invalid temperature")
					series = append(series, v)
					times = append(times, fmt.Sprintf("%s-%02d", row[1], j-1))
				}
			}
		} else {
			j := 2
			for _, row := range rows[1:] {
				v := math.NaN()
				if row[j] != "" {
					q, e := strconv.ParseFloat(row[j], 64)
					require(e == nil, "invalid time-series value")
					v = q
				}
				series = append(series, v)
				times = append(times, row[1])
			}
		}
	}
	n := len(series)
	cut1, cut2 := n*6/10, n*8/10
	lag := 6
	x := [][]float64{}
	y := []float64{}
	rowtimes := []string{}
	targetIDs := []int{}
	tr, va, te := []int{}, []int{}, []int{}
	skipped := 0
	for t := lag; t < n; t++ {
		good := finite(series[t])
		for _, v := range series[t-lag : t] {
			good = good && finite(v)
		}
		b := 0
		if t >= cut2 {
			b = 2
			good = good && t-lag >= cut2
		} else if t >= cut1 {
			b = 1
			good = good && t-lag >= cut1
		}
		if !good {
			skipped++
			continue
		}
		i := len(x)
		x = append(x, append([]float64(nil), series[t-lag:t]...))
		y = append(y, series[t])
		rowtimes = append(rowtimes, times[t])
		targetIDs = append(targetIDs, t)
		switch b {
		case 0:
			tr = append(tr, i)
		case 1:
			va = append(va, i)
		case 2:
			te = append(te, i)
		}
	}
	out := regressionResult(x, y, tr, va, te, false)
	naive := make([]float64, len(te))
	for i, k := range te {
		naive[i] = x[k][lag-1]
	}
	out["last_value_mae"] = MAE(Values(y, te), naive)
	out["original_observation_count"] = n
	out["target_indices"] = targetIDs
	out["target_times"] = rowtimes
	out["dropped_windows"] = skipped
	out["lag"] = lag
	out["scope"] = "strict chronological complete windows contained in one partition, historical snapshot; no causal discovery"
	return out
}
func Grunfeld(repo string) map[string]any {
	r := ReadCSV(repo, "data/industries/grunfeld/data.csv", ',')
	firmj, yearj := column(r[0], "firm"), column(r[0], "year")
	groups := map[string][][]string{}
	for _, row := range r[1:] {
		groups[row[firmj]] = append(groups[row[firmj]], row)
	}
	x := [][]float64{}
	y := []float64{}
	identity := []string{}
	tr, va, te := []int{}, []int{}, []int{}
	for _, firm := range sortedKeys(groups) {
		rows := groups[firm]
		sort.Slice(rows, func(i, j int) bool { return rows[i][yearj] < rows[j][yearj] })
		for i := 1; i < len(rows); i++ {
			v := []float64{}
			for _, col := range []string{"invest", "value", "capital"} {
				z, e := strconv.ParseFloat(rows[i-1][column(r[0], col)], 64)
				require(e == nil, "panel numeric")
				v = append(v, z)
			}
			target, e := strconv.ParseFloat(rows[i][column(r[0], "invest")], 64)
			require(e == nil, "panel target")
			k := len(x)
			x = append(x, v)
			y = append(y, target)
			identity = append(identity, firm+":"+rows[i][yearj])
			if i < 12 {
				tr = append(tr, k)
			} else if i < 16 {
				va = append(va, k)
			} else {
				te = append(te, k)
			}
		}
	}
	out := regressionResult(x, y, tr, va, te, false)
	out["firm_year"] = identity
	out["features"] = []string{"previous investment", "previous value", "previous capital"}
	out["scope"] = "lagged within-firm temporal experiment, not causality"
	return out
}
func ModeChoice(repo string) map[string]any {
	rows := ReadCSV(repo, "data/industries/modechoice/data.csv", ',')
	cols := []string{"ttme", "invc", "invt", "gc", "hinc", "psize"}
	x, idx := numeric(rows, cols)
	require(len(idx) == len(rows)-1, "choice missing policy")
	gj, cj := column(rows[0], "individual"), column(rows[0], "choice")
	groups := []string{}
	y := []float64{}
	members := map[string][]int{}
	for i, row := range rows[1:] {
		g := row[gj]
		groups = append(groups, g)
		members[g] = append(members[g], i)
		v, e := strconv.ParseFloat(row[cj], 64)
		require(e == nil && (v == 0 || v == 1), "choice binary label")
		y = append(y, v)
	}
	for _, v := range members {
		require(len(v) == 4, "complete four-alternative choice set required")
		s := 0.
		for _, i := range v {
			s += y[i]
		}
		require(s == 1, "exactly one chosen alternative")
	}
	tr, va, te := GroupSplit(groups)
	s := FitScaler(Rows(x, tr))
	z := s.Transform(x)
	trainSet := map[int]bool{}
	for _, i := range tr {
		trainSet[i] = true
	}
	w := make([]float64, len(cols))
	for ep := 0; ep < 250; ep++ {
		g := make([]float64, len(w))
		n := 0
		for _, key := range sortedKeys(members) {
			ids := members[key]
			if !trainSet[ids[0]] {
				continue
			}
			scores := []float64{}
			for _, i := range ids {
				scores = append(scores, dot(w, z[i]))
			}
			p := softmax(scores)
			for j, i := range ids {
				for k := range w {
					g[k] += (p[j] - y[i]) * z[i][k]
				}
			}
			n++
		}
		for k := range w {
			w[k] -= .1 * (g[k]/float64(n) + .01*w[k])
		}
	}
	testSet := map[int]bool{}
	for _, i := range te {
		testSet[i] = true
	}
	predictions := []map[string]any{}
	correct := 0
	for _, key := range sortedKeys(members) {
		ids := members[key]
		if !testSet[ids[0]] {
			continue
		}
		a := []float64{}
		for _, i := range ids {
			a = append(a, dot(w, z[i]))
		}
		p := softmax(a)
		best := 0
		for j := range p {
			if p[j] > p[best] {
				best = j
			}
		}
		if y[ids[best]] == 1 {
			correct++
		}
		predictions = append(predictions, map[string]any{"individual": key, "rows": ids, "probabilities": p, "predicted_row": ids[best]})
	}
	return map[string]any{"features": cols, "train_rows": tr, "validation_rows": va, "test_rows": te, "predictions": predictions, "group_accuracy": float64(correct) / float64(len(predictions)), "weights": w, "scope": "conditional-logit teaching implementation; traveler grouping preserved, not population travel shares"}
}
