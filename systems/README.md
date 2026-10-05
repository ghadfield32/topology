# Notebook → understand it. Project → engineer it.

This track integrates the supplied systems-learning path into the existing topology course. It does not reset Stage 01 or turn topology into six copies of the same curriculum. The theory lives in `lessons/`; your established Go/Rust scientific implementations remain in `native/`; this directory adds focused engineering projects around those foundations.

## Two layers, one repository
The **learning/research layer** is a short notebook: explain a question, predict one result, execute a bounded experiment, inspect evidence. The **engineering layer** is the source project: actual compiler, build manifest, tests, debugger, warnings, sanitizers, profiling and Git. A notebook that starts `cargo` is an orchestration notebook, not a Rust kernel; the binary still computes in Rust. A Python workbook must run its scientific reference rather than merely admire a previous Go output.

Follow the source's **Explain → Predict → Implement → Break → Apply** pattern. Break means a controlled invalid input or isolated fault with a stated expected diagnostic, never corruption of the authoritative dataset or production service. Finish by recording what surprised you, what failed, why, the Python equivalent and where the idea could help your work.

## Source stages and roles
The source announces nine stages but labels Stage 0 through Stage 9. We preserve those ten labels as sys00–sys09 so they cannot be confused with the 31 topology stages.

| Source stage | Here | Role |
|---|---|---|
| 0 | [sys00](lessons/sys00.md) | Computer representation, memory, compilation |
| 1 | [sys01](lessons/sys01.md) | C binary reader and memory boundaries |
| 2 | [sys02](lessons/sys02.md) | C++20 numerical/topological library |
| 3 | [sys03](lessons/sys03.md) | pybind11/Python boundary |
| 4 | [sys04](lessons/sys04.md) | OpenCV image layout and geometry |
| 5 | [sys05](lessons/sys05.md) | Profile → transfers → compile/precision → Triton → CUDA |
| 6 | [sys06](lessons/sys06.md) | TypeScript validation and result viewer |
| 7 | [sys07](lessons/sys07.md) | Rust ownership and capture validation |
| 8 | [sys08](lessons/sys08.md) | PyO3 native extension |
| 9 | [sys09](lessons/sys09.md) | Go bounded worker service |

Do not begin all ten simultaneously. Continue your topology Stage 01. Use sys00/01 to understand representation and memory when needed; keep the existing Go/Rust Stage 01 exercise. The source's suggestion to study service-oriented Go later is not a reason to discard native Go already implemented. The TypeScript application track can proceed in parallel after you understand the result schema. GPU work waits for a measured bottleneck and working CPU reference.

## Concrete project and data boundary
The integration demo uses the retained SPL selected ball observations. Their frame-derived clock, feet-to-metres conversion, unknown confidence and one-trial limitation remain explicit. C reads a new documented portable binary derived from those rows. Rust independently validates it. Python fits a bounded initial state; C++ evaluates a fixed-gravity trajectory. SQL checks row identities and grouped errors. TypeScript validates and displays observed/predicted coordinates. The Go service separately schedules allowed native Go labs with a bounded queue. CUDA/Triton and optional PyO3/OpenCV builds never become passed simply because their source files exist.

## How to work
`python learn.py project --unit sys01 --output my_work/sys01_practice01` makes a private project and data copy. Read its START.md, predict, edit `project/`, then run `python learn.py check-project --workspace my_work/sys01_practice01 --output my_work/sys01_practice01/attempt01`. That command compiles YOUR copied source. The original course remains unchanged. Copying reference code alone is guided practice; your independent change and explanation are separate evidence.

Every result belongs in a new directory. Keep the first failed attempt. A sanitizer detecting an intentionally faulty program is expected failure evidence, not a reason to report the unsafe program as a successful application. No automatic learner grades are assigned.
