# Stage 19 coding solutions

Attempt your learner notebook before opening this file.

## 19.C1 — decision_delay

Return causal decision delay, rejecting a decision before the estimated onset.

**Hint:** Decision time is when sufficient evidence becomes available, not necessarily the event onset.

```python
def decision_delay(onset_time, decision_time):
    if not np.isfinite([onset_time,decision_time]).all() or decision_time<onset_time:raise ValueError("Decision must be finite and no earlier than onset.")
    return decision_time-onset_time
```

A retrospectively assigned onset timestamp does not mean an online decision was available then.

### Checks

```python
assert np.isclose(decision_delay(.24,.26),.02)
try:decision_delay(.3,.2)
except ValueError:pass
else:raise AssertionError("Negative decision delay is invalid under this contract.")
```

## 19.C2 — visible_pair_mask

Allow a pair only when both observations are visible and the identity pairing is valid. Inputs are one-dimensional matching boolean arrays.

**Hint:** Use conjunction, not a union of evidence.

```python
def visible_pair_mask(visible_a, visible_b, identity_matches):
    a=np.asarray(visible_a,bool);b=np.asarray(visible_b,bool);i=np.asarray(identity_matches,bool)
    if a.ndim!=1 or a.shape!=b.shape or a.shape!=i.shape:raise ValueError("Matching one-dimensional masks required.")
    return a&b&i
```

Valid visibility and identity are prerequisites, not sufficient evidence of physical contact. Predicted positions cannot be relabeled as direct observations.

### Checks

```python
assert np.array_equal(visible_pair_mask([1,1,0],[1,0,1],[1,1,1]),[True,False,False])
assert not visible_pair_mask([1],[1],[0])[0]
```

## 19.C3 — event_rates

Return precision and recall from nonnegative integer counts. Undefined rates are None.

**Hint:** Precision denominator uses predicted events; recall denominator uses reference events.

```python
def event_rates(true_positive, false_positive, false_negative):
    vals=[true_positive,false_positive,false_negative]
    if any(not isinstance(v,(int,np.integer)) or v<0 for v in vals):raise ValueError("Nonnegative integer counts required.")
    tp,fp,fn=vals
    return {"precision":tp/(tp+fp) if tp+fp else None,"recall":tp/(tp+fn) if tp+fn else None}
```

These counts must come from a declared one-to-one matching protocol. Correct arithmetic does not establish valid annotations or an appropriate event definition.

### Checks

```python
assert event_rates(2,1,2)=={'precision':2/3,'recall':.5}
assert event_rates(0,0,0)=={'precision':None,'recall':None}
```