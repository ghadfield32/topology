# Independent work: `not_assessed`

The worked reference above is not the assignment. Nothing in this repository scores you,
and a run that finishes is not a demonstrated understanding. These exercises are the ones
worth doing by hand, in order of increasing difficulty. Keep them in
`my_work/world_model_*/`, never in `optional/world_model/`.

## 1. Predict before you run (do this first)

Write the answer in `my_work/world_model_ex01/prediction.md` **before** running anything.

1. `--tolerance 0.02` and a model that beats the frozen baseline for 37 steps. If you set
   the tolerance to `0.005`, does the trust horizon go up, down, or stay the same? Why?
2. The planner draws 200 random plans of length 15. How many distinct 15-step plans exist?
   Compute the fraction of the space being sampled.
3. The balance goal and the park goal share one trained model. Name the *one* thing that
   differs between them, precisely enough to write in a diff.

Then run the tiny configuration and check each prediction. A wrong prediction is the most
useful outcome; write down which assumption it falsified.

## 2. Break the objective on purpose

This is the article's central bug, and reproducing it is the single best exercise here.

Add a third goal `score_park_average` that scores by the **mean** distance from the
target across the whole dream instead of the terminal distance. Compare it with
`score_park` on the same model, the same seeds, and the same number of planning episodes.

Your `comparison.md` must answer:

- Which goal parks the cart closer?
- Is the difference reproducible across at least three seeds?
- Does the *average* goal lose because it discards the correct plan (as the article
  claims), or for a different reason you can actually observe in the planned action
  sequences?
- What would you have to measure to distinguish those two explanations?

Do not report "the terminal score is better" without the observation that explains it.

## 3. Remove the disclosure and measure the damage

`play_episode` uses the hand controller for the first `warmup` decisions and records how
many decisions were planned. Run with `--warmup 8`, then `--warmup 0`, on a model trained
with the default settings.

Report: the survival steps in both conditions, how many decisions were actually planned,
and whether the difference survives more than one seed. A result that changes only the
warm-up is a statement about a blank memory, not about the model.

## 4. Replace the random search with a better one

The planner samples uniformly at random, which is why the useful horizon is far below the
accurate horizon. Implement one alternative in your own copy — beam search over actions,
or a shooting method that refines the best sampled plan — and compare:

- steps survived at planning horizons 1, 3, 5, 10, 20;
- decisions per second;
- whether the improvement appears at long horizons, where random search is starved, or
  also at short ones, where it is not.

This is the exercise that separates "the model is bad" from "the search is bad".

## 5. Write the Rust test that would have caught a bug

In your own copy of `rust/`, add a test that fails on a plausible mistake in the
persistence reduction — for example, ordering simplices by value alone rather than by
`(value, dimension, vertices)`, or dropping the essential-bar bookkeeping. Then delete the
fix and confirm the test fails.

Deliver: the test, the mistaken output it produces, and one sentence on why the mistake is
plausible enough to be worth a test.

## 6. Extend the topology honestly (hardest)

The current summary describes one cloud at one scale. Choose **one** extension and state
its limits before you run it:

- a stability check: perturb the collected cloud by a declared amount and report the
  bottleneck distance against the perturbation size;
- a comparison between two *collectors* (different `exploration` or `bias_scale`) at a
  fixed scale;
- a scale sweep, reporting how the essential-bar count changes with `max_edge`.

Whatever you choose, the write-up must contain a sentence of the form "this does **not**
show …". A shape summary that only says what it shows is not finished.

## Deliverable contract

For each exercise, a private directory containing:

```
my_work/world_model_exNN/
  prediction.md     # written before the run
  results/          # the actual output directory from the run
  comparison.md     # what happened, in the repository's seven-question form
  reflection.md     # your own words; nobody else fills this in
```

The seven questions in `comparison.md` are the ones from
[polyglot/LEARNING_WORKFLOW.md](../../polyglot/LEARNING_WORKFLOW.md), applied to this area:

1. What is one observation?
2. What types did I choose in Python and Rust?
3. What errors can each language represent or prevent?
4. What numerical invariant should match?
5. Which differences are formatting or floating-point effects rather than science?
6. Which specialised library functionality did I *not* reproduce?
7. What does the experiment support, and what does it not support?

Your reflection is yours. Do not paste an answer from this page into it and call it your
independent work.
