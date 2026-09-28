# One mathematical curriculum; complete, staged language practice

The aim is not to memorize the same theorem in three languages. Learn the idea once, then expose the implementation choices in Python, Go and Rust. This document teaches how to progress; each of the 57 native-unit pages identifies the computation, actual inputs, three independent challenges and the boundary to its original Python notebook.

Your current position is Stage 01. Stage 00 is an environment/data orientation, not a reason to repeat familiar Python. Do not skip a mathematical gate because the code looks short.

## A. What counts as learning

Separate four records: read, guided practice, independent demonstration and delayed recall. A compiler pass establishes that one program can be built, not that its algorithm is right. A unit test checks its assertions, not every possible input. Two programs can share a conceptual error. A correct numerical result can still be interpreted incorrectly.

For every session, save: your question, the observation unit, a prediction, one hand calculation, the code you changed, the test output, a controlled perturbation, a supported conclusion and a limitation. State what needed help. Revisit a changed example after a delay. These records remain local unless you deliberately review and publish them.

**One primary explanation:** use `course.py stage N` for the original lesson. Use `native_course.py show stageNN` for the implementation path. Open a primer only where you are stuck. The combined books and saved notebook exports are alternate views, not additional assigned reading.

## B. Shared foundations before language differences

A value is a piece of data. A type constrains which values or operations a program accepts. An array has a shape and a storage order; those are distinct. A function has inputs, outputs and a contract. An error is a result to handle, not a number to replace with zero. A test has a stated expectation and a finite scope.

Start with a 2-by-3 matrix. Say whether a function may change its input. Calculate the output shape before multiplying. Specify `f64`/`float64` and the coefficient field. Real-valued arithmetic and F2 arithmetic are not interchangeable even if the bytes contain only zeros and ones.

Then define observations. One frame, one trial, one athlete, one firm-year and one alternative in a traveler's choice set are not interchangeable independent units. IDs should not silently become model features; class labels should not leak into self-supervised encoder fitting; a missing coordinate should not become the origin.

### The Stage 01 contract

Take A=[[1,1,0],[1,0,1],[0,1,1]]. Derive its real rank and F2 rank. Add the feature 2*x0-3*x1 to the four-column Iris matrix and derive the resulting null vector. Explain what numerical tolerance means and what it does not say about biology.

The Go code clones row storage before elimination. The Rust code creates an owned working matrix from a borrowed input. Trace those choices. A compiler preventing an invalid borrow does not automatically select a stable numerical algorithm.

## C. Python learning path

### P0 — arrays, functions, notebooks and tests (Stages 00–02)

Use the existing isolated uv environment, not whatever interpreter an editor happens to select. Inspect dtype, shape and source IDs. Learn Boolean masks as finite preimage calculations. Understand copying, views, broadcasting and axis selection. Write the small loop before using a vectorized expression. Tests should cover an empty array, a mismatched shape and a nonfinite value, not only the happy path.

**Deliverable:** explain your matrix-rank investigation from inputs to outputs. Show which array is copied and why.

### P1 — numerical and statistical reasoning (Stages 01–06)

Study rank, null spaces, covariance, conditioning, discretization and tolerance. State whether you use a population or sample covariance convention. Do not interpret four stored columns as proof of a four-dimensional manifold. Explicitly preserve the coefficient field in homology calculations.

**Deliverable:** verify boundary-of-boundary zero on a small complex and explain the proof separately from its matrix test.

### P2 — scientific libraries without blind trust (Stages 07–17)

Read the algorithm's assumptions and parameters. Compare your small persistence algorithm with the retained reference and optional production libraries when installed. Use exact geometric controls before real point clouds. Separate fitting registration references from holdouts. Check an image's channel order and scale, not only its filename.

**Deliverable:** a same-data comparison with the baseline and a perturbation that reveals a limitation.

### P3 — models and reproducible research (Stages 18–30 and R01–R05)

