# sys00 — What is the computer actually doing?
**Source:** Stage 0 of the supplied systems-learning path. **Topology connection:** Stage 01 matrices/fields and Stage 18 data layout. **Project:** C memory/layout experiment plus the existing native Stage 01.

## Explain: start at a byte, not a language ranking
A bit has two states; eight bits form a byte in this project's format. Hexadecimal is a compact way to display bit patterns. A declared type tells the program how to interpret those patterns. The bytes `00 00 80 3f` can be interpreted as a little-endian float32 value or as an integer; neither interpretation follows merely from seeing four bytes. Endianness specifies the order of bytes within a multibyte scalar. Dtype, shape and storage order are separate parts of an array contract.

Unsigned arithmetic has defined modular behavior in C; signed overflow is not a safe substitute. The demo prints unsigned wrap without invoking signed overflow. IEEE floating point has finite precision and special values. Addition can lose low-order information, and changing summation order may change a numerical result. Never infer exact scientific equality solely from rounded display. In Stage 01, distinguishing real arithmetic from F2 arithmetic is a different issue again: the coefficient field changes the mathematical operation, not just rounding.

A pointer stores an address-like value referring to an object. It is not the object's content and is not a physical-RAM coordinate you should compare across executions. A process has an address space; the operating system maps virtual memory. Registers and caches are hardware resources involved in executing instructions. A thread shares a process's address space but has its own execution state. A data race is not prevented merely because two variables have different names.

A Python list of integers is not the same representation as C's contiguous `int[3]` or a C++ `std::vector<int>`. A vector owns a dynamic buffer plus bookkeeping; a Python list stores references to Python objects. A NumPy array has another explicit storage/dtype contract. Stack and heap are useful starting concepts, but language semantics and compiler decisions are not fully described by labeling every variable 'stack'. Inspect the behavior you can measure and state platform details.

## Compilation and operating-system boundary
The compiler translates a source representation through intermediate stages to object code. Linking resolves symbols and combines object files/libraries. A static library is an archive of object code; a shared library is loaded with a runtime/linker contract. A system call crosses into operating-system services. SIMD applies operations to multiple lanes; it is not a guarantee that arbitrary Python loops or C++ code become vectorized.

Follow one real invocation: Python creates a NumPy/Torch value; a scientific library selects compiled code; an accelerator operation may launch a CUDA kernel; GPU threads use registers, shared memory and VRAM. This course's new host has no usable CUDA device, so the hardware diagram is not a recorded GPU execution trace.

## Predict and implement
Prepare sys00 with `learn.py project`. The C project contains `memory_demo.c`. Predict why assigning through `int *p=&x` changes x. Predict the unsigned wrap. Do not hard-code a struct's total size from a diagram: padding/alignment are ABI-dependent. Build with CMake, run `memory_demo`, and explain `sizeof(Observation)` and `offsetof(frame)` on your machine. The portable trajectory format instead specifies fields byte by byte.

## Break and apply
In a private copy, compare a shallow container copy with an independent copy in each existing native language. Change one element and test caller-visible mutation. Then inspect the NPY/PNG source-decoder checks in `native/`: a matching filename or shape is not enough; endian order, values, channels and missingness also matter.

## Exit gate
Explain bits/bytes, signed/unsigned, floating point, pointer/value, ownership, process/thread, compilation/linking and dtype/shape/order. Trace one Stage 01 matrix from disk to computation to result. Name something the trace does not establish, such as biological manifold dimension or a performance ranking. Register/cache/virtual-memory/SIMD internals become targeted deeper readings, not prerequisites for finishing this finite exercise.
