# sys01 — C: machine-facing fundamentals
**Source:** Stage 1, compilation, primitive data, pointers, arrays, stack/heap, structs and `trajectory_binary_reader`. **Existing connection:** topology Stages 01, 02 and data-contract work. C is the source's anatomy lesson, not a demand to rewrite the scientific course.

## Explain
The expression `&x` obtains a pointer to x; `*p` accesses the referred object while that object remains valid. A pointer carries no general array-length guarantee. For every buffer, keep a pointer and a length, and prove an index is within that length before dereferencing it. `size_t` is for sizes, fixed-width integers for a wire-format contract, and `double` for the binary64 fields after validating the representation. `sizeof(pointer)` is not the allocated array's size.

`malloc(n)` asks for n bytes; it may fail. A successful allocation requires exactly one eventual release by its owner. A double free, use after free, leak, dangling pointer, null dereference and buffer overflow are different failure modes. Our default reader uses fixed local buffers and no row allocation: it reads a 12-byte header and then one 48-byte record at a time. Its memory use is bounded even when record count is large. That statement describes this format reader, not every downstream operation or all LiDAR formats.

A C struct is convenient in memory but not a portable file format. Compiler padding and endian order are why `trajectory_read` decodes unsigned integers explicitly and copies binary64 bits with `memcpy` rather than violating aliasing or alignment rules. The output summary is assigned only on success. A failed parse must not leave a plausible partly valid result for later analysis.

## Build the compiler pipeline once
From your private project directory, inspect these steps (paths may need the project include directory):
```
cc -E -Iinclude src/trajectory.c -o trajectory.i
cc -S -Iinclude src/trajectory.c -o trajectory.s
cc -c -Iinclude src/trajectory.c -o trajectory.o
```
Preprocessing expands includes/macros; compilation emits assembly; assembling produces an object; linking connects the object to callers and libraries. The complete project uses CMake so those dependencies are recorded. Compiler/linker errors are distinct: missing headers differ from unresolved definitions.

## Predict
Read `systems/contracts/TRAJECTORY.md`. Calculate the expected byte size for 12 rows: `12 + 12*48 = 588`. Determine which bytes store the first timestamp. The confidence flag is zero because the provider excerpt has no confidence values; its placeholder scalar must not be described as confidence zero. Frame/sample-rate time is not synchronized camera time.

## Implement
Prepare the project, inspect each parser function, compile with warnings, and run `trajectory_reader data/trajectory.bin`. Explain the observed row count, mean and time range. Compare with independent Python and Rust calculations. Do not equate this selected-frame mean with a time-weighted mean. Change a copied frame ID or truncate a record and predict the rejected condition before running it.

## Break, in isolation
`breakage/use_after_free.c` is intentionally unsafe. Compile it with AddressSanitizer/UndefinedBehaviorSanitizer in a disposable output directory, run only that manufactured example, and read the allocation/free/read stack locations. A nonzero exit and a matching diagnostic are the expected outcome. Do not place this program in an ordinary production target or run fault experiments on authoritative files. A sanitizer finding no problem on a valid run is finite test evidence, not a proof of memory safety.

## Apply and exit
Write a second explicit field decoder or add a versioned optional field in your private format. Update tests for valid input, wrong magic, truncation, excessive count, trailing bytes, nonfinite coordinates, confidence flags and ordering. Explain every buffer boundary and resource lifetime. Once you can do this, follow the source's direction to move to modern C++ instead of getting trapped in unrelated C syntax.
