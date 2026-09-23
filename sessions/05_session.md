# Stage 05 guided session — Choose the object before counting its holes

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/05_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/05_lab.ipynb). The [original workbook](../workbooks/05_workbook.md) and [worked lab](../notebooks/05_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real training digit foreground; exact ring and diagonal-pair controls.

## What you will be able to demonstrate

1. Distinguish closed-square pixel geometry from a graph of pixel centers.
2. Count vertices, edges, and faces of a small cell complex.
3. Explain why diagonal touching connects closed squares.
4. Declare the intensity threshold before interpreting a real image.

## Start with one pixel
A pixel can be modeled in several ways: a point at its center, a square region, or a vertex carrying a value in another complex. These choices are not equivalent descriptions. Our image model is the union of closed unit squares selected by an intensity rule. Closed means that the boundary belongs to the square. Two squares meeting only at one corner therefore intersect and their union is connected.

In contrast, a graph connecting pixel centers only horizontally and vertically leaves a diagonal pair disconnected. That graph is a legitimate object; it is simply a different object. Before arguing that two programs disagree about topology, compare the objects and connectivity conventions they actually use.

## Count a two-square example
One square has four vertices, four edges, and one face, so its Euler characteristic is `4−4+1=1`. Two squares sharing an entire edge have six distinct vertices, seven distinct edges, and two faces: `6−7+2=1`. Two squares meeting only at one corner have seven vertices, eight edges, and two faces: `7−8+2=1`. Both unions are connected and have no planar hole.

Counting each square's four vertices separately would double-count shared pieces. A complex records shared faces by identity, not by coincident drawings. Our independent pixel checker therefore collects distinct vertex and edge keys before computing `V−E+F`.

## Put a hole in the example
Select all eight squares surrounding the middle square in a three-by-three grid, leaving the center unselected. The union is connected and encloses one missing square. It has 16 vertices, 24 edges, and 8 square faces, giving Euler characteristic zero. For this finite planar complex, H₂ is zero and `χ=β₀−β₁`; thus `β₁=1−0=1`.

When we split each square into two triangles, we add a diagonal edge and replace one square face with two triangle faces. The change in `V−E+F` is `0−1+1=0`. More importantly, this subdivision preserves the underlying square region. We can use triangulated boundary matrices and compare them with direct square-cell counting.

## Now threshold a real image
A threshold creates a binary selection from measured intensities. In the digit course, bright strokes enter first through `f=1−intensity/16`. Selecting intensities at least 8 is equivalent to selecting `f≤0.5`. Every term needs a declared convention: bright or dark first, strict or non-strict inequality, closed squares or center points, and whether the exterior is padded.

The answer is topology of this chosen thresholded image model. It is not proof that every handwritten instance of the corresponding numeral has that topology. A low-resolution stroke can join diagonally or disappear at a threshold. Later persistence replaces a single arbitrary threshold with an entire changing family, but it does not remove the need to define that family.

## Predict, execute, and explain

### Step 1

Check three declared square-cell objects using connectivity and Euler counting, without boundary matrices.

```python
from shape_lab.audits import pixel_betti_oracle
ring = np.ones((3, 3), dtype=bool); ring[1, 1] = False
print('ring:', pixel_betti_oracle(ring))
print('diagonal pair:', pixel_betti_oracle(np.eye(2, dtype=bool)))
assert pixel_betti_oracle(ring) == (1, 1)
assert pixel_betti_oracle(np.eye(2, dtype=bool)) == (1, 0)
```

### Step 2

Construct the declared foreground from one real training digit.

```python
from shape_lab.data import digit_example
image, sample_id = digit_example(8)
threshold = 8
foreground = image >= threshold
b0, b1 = pixel_betti_oracle(foreground)
print('record:', sample_id, 'threshold:', threshold, 'Betti:', (b0, b1))
import matplotlib.pyplot as plt
plt.figure(figsize=(4, 4)); plt.imshow(foreground)
plt.title('Declared closed-square foreground'); plt.axis('off'); plt.show()
```

### Step 3

Record conventions next to the numeric answer.

```python
result = {'sample_id': sample_id, 'foreground_rule': 'intensity >= 8',
          'object': 'union of closed square cells', 'corner_touching_connected': True,
          'betti': [b0, b1], 'claim': 'One thresholded image, not an ideal numeral.'}
```

## Transfer problems — attempt without the solution

### 05.T1

For two diagonally touching selected pixels, why do a four-neighbor center graph and a closed-square union disagree about H0?

<details><summary>Reveal reasoning after your attempt</summary>

The graph omits a connection, while the closed squares share a corner. They encode different spaces; neither output alone resolves which representation the application needs.

</details>

### 05.T2

Why does adding an interior diagonal to triangulate a square leave Euler characteristic unchanged?

<details><summary>Reveal reasoning after your attempt</summary>

Vertices are unchanged, edges increase by one, and the one square face is replaced by two triangle faces, increasing face count by one. The changes cancel in V−E+F.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/05_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