Use source hashes, versioned protocols, train-only preprocessing and fresh kernels. Compare a learned model with a conventional solver or baseline. Inspect losses, model weights and sample-level predictions. A physical penalty is not a conservation theorem. A low distributional regularizer score is not proof of semantic information.

**Deliverable:** an exposed teaching result with clearly stated limits, followed later by a genuinely independent capstone.

### Python strengths and tradeoffs to investigate

Python provides concise exploratory code and access to the existing scientific ecosystem. An array expression may execute optimized compiled code; therefore a Python-versus-Go/Rust timing comparison must identify the actual kernels. Dynamic types and notebook state can hide shape errors or stale state. Compiled extensions also introduce binary/version constraints. Test the concrete workload; do not declare an automatic language speed hierarchy.

## D. Go learning path

### G0 — compile, run, inspect (Stage 01)

Learn packages, exported names, `go.mod`, `main`, `go test`, `go run` and `go build`. Distinguish a program's exit status from its mathematical result. Read the runner at `native/go/cmd/shape-go/main.go`; find where input flags, computation and output writing occur. A successful source file listing is not lab completion.

**Exercise:** run Stage 01 directly, then deliberately supply an unknown lab key. Explain the two outcomes.

### G1 — slices, maps, structs and mutation (Stages 01–04)

A slice refers to an underlying array. Copying a slice descriptor does not duplicate its data. A matrix represented as `[][]float64` requires attention to both the outer slice and each row. Learn `make`, `append`, `copy`, length/capacity and struct fields. Use maps for identities, not for assuming iteration order. Sort keys before deterministic output.

**Exercise:** construct one shallow copy that aliases row storage and one deep copy that does not. Mutate a pivot and test the caller-visible difference. Then explain why the actual elimination function preserves its input.

### G2 — contracts and data readers (Stages 02–07, industry entry cases)

Read CSV with a CSV parser, not `strings.Split`. Quoted commas and newlines are valid fields. Learn `encoding/json`, `UseNumber`, bounds checks, typed records and error returns. The reader distinguishes unknown bytes from a supported binary format, limits decompression, checks archive member paths and rejects unsafe integer conversions.

**Exercise:** decode the supplied PNG and NPZ versions of an image and compare every pixel. Test BOMs, missing numeric fields, scientific notation, embedded NUL in Unicode arrays and malformed archives. Explain why whole-file hashing and decoded-value equality answer different questions.

### G3 — topology data structures (Stages 05–11)

Represent a simplex by sorted distinct vertex IDs plus filtration value. Validate faces before reduction. A graph clique does not become a filled simplex unless the construction says so. Trace sorted XOR boundary columns and a separate MST. Use bounded teaching data: the enumerator deliberately refuses excessive simplices.

**Exercise:** write an independent boundary builder on a private copy and compare with the reference triangle and tetrahedron. Preserve multiplicities in intervals. Do not report unsupported H2 structure from a dimension-truncated complex.

### G4 — geometry and temporal processing (Stages 13–20, S00–S06)

Make coordinate frames and units explicit. Distinguish rotations from reflections and optical depth from Euclidean range. Read actual timestamps rather than replacing time with row number. Reject a gap when the motion calculation lacks support. Use context and cancellation when designing your own long-running service; the current reference CLI is a bounded batch program.

**Exercise:** compute a nonuniform-interval velocity and show how an incorrect sampling-rate assumption changes it.

### G5 — training and automatic differentiation (Stages 23–29, R02–R04)

Study the scalar reverse-mode tape: node value, parents and local derivative weights. Backpropagation accumulates contributions along every edge. The second-order jets retain derivatives on that tape so parameter gradients can pass through input derivatives. This is an educational implementation, not a replacement for a mature tensor compiler.

**Exercise:** verify the derivative of tanh(w*x), its second derivative in x and the derivative of that quantity in w. Compare finite differences with the tape and the independent PyTorch checks before training a PINN.

