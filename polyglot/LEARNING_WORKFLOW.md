# Reimplement instead of copy

For each lab, do **not** edit the reference source in place. Create a private folder such as:

```text
my_work/polyglot/stage01_attempt01/
  prediction.md
  go/
  rust/
  comparison.md
```

Copy the relevant `polyglot/go/labs/<lab>.go` and `polyglot/rust/src/labs/<lab>.rs` only after you have written the hand prediction. For a harder practice pass, delete the body of the `run` function and rebuild it from the spec page and tests.

In `comparison.md`, answer:

1. What is one observation?
2. What types did I choose in Python, Go and Rust?
3. What errors can each language represent or prevent?
4. What numerical invariant should match?
5. Which output differences are formatting or floating-point effects rather than scientific differences?
6. Which specialized Python library functionality did I *not* reproduce?
7. What conclusion does the experiment support, and what conclusion does it not support?
