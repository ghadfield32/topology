# Stage 00 — Start here: how to learn, run, and question the results

**Starting point:** No prior topology knowledge is assumed.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Begin with observations, not unfamiliar terminology
Imagine putting several dots on paper. You can ask where each dot is, which dots are close together, whether they form separated groups, and whether they surround an empty region. These are different questions. A table of measurements can be treated similarly even when its rows have more than two numbers and cannot be drawn faithfully on a page.

An **observation** is one measured item. A **feature** is one measurement of that item. A **dataset** collects observations. In our Iris data, an observation is a flower sample and a feature is a measured length or width. In our digits data, an observation is a small handwriting image. A **label** says which species or digit was recorded; it is not a geometric coordinate unless we deliberately, and usually inappropriately, put it into the distance calculation. See sources D1–D3 for the actual dataset descriptions.

We will start with tiny examples whose answers can be derived exactly. We will then use genuine measured data. Artificial circles are useful controls, not evidence that real populations are circular. Every notebook identifies which kind of example it is using.

**Topology** studies spaces and continuous maps. **Homology** translates part of their shape information into algebra. **Persistence** follows homology classes as a construction changes with a parameter. Those words will become precise one at a time; you do not need to understand them before starting.

## 2. Your two routes through the package
The reading route needs no installation: open `START_HERE.html`, read a stage, and view its saved notebook outputs. The experimentation route uses Python and Jupyter. Follow `README.md` to create one project-specific environment, then open the notebooks in numerical order. A notebook mixes explanatory text with executable code cells. Run cells from the top. Restarting the kernel and running all cells is the best check that the notebook does not depend on forgotten variables.

A terminal is a program into which you type commands. A folder path tells it where a file lives. `cd` changes the working folder. `python` starts the Python interpreter; `python -m pytest` asks Python to run the test module. The virtual environment is a separate package installation area for this course; it is not a new operating system. You do not need a GPU or to modify your production projects.

Python counts positions starting at zero. `x[0]` means the first item. `len(x)` counts items. `print(x)` displays a value. An assignment such as `a = 3` stores a value; `a == 3` asks whether two values are equal. `assert condition` stops execution when the condition is false. An assertion is an automatic check of one statement in a computation, not a proof about all possible inputs.

A NumPy **array** is a structured collection of numbers. A 2D array has rows and columns: a shape of `(150, 4)` means 150 rows and four columns. The expression `X[:, 0]` selects all rows of the first column. `import numpy as np` makes the numerical library available under the short name `np`. You will see these patterns repeatedly.

## 3. Learn in six moves
Read an explanation and say what problem it solves. State the definition. Work one small example on paper. Predict the code output. Run the code and compare. Finally, explain what the output does not establish.

Do not immediately read the solution after a difficulty. Write the exact point at which you became stuck: an unknown word, a missing algebra step, an unclear assumption, or a programming error. Read the relevant hint in the lesson, try again, and then compare with the separate solution. Re-solving a related question after a delay is more informative than recognizing an answer you just saw.

Each stage has a short notebook plus a detailed lesson and worked exercise solutions. The code is already functional: your task is to understand and modify it, not repair intentionally broken starter files. A deeper code-reading task points to a specific function in `src/shape_lab`. The tests under `tests/` check mathematics and software. They do not mark you as mathematically proficient.

## 4. Know the boundaries of the claim
This is an original introductory course aligned to the supplied chapter outline, not the text of *Listening to Shape*. The publisher page could not be retrieved during this build; its March 2027 date remains the user's supplied listing, not a newly confirmed release promise. A final book audit is included for when the actual text is available.

The course's central computation is ordinary homology over the two-element field. It covers essential point-set topology, introductory algebraic topology, one-parameter persistence, and applied evaluation. Advanced topics have an explicit bridge later; no finite archive should pretend to include every theorem in topology.

The core was designed to run with the numerical packages available in the build environment. Ripser and GUDHI are optional cross-checks. Their installation was blocked here, so their checks are labeled NOT RUN, not passed. This is a limitation of the independent validation evidence, not a reason to invent results.

## 5. Your first practical session
Open the Stage 00 notebook. Run the cell that shows array shapes and a few **training** observations. Make a simple plot and locate its saved PNG in `reports/stage_00`. Change one display choice, rerun, and explain what changed. No interpretation of holes is expected yet.

Use the version-3 learner record in `progress/learning_log_v3.json`; see `docs/LEARNING_SYSTEM_V3.md` for recording evidence or preserving an older log. Leave all stages unmastered initially. Record both what you did independently and what you needed help with. When continuing here, paste your stage number, answers, and any error traceback rather than saying only that it did not work.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**00.1.** Explain observation, feature, label, and dataset using one handwriting image.

**00.2.** What do the two numbers in an array shape mean? What does X[:, 0] select?

**00.3.** Predict whether `3 == 3` and `3 == 4` are true; explain why assignment is different.

**00.4.** Why do we run an exact synthetic example before a real-data experiment?

**00.5.** What does a passed software test establish, and what does it not establish?

**00.6.** Find the digits split sizes in data/manifest.json and explain why they are not the original UCI split.

## Mastery gate

Run Stage 00, explain its data shapes and provenance, and distinguish code execution from understanding.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: D3, R1. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/00_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/00_solutions.md`, record what was independent, and continue only when the gate is met.
