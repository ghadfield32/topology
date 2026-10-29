# Exercises: the worked reference is not the assignment

The library in `src/` is worked material. Reading it establishes that the code compiles; it
does not establish that you can design the same contract yourself.

Status of everything on this page: **not_assessed**.

## 1. Change the mutation contract (RS02–RS03, RS04)

`translate_in_place` currently validates the whole batch, then writes. That is a deliberate
all-or-nothing choice. Implement the alternative and defend it:

```
pub fn translate_prefix(points: &mut [[f64; 3]], offset: [f64; 3]) -> Result<usize, InputError>
```

Requirements:

1. Write your own test **first**, and run it to observe the failure before implementing.
2. Decide whether a failure after row *k* leaves rows `0..k` moved or untouched. Whichever you
   choose, the doc comment must state it and the test must prove it.
3. Return how many rows were committed, so the caller can see the partial effect instead of
   guessing.
4. Explain which caller would prefer this to `translated`, and which would be made worse.

Rejected alternative to explain: adding `.clone()` inside the failing branch to avoid the
question. What does that hide?

## 2. The independent `append_feature` contract

The central exercise (RS01, RS05, RS06). Before writing code, answer in your own notes:

- Why is the input `&[[f64; 4]]` and the output `Vec<[f64; 5]>`?
- Which errors are possible, and which of them can be detected without touching any row?
- Can your function change the caller's data? Prove the answer with a test.
- What does the added column say about **rank**, and what does it not say?

Then implement this stricter variant:

```
pub fn append_feature_checked(
    rows: &[[f64; 4]],
    a: f64,
    b: f64,
    tolerance: f64,
) -> Result<Vec<[f64; 5]>, InputError>
```

It must additionally reject a `tolerance` that is not finite and strictly positive, and it
must reject coefficients whose product with the largest input would leave `f64` range. Predict
each rejection before you run it. Include at least one case where your first version returned
`Ok` and the stricter version returns `Err`.

## 3. Extend the compiler cases (RS03)

Add one accepted and one rejected example of your own to `compiler_cases/`, with an entry in
`cases.json`.

- The rejected case must name the diagnostic code you actually observe, not the one you
  expected. Capture it with the real compiler before editing the JSON.
- Write the explanation in terms of *resource, owner, required access, and where that access
  is still needed* — not in terms of memorising an error number.

Then run `python check_compiler_cases.py --output ../../my_work/compiler02`.

## 4. Apply it to real data, not a fixture

Use the crate's functions on a route the course already ships. Choose one and record the
assumption you had to state explicitly:

| Route | What you must decide before computing |
|---|---|
| `data/raw/iris.csv` | One flower per row; the four measurements are the only numeric columns. |
| `poux_bridge` inputs | Whether a sum and a count belong to the same grouping as the average. |
| `data/raw/digits.npz` | Pixel convention, shape order and coefficient field. |

Your note must separate: decoding, structural validity, domain validity, and the scientific
claim. A valid file is not a valid measurement model.

## 5. Performance, only with a matched workload

If you compare two implementations, hold the workload fixed and report: data identity, build
profile, initialisation, decode, calculation, serialisation, peak memory, repetitions, and
numerical error. A faster wrong answer is still wrong, and one run is not a measurement.

Record the profile you used. `cargo run` and `cargo run --release` answer different questions.

## What "independent" means here

You may read this crate, the Rust Book and the compiler's own output. You may not mark the
exercise complete because a worked answer was explained to you. The distinction the course
already keeps:

> "I understood the explanation."

versus:

> "I reconstructed the argument and implemented a changed version myself."

Record which one happened, plus the assistance you used. Then revisit a changed instance after
a delay; that is the only evidence of retention this crate cannot produce for you.