### G6 — concurrency and performance, after correctness

Learn goroutines, channels, wait groups, mutexes, cancellation and bounded work queues. Concurrency organizes independent work; it does not guarantee faster execution. Keep deterministic merge order when reductions are being compared. The input-audit map is mutex-protected, but its lifecycle is one run per process; do not assume concurrent independent Run calls have isolated provenance. Use separate processes unless you refactor the context explicitly.

**Exercise:** process disjoint chunks, carrying both sum and count, and merge in a deterministic order. Check the race detector where available. Record file decode, allocation, calculation and serialization time separately. Reject unbounded queues and silent dropped frames.

### Go strengths and tradeoffs to investigate

The native program is a straightforward compiled command with standard-library data support. Slices and explicit loops make data movement visible; garbage collection and allocation still cost resources. Concurrency is convenient, but data races and nondeterministic reductions remain possible. The ecosystem does not automatically provide every scikit-learn or PyTorch operation. Compare a deliberate implementation or supported library—not a Python wrapper presented as Go training.

## E. Rust learning path

### R0 — toolchain, crates and errors (Stage 01)

Learn rustup, rustc, Cargo, packages, crates, modules and Cargo.lock. Build from `native/rust`, where Cargo discovers the vendored-source configuration. Read a compiler diagnostic instead of repeatedly inserting clones. This delivery includes an actual compiler-tested workspace and source dependencies; it does not include a compiler binary for your operating system.

**Exercise:** run tests offline, run Stage 01, then supply an invalid source path and identify where it is rejected.

### R1 — ownership, borrowing and collections (Stages 01–04)

A value has an owner responsible for its lifetime. A borrow gives temporary access without moving ownership. `&T` is shared access; `&mut T` grants exclusive mutable access subject to Rust's rules. `Vec<T>` owns a growable sequence; a slice borrows a region. Copying a numeric scalar differs from cloning a vector.

**Exercise:** implement an in-place elimination kernel taking mutable data and a preserving interface that clones once before calling it. Explain why a row-pivot loop can cause conflicting borrows and how disjoint slices or a deliberate pivot copy resolve the issue.

### R2 — valid states, Result and Option (Stages 02–07)

Use enums to name alternatives. `Option` represents presence or absence; `Result` distinguishes success from failure. Do not encode missing coordinates as zero or essential intervals as an arbitrary huge finite number. The current educational kernels use asserts and the CLI catches panics; a service-oriented refactor should expose typed errors without hiding invariant failures.

**Exercise:** design typed units for metres and pixels, or an enum distinguishing observed, inferred and missing geometry. Show how this prevents one concrete mistake while leaving numerical validation necessary.

### R3 — native parsing and serialization (industry cases)

Inspect `serde`, `csv`, `zip`, and `png` as format libraries, not mathematical black boxes. Check endian order, dtype widths, Fortran versus C storage and Unicode lengths. The JSON dependency's round-trip float feature preserves the tested source decimals; the prior discrepancy is retained in the evidence record.

**Exercise:** write a round-trip test for a scalar Unicode NPY value and a big-endian array. Reject an object dtype rather than deserializing a pickle. Explain the decoded-image alpha convention and why premultiplication can change stored channel values.

### R4 — algebra, topology and geometry (Stages 05–20)

Trace owned matrices, borrowed points, sorted boundary supports, optional deaths and explicit numeric tolerances. Keep algorithm choice separate from memory safety. A safe program can compute the wrong homology if it omits killing simplices, or the wrong depth if it ignores a principal-point offset.

**Exercise:** implement one independent MST or radius-graph component calculation and compare its invariants against persistence. Test the exact square before an observed cloud.

### R5 — autodiff and small learning systems (Stages 23–30, R01–R05)

