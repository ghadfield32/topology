# Stage 00 workbook — From a row of measurements to a mathematical question

## Begin here, with no topology background

Put three marks on paper. You already have several possible questions: how many marks there are, their separation, whether they form a cluster, and whether joining nearby marks creates a loop. None of these questions requires knowing the word topology yet. Our goal is to turn informal questions into explicit constructions with checkable answers.

Now replace the marks by measurements. The first two rows in the included Iris file have measurement vectors `(5.1,3.5,1.4,0.2)` and `(4.9,3.0,1.4,0.2)` in centimetres. Subtracting gives `(0.2,0.5,0,0)`. Their Euclidean separation is √(0.2²+0.5²), about 0.5385 in the stated coordinate units. The first calculation concerns these numerical observations, not every member of the species.

The species label is stored separately. It tells us an annotation, not where the flower sits in a mathematical space. Including label codes 0,1,2 as an extra coordinate would silently decide that successive labels are equally separated. There is no justification for that geometry merely because the labels are integers.

## Three kinds of example in this course

A **hand-derived control** has a known mathematical answer: a triangle outline has one edge cycle that is not a face boundary. A **synthetic experiment** deliberately generates observations, such as noisy points near a circle. A **real-data experiment** uses actual measured samples or handwriting images, while acknowledging how they were collected and what information is absent.

Controls catch errors. Synthetic experiments isolate mechanisms. Real data test whether an interpretation remains useful in a particular observed setting. They serve different roles. We never silently replace a missing real dataset with a synthetic array and call it real evidence.

## The chain of objects we will build

Start with the raw table or image. Select measurements and a meaning of closeness. Build a complex: a structured collection of vertices, edges, filled triangles, and possibly higher-dimensional pieces. Use linear algebra to identify certain kinds of holes. Repeat across a parameter to follow which classes persist. Finally decide whether the resulting information answers a useful question.

Every arrow is a modeling decision. There is no automatic step where an arbitrary data table acquires the uniquely correct topology. That is why learning the basic definitions matters before interpreting a plot.

## Your first code session

Open the learner notebook for Stage 00. It has a setup cell and five short functions to write. The setup finds the extracted course directory and imports the included code and data. It makes no data-download request. The first exercise asks for a table's shape; the second asks for a mean. Do them with plain reasoning before NumPy abbreviations.

For each function, say its contract aloud. For example: “The input is a nonempty rectangular list of numeric rows. The output is a pair containing the row count and the column count.” Write one answer you can verify manually. Run the check. Explain whether the actual output matches your prediction and why.

A line raising NotImplementedError is intentionally unfinished work. A reference answer notebook exists separately. Open it only after trying. Reading it first is allowed for learning, but then label your attempt as guided rather than independently solved.

## Inspect the real objects

The Iris file is a CSV: a header names the columns and each later line is an observation. The digit snapshot stores 1,797 images, each with 8 rows and 8 columns of intensities. Our frozen partition has 1,077 training, 360 validation, and 360 test images. Those are this course's image-level partitions, not a claim that different writers are separated.

Use only the training image examples during early exploration. The final worked test results are already published inside this package. Reproducing them is valuable, but it cannot make them unseen again. A later independent project needs a fresh evaluation design.

## Make a useful first record

In your work folder, write four sentences: what one observation means; which columns are measurements; which values are labels; and one conclusion the current example cannot establish. Then include the output of your five functions. That is more useful evidence than recording “watched a topology video.”

The local tracker distinguishes practice, independent assessment, and delayed recall. It does not train an AI model, notify you in the background, or know whether your self-report is truthful. It helps preserve evidence so this chat can focus on your actual misunderstandings instead of restarting the plan.

**Depth boundary:** Stage 00 introduces the workflow, not a proof of any topological inference theorem. Unknown terms in the pipeline are intentionally unpacked in later stages. Sources D1–D3 establish the dataset descriptions; the numerical examples and exercises are original.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/00_lesson.md) · [Worked lab](../notebooks/00_lab.ipynb) · [Your coding notebook](../practice/learner/00_practice.ipynb) · [Reference coding solutions](../practice/00_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
