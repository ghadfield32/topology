# Stage 01 guided session — Why the arithmetic system changes the answer

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/01_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/01_lab.ipynb). The [original workbook](../workbooks/01_workbook.md) and [worked lab](../notebooks/01_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real training digit intensities plus an exact, constructed three-by-three matrix.

## What you will be able to demonstrate

1. Translate a small matrix into a system of equations.
2. Perform a row operation and explain why it preserves the solution set.
3. Compare rank over the real numbers and over a prime field.
4. Distinguish a numerical calculation on an image from a topological invariant.

## A matrix is a rule for combining coordinates
A vector is an ordered list of numbers. A matrix can describe a linear rule: multiply each input coordinate by its column and add the resulting columns. The kernel consists of inputs sent to zero. The image consists of all outputs the rule can produce. Rank is the dimension of that image. Rank–nullity says that input dimension equals kernel dimension plus image dimension.

The words “dimension” and “zero” refer to a specified arithmetic system. Over the real numbers, two is nonzero and division by two is allowed. In the field F₂, there are only two elements, 0 and 1; `1+1=0`. Subtraction and addition therefore coincide. This is exact arithmetic, not an approximation to real arithmetic.

## Work a complete example
Consider the three columns `(1,1,0)`, `(1,0,1)`, and `(0,1,1)`. Over F₂ their sum is zero because every coordinate has two ones. The first two are independent: neither is zero and neither equals the other. Consequently the binary rank is two and the kernel has dimension one. The all-ones input is the nonzero kernel vector.

Over the real numbers, the sum is `(2,2,2)`, not zero. The matrix determinant is -2, so its real rank is three. A software call that computes real-valued rank can therefore be completely correct and still answer the wrong question for a binary homology calculation.

For F₃, arithmetic is modulo three. Two has inverse two because `2×2=4`, which leaves remainder one on division by three. Row reduction must multiply a pivot row by the inverse of its pivot before eliminating other entries. In a prime field every nonzero element has an inverse. Modulo four, two does not, so a general “modulo any integer” implementation cannot pretend that the result is a field.

## What a row operation proves
Swapping two equations does not change their simultaneous solutions. Multiplying one equation by a nonzero field element is reversible. Adding a multiple of one equation to another is reversible. Those facts justify elimination. The algorithm is not correct because its output looks triangular; it is correct because each allowed transformation preserves the relevant linear relations.

The real digit image used below is simply a matrix of intensities. Its matrix rank can change with a coefficient convention, but that rank is not the number of loops in the digit. Homology will require a boundary map constructed from a complex. We practice exact arithmetic now so that this additional construction is intelligible later.

## Know when to return to a primer
If matrix multiplication feels unfamiliar, calculate one column combination before running anything. If the proof uses a word such as “independent,” write its definition and test a two-vector example. The efficient route is not to skip the missing definition; it is to repair precisely that definition and then return to the current argument.

## Predict, execute, and explain

### Step 1

Construct the three-column example and compare its ranks using two explicitly different arithmetic systems.

```python
from shape_lab.audits import rank_prime
A = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
print('real rank:', np.linalg.matrix_rank(A))
print('rank over F2:', rank_prime(A, 2))
print('rank over F3:', rank_prime(A, 3))
assert (np.linalg.matrix_rank(A), rank_prime(A, 2), rank_prime(A, 3)) == (3, 2, 3)
```

### Step 2

Check the kernel claim directly. The same stored integers are interpreted in two different ways.

```python
v = np.ones(3, dtype=int)
print('A v over integers:', A @ v)
print('A v modulo 2:', (A @ v) % 2)
assert np.all((A @ v) % 2 == 0)
assert not np.all(A @ v == 0)
```

### Step 3

Use a real digit as an arithmetic object without calling its image-matrix rank a hole count.

```python
from shape_lab.data import digit_example
image, sample_id = digit_example(0)
result = {'sample_id': sample_id, 'real_matrix_rank': int(np.linalg.matrix_rank(image)),
          'binary_matrix_rank': rank_prime(image, 2),
          'interpretation': 'Rank of the intensity matrix; NOT image homology.'}
print(result)
```

## Transfer problems — attempt without the solution

### 01.T1

For A=[2], calculate kernel dimension over F2 and F3.

<details><summary>Reveal reasoning after your attempt</summary>

The map F2→F2 is zero, so its kernel has dimension one. Over F3 multiplication by two is invertible, so the kernel is zero-dimensional.

</details>

### 01.T2

Why is a real-valued SVD threshold irrelevant to the exact F2 rank of a zero–one matrix?

<details><summary>Reveal reasoning after your attempt</summary>

SVD approximates real singular values. Binary rank is a question about linear relations in a different field and uses exact modular arithmetic, not a floating-point tolerance.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/01_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
