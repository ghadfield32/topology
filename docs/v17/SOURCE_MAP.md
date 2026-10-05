# Source-derived structure, integration choices, and execution limits

## Requested basis

The new source is the user-provided `Pasted text(20261004-164420).txt`. Its key rule is **Notebook → understand it. Project → prove you can engineer it.** Its repeated learning cycle is **Explain → Predict → Implement → Break → Apply**. The provided implementation transcript is a different source: it reports a local 171-workbook generator and a successful Stage 01 triad; it explicitly says the complete 171-workbook sweep was not run.

The source introduction says "nine stages" but its actual headings run from Stage 0 through Stage 9. This package preserves all ten headings as `sys00`–`sys09`, without renumbering topology Stage 00–30. That is a numbering clarification, not an omitted topic.

The supplied v16 archive is the executable base. All its original paths are retained. The new `learning/` view is generated from the existing 57-unit native registry and 31-stage core catalogue, not a new competing mathematics syllabus. The missing local workbook generator was not present in the archive or readable on the remote branch. These interfaces are reconstructed from the supplied contract, not recovered unpublished edits.

## Exact topic families and where they go

| Source heading | Preserved learning topics | Implementation and limits |
|---|---|---|
| Environment | VS Code, WSL2/Linux, Git, real compilers, research versus engineering layers | FIRST_RUN.md and MIGRATION.md; no Windows/WSL upgrade or installation was performed on your computer. |
| Stage 0 | Binary/hex, signed/unsigned, floating point, registers, stack/heap, virtual memory, processes/threads, caches/SIMD, compile/link/libraries/syscalls | sys00; portable byte contract, C memory experiment, debugger/profiling assignments. Not a measured hardware microarchitecture course. |
| Stage 1 C | Preprocessing through linking; primitive types; pointers; arrays/buffers; malloc/free; structs; leaks/double-free/UAF/bounds/null | sys01; real bounded binary reader, exact format, tests, actual sanitizer failure fixture. Other unsafe examples are learner tasks, not silently executed by normal runs. |
| Stage 2 C++ | Values/references/const, vector/array/string/maps/optional/variant, RAII, unique/shared ownership, copy/move, templates, algorithms, CMake, debugger, sanitizers, profiling | sys02; C++20 trajectory and MST core plus concept tests. Debugger session, ThreadSanitizer and full OpenCV engine are not recorded as executed. |
| Stage 3 C++/Python | pybind11, same inputs, numerical error, latency/throughput/memory | sys03; actual extension and numerical checks. Installed PyTorch's real pybind11 headers were explicitly selected in this build; clean pybind11 package installation was not performed. No speedup claim. |
| Stage 4 OpenCV | Mat/channels/stride/copy, intrinsics/distortion/projection/PnP/triangulation/stereo | sys04 maps to existing Stages14–17 and native stereo; Python OpenCV experiment runs. New C++ OpenCV probe needs development headers and is blocked here. General PnP/calibration remains a guided extension. |
| Stage 5 GPU | PyTorch profiler, device placement, transfers, vectorization, compile, FP32/FP16/BF16/TF32, Triton, CUDA, SM/warp/block/grid/memory, Nsight | sys05; CPU profiling on repeated real measurements runs. GPU/Triton/CUDA and Nsight/precision comparisons are source-backed projects, not CPU results relabeled as GPU execution. |
| Stage 6 TypeScript | JS execution, Promise/async, primitives/interfaces/unions/generics/narrowing/unknown, runtime data, viewer | sys06; strict TS project and actual offline viewer of observed/predicted 3D coordinates via a labeled 2D projection. No hidden Three.js or full uncertainty ellipsoids. Deno notebook option linked, not required. |
| Stage 7 Rust | let/mut/struct/enum/match, ownership/borrowing/lifetimes, Option/Result, traits/iterators, Cargo/fmt/clippy | sys07 plus retained native Rust guides; actual capture validator and compiler failures. Clippy/fmt are learning commands unless execution records show them run. |
| Stage 8 Rust/Python | PyO3 extension over Rust validation | sys08 actual source over the tested Rust library. PyO3/maturin not resolved or compiled here; explicit blocked gate. |
| Stage 9 Go | Struct/interface/error/defer, goroutine/channel/context, HTTP/JSON/timeouts/cancellation/worker pools/shutdown | sys09; tested bounded service invokes compiled native Go only through an allowlisted lab. Actual local HTTP request recorded; not durable or production-authenticated orchestration. |
| Integrated capstone | Capture→Rust validation→Python science→C++ bottleneck→GPU optional→TS viewer; Go orchestration | run_demo implements C/Rust ingestion, Python fit, C++ trajectory, SQL audit, TS display; Go HTTP service tested separately with native Stage01. GPU and PyO3 are not connected without their own gates. |
| Support priorities | SQL, Swift as needed, exploratory Julia/Zig/Mojo, T-shaped depth | SQL joins/windows are in the worked experiment. Swift/Julia/Zig/Mojo remain explicitly exploratory and are not newly promised full language courses. |

## Deliberate integration decisions (our design, not quotations from the source)

- Keep Geoff on topology Stage 01. The source's systems Stage0 is an optional prerequisite repair, not a reason to redo completed topology orientation.
- Retain the already-built Go/Rust mathematics routes. The source's "Go later" guidance governs the service capstone, not a retroactive removal of existing Go labs.
- Do not require C++, GPU or Kubernetes before learning continuity or homology. The two layers advance when a useful project needs them.
- Keep Python as a scientific reference, Go/Rust as actual native calculations, C as byte/resource anatomy, C++ as geometry/topology kernel work, TypeScript as a validated display, and GPU as a measured optional acceleration path.
- Preserve old source/evidence files; create one new navigation layer rather than physically breaking imports and notebook data paths.
- Use one existing observed SPL excerpt across project boundaries. Its finite selected-frame average, ideal frame clock and tracking estimates are not independent physical ground truth.

## Qualifications not silently copied from the source

The unused two-`&mut` snippet in the source can compile under non-lexical lifetimes. Our failure fixture actually uses both borrows after creating the second, so the compiler conflict is demonstrated rather than assumed. `std::move` requests a move-compatible operation; it is not proof that no copy occurs for every type. A C struct's ABI layout is not our portable wire format. TypeScript types alone do not validate JSON.

The source includes dates, software-version statements, Windows lifecycle advice, tool recommendations and illustrative durations. This package does not independently certify every time-sensitive sentence. Installation references below were consulted for specific setup decisions; durations are study suggestions, not measured mastery or completion promises. No full external article, paid tutorial, model weights, private LinkedIn/account material, or compiler binary is republished here.

## Official implementation references consulted

- WSL environment/filesystem guidance: https://learn.microsoft.com/en-us/windows/wsl/setup/environment
- CUDA on WSL driver model: https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- CMake tutorial: https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- pybind11 build helpers: https://pybind11.readthedocs.io/en/stable/compiling.html
- PyO3 pinned source API: https://pyo3.rs/v0.23.5/getting-started
- PyTorch profiler: https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
- Rust ownership/borrowing: https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
- Go effective practices: https://go.dev/doc/effective_go
- Deno notebooks (optional): https://docs.deno.com/runtime/reference/cli/jupyter/

The original topology references, book-coverage audit, Poux register and native16 coverage ledger remain authoritative for their own scope. This source map adds no claims of full scientific equivalence or automatic learner mastery.
