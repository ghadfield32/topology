# Stage 19 guided session — Do not let future observations leak into an event decision

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/19_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/19_lab.ipynb). The [original workbook](../workbooks/19_workbook.md) and [worked lab](../notebooks/19_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real historical annual observations for causal timing; no human-contact or scientific solar-event ground truth.

## What you will be able to demonstrate

1. Distinguish event onset, confirmation time, and observation availability.
2. Construct a past-only confirmation rule on a real dated series.
3. Check that extending the future does not revise already-issued decisions.
4. Separate a threshold-rule output from validated human–object interaction labels.

## An event label needs a definition
A temporal rule is not meaningful until its conditions, input units, and timestamp conventions are explicit. “Release” could refer to physical loss of contact, a visually annotated frame, or a distance threshold. Those are not interchangeable. The existing hand–ball example remains a synthetic hypothesis test; no real contact annotations are bundled.

This supplement uses a real historical annual sunspot series to teach the timing logic without claiming to validate basketball events. We define an intentionally simple rule: after at least two consecutive high values, confirm a high episode. The threshold is declared for the exercise, not optimized to represent a scientific solar event.

## Separate onset from the decision
If high values occur in years 1901 and 1902, an online two-observation confirmation can issue its decision when the 1902 value is available. It can report an onset hypothesis of 1901, but it cannot honestly claim to have known in 1901 that the run would continue. Backdating onset is not the same as backdating knowledge.

Annual data simplify the clock. A real operating system would also need publication or sensor-arrival timestamps. The historic year alone does not establish when the measurement became available. This notebook assigns availability at the annual sample boundary as an explicit teaching convention.

## Check causality with prefixes
Run the rule on the first k observations. Then run it on the whole series. Restrict the full-series decisions to those issued by time k. They should match the prefix output. A centered smoother or retrospective labeling rule may violate this test because it can use later observations to change an earlier decision.

The test validates past-only behavior of the particular rule. It does not validate event accuracy. To measure accuracy, we would need independently defined reference events and a matching rule specifying time tolerance, one-to-one matching, and handling of missing observations.

## Transfer the distinction to basketball
A distance-only hand–ball rule should output a separation candidate, not certified contact or possession. Missing visibility must not silently become a confidently observed trajectory. Identity changes, camera synchronization, occlusion, fast motion, and false near-passes need labeled evaluation. Onset error and decision delay should both be reported; a rule can locate an onset retrospectively while deciding too late for an online application.

The historical series gives genuine timestamps for learning code. It is not a substitute sports benchmark. This boundary lets us practice the full causal mechanism now while leaving real event validation as an explicit requirement rather than inventing ground truth.

## Predict, execute, and explain

### Step 1

Read real annual observations. The threshold is a declared teaching rule, not a scientific event definition.

```python
import pandas as pd
series = pd.read_csv(ROOT/'data/time_series/sunspots_yearly.csv')
years = series.YEAR.to_numpy(dtype=int)
values = series.SUNACTIVITY.to_numpy()
threshold = 80.
assert np.all(np.diff(years)==1)
print('historical range:', years[0], years[-1])
```

### Step 2

Confirm once per high episode using only observations already available. Retain both onset and decision year.

```python
def confirm_high_episodes(years, values, threshold=80., run_length=2):
    run = 0; emitted = False; out = []
    for year, value in zip(years, values):
        if np.isfinite(value) and value >= threshold:
            run += 1
            if run >= run_length and not emitted:
                out.append({'onset_year': int(year-run+1), 'decision_year': int(year)})
                emitted = True
        else:
            run = 0; emitted = False
    return out
all_decisions = confirm_high_episodes(years, values)
print(all_decisions[:8])
assert all(e['decision_year'] > e['onset_year'] for e in all_decisions)
```

### Step 3

Run prefix checks to ensure future samples cannot alter decisions already issued.

```python
for count in [60, 120, 180, 240, len(years)]:
    prefix = confirm_high_episodes(years[:count], values[:count])
    already_issued = [e for e in all_decisions if e['decision_year'] <= int(years[count-1])]
    assert prefix == already_issued
result = {'real_time_series': 'historical yearly sunspot activity 1700-2008',
          'threshold': threshold, 'confirming_observations': 2,
          'episodes': len(all_decisions), 'prefix_checks': 5,
          'availability_assumption': 'annual sample boundary; actual publication times not supplied',
          'independent_event_accuracy_measured': False, 'basketball_events_validated': False}
```

## Transfer problems — attempt without the solution

### 19.T1

Can a confirmed event have an onset earlier than its decision timestamp?

<details><summary>Reveal reasoning after your attempt</summary>

Yes. The onset is a hypothesis about when the event began; confirmation may require later observations. The system must preserve the later decision time rather than pretending knowledge was available at onset.

</details>

### 19.T2

Does passing prefix consistency establish event precision and recall?

<details><summary>Reveal reasoning after your attempt</summary>

No. It establishes a past-only property of the implemented rule on the tested sequences. Precision and recall require independent reference labels and an explicit matching protocol.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/19_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