Read the native tape and jet code. This tape uses `RefCell` for runtime-checked interior mutability so expression construction can use shared handles. That is a deliberate teaching convenience, not a zero-overhead or automatically thread-safe design. Nodes are index references into an owned graph; backward accumulation must cover repeated parents.

**Exercise:** compare a repeated-variable derivative, then the mixed derivative needed by the PINN. Plot or tabulate both data/model error and the relevant physical residual. Preserve failed training runs.

### R6 — services, parallelism and deployment

Learn `Send`, `Sync`, thread scopes, mutexes, channels and structured cancellation before designing a parallel service. Compile once for timing comparisons; do not compare `cargo run` compilation time with an already running Go binary. Do not equate bounds checks with validation of external data rights or scientific meaning.

**Exercise:** use owned chunk messages, deterministic reductions and an explicit memory limit. Rebuild the image and run its own acceptance before submitting a Kubernetes Job. Export evidence from a PVC before cleanup.

### Rust strengths and tradeoffs to investigate

Ownership can expose lifetime and aliasing mistakes before runtime. Explicit types can make invalid combinations harder to express. Compiler diagnostics and dependency/linker setup require learning effort; numeric algorithms still need tests, conditioning analysis and independent checks. Unsafe code or foreign-library integration adds separate obligations. Native code is not a universal promise of faster computation than optimized Python libraries.

## F. Compare languages without changing the scientific question

For an exact comparison, keep IDs, labels, coefficient field, ordering and algorithm identical. For f64 calculations, state tolerance and show discrepancies. For training, match the actual initial arrays or generator algorithm, not merely the integer seed. Separate exact/numerical agreement from protocol agreement.

The native16 protocol is intentionally small enough to inspect. Some original Python notebooks use different descriptors, split policies, architectures and solvers. Those differences are recorded in COVERAGE.md. Do not interpret different accuracies from different partitions as a language comparison.

Three implementations agreeing can be good software evidence, but they are not three independently collected datasets. Independent controls, library checks and proofs still matter. The included Python checks independently reproduce selected classifiers and neural-physics training, rather than validating only a scalar aggregate.

## G. Cross-sector sequence

At Stage 01 use Iris for rank and redundancy, then the Poux/SPL bridge for weighted means and time-order information. After metrics, inspect Wine or Seeds feature geometry. After data-splitting lessons, examine healthcare records, firm-year panels and grouped travel alternatives. After persistence, compare a descriptor with a conventional feature baseline. After camera geometry, use the measured stereo example. After dynamics and uncertainty, build a physically defensible study rather than forcing a neural PDE onto a scalar table.

Every source has a specific observation unit and acquisition history. Selected sports profiles, transcribed frames, old climate series and simulated oscillators must retain those labels. The package does not acquire modern full sports video, LiDAR or model weights on your behalf.

## H. Completion gates

1. Define the idea and give a nonexample.
2. Calculate a small instance before code.
3. Run the reference and explain every output field.
4. Make an independent private change in Go and Rust and test it.
5. Compare the two implementations and selected independent Python checks.
6. Change one assumption and predict the consequence.
7. Write a result with its strongest justified conclusion and a limitation.
8. Revisit a changed problem after a delay.

A complete learning path does not mean every future task is solved. General alpha complexes, original-paper reproductions, full spatial-model pipelines, independent physical validation and the actual book audit remain explicit advanced obligations. Keep the course usable now without labeling those obligations as already completed.

## Official free references

- Rust ownership/borrowing: https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- Rust error handling: https://doc.rust-lang.org/book/ch09-00-error-handling.html
- Cargo vendoring/locked/offline: https://doc.rust-lang.org/cargo/commands/cargo-vendor.html
- Go tour: https://go.dev/tour/
- Effective Go, slices and concurrency: https://go.dev/doc/effective_go
- Go tests: https://go.dev/doc/tutorial/add-a-test
- NPY representation contract: https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html
- Existing topology sources and Poux source register remain in the original course; do not copy subscription tutorials into this package.
