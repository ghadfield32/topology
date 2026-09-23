# Foundation B — Enough Python and Jupyter to run the course

You do not need to become a software engineer before learning the mathematics. You do need to know what a cell does, what its inputs are, and whether an output was actually computed from your current code. The examples below are deliberately small. Every new coding activity also includes a full reference implementation and explicit checks.

## A notebook is a sequence of instructions with memory

A Markdown cell contains explanation. A code cell contains Python instructions. Running a code cell sends those instructions to a running Python process called the kernel. Variables remain in that kernel until it is restarted. A notebook saved on disk can contain old outputs even when its code has since changed.

Use **Restart Kernel and Run All** when checking reproducibility. Running cell 15 before cell 2 may work accidentally because an old variable remains in memory. That is not a correct fresh execution. In the supplied reference notebooks, saved execution reports document fresh-kernel runs; your modified notebook needs its own run.

The terminal commands in README.md belong in your terminal, not in an ordinary Python cell. Conversely, `import numpy as np` is Python code, not a shell command. The `%matplotlib inline` line is a Jupyter-specific command; it is not valid syntax in a normal `.py` script.

## Variables, arithmetic, and comparisons

```python
length = 3
width = 4
squared_length = length**2 + width**2
length_of_diagonal = squared_length**0.5
assert length_of_diagonal == 5
```

The single equals sign assigns a value to a name. `==` compares two values. `**` means exponentiation; `^` is not exponentiation in Python. Later, `^` appears intentionally as XOR for binary coefficients or set symmetric difference.

Division `/` preserves fractional results. Floor division `//` discards the fractional part toward negative infinity. Replacing `/16` with `//16` in the image transformation would destroy most grayscale information. Floating-point arithmetic is approximate; use an appropriately justified tolerance such as `np.allclose` when comparing computed square roots. Use exact comparisons for integer counts and exact binary arithmetic.

A boolean is `True` or `False`. Comparisons create booleans. `and`, `or`, and `not` combine ordinary boolean statements. NumPy arrays use elementwise operators such as `&` and `|`, with parentheses around comparisons.

## Lists, indexing, and loops

```python
measurements = [2.0, 4.0, 6.0]
first = measurements[0]
last = measurements[-1]
mean = sum(measurements) / len(measurements)
assert first == 2 and last == 6 and mean == 4
```

Python starts counting positions at zero. A slice `values[1:3]` includes positions 1 and 2 but excludes position 3. This indexing convention is separate from the topological meaning of a half-open interval, although both exclude the right endpoint.

A loop repeats an operation:

```python
total = 0
for value in measurements:
    total += value
assert total == 12
```

Indented lines belong to the loop. The final assertion is outside it. Do not add arbitrary spaces to solve an indentation error: identify which block each line is meant to belong to.

## Functions make assumptions and outputs explicit

```python
def mean_of_nonempty(values):
    return sum(values) / len(values)

assert mean_of_nonempty([1, 3]) == 2
```

`def` declares a function. A parameter is the name used for an input inside the function. `return` sends the result back to the caller. Printing a result is not the same as returning it. A function that only prints normally returns `None`, which will fail a test expecting a number.

This example assumes a nonempty numeric collection. An educational function can work within explicitly stated assumptions; do not claim it handles all possible inputs. The general course helpers validate their key structural inputs. The coding prompts tell you the input domain you need to support.

The learner notebooks use `raise NotImplementedError(...)` as an honest marker of unfinished work. Replace that line with your implementation. The error is not a broken dependency. Never remove a failed assertion merely to obtain a successful-looking notebook.

## Arrays and axes

```python
import numpy as np
X = np.array([[1., 2.], [3., 4.], [5., 6.]])
assert X.shape == (3, 2)
assert np.array_equal(X[:, 0], [1, 3, 5])
assert np.array_equal(X.mean(axis=0), [3, 4])
```

`X[:,0]` means all rows of column zero. `X[0,:]` means all columns of row zero. With observations in rows, `axis=0` combines observations and gives one mean per feature. `axis=1` combines features and gives one result per observation.

Broadcasting lets compatible shapes combine without explicitly writing every loop. Subtracting a four-element mean vector from a 150-by-4 table subtracts that same mean from each row. For pairwise differences, `X[:,None,:] - X[None,:,:]` has shape `(n,n,d)`: one d-coordinate difference per observation pair. Square, sum over the last axis, and take a square root to obtain Euclidean distances. First understand the three shapes before trying to memorize the expression.

## DataFrames and explicit columns

A pandas DataFrame associates names with columns. In the Iris CSV, `sample_id` records identity; the four names ending in `_cm` record measurements; `label` and `species` record annotations. Selecting every numeric column would accidentally include IDs and labels. Use explicit feature names.

A missing value is not zero. The own-data explorer rejects nonfinite selected values rather than silently invent a cleaning rule. A cleaning decision can alter distances and topology and therefore belongs in your experiment description.

## Read an error in order

Find the last error line and the line of your code that caused it. `NameError` means a name is unavailable. `ModuleNotFoundError` often means the package is not installed in the active kernel. `ValueError` usually means the function received an unsupported value or shape. `AssertionError` means a claimed property did not hold. It can reveal wrong code, a wrong expected answer, or a changed assumption.

Reduce the failure to the smallest example. Print shapes and a few values. Compare with the stated convention. Correct the cause and rerun the original check. Record the lesson in `my_work/` instead of hiding the failed attempt.

**Primary follow-up:** the official Python tutorial, source P1 in [Sources](../docs/SOURCES.md). Its current online version can differ from the pinned build interpreter. The package records its actual tested versions separately.
