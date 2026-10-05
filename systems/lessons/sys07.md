# sys07 — Rust: capture validation and ownership
**Source:** Stage 7. Your existing 57 native Rust units remain available; this project emphasizes the validator role described by the new path.

## Explain ownership before lifetime notation
An owned value controls the lifetime of its resources. Moving a String transfers ownership; using the moved-from binding afterward is invalid. Borrowing gives access without transferring ownership. `&T` is shared access; `&mut T` gives exclusive mutable access while that borrow is active. A slice borrows a region of a collection. Cloning a Vec creates an owned copy; copying a scalar has different cost and meaning.

Do not begin by memorizing `'a`. Ask which object owns the storage and how long the reference must remain valid. The compiler can use non-lexical lifetimes: a borrow that is never used again may end before the textual scope closes. Consequently, the two unused mutable references in the source's short sketch are not a reliable compile-failure test by themselves. Our `breakage/conflicting_borrows.rs` deliberately uses both after the second borrow, and produces E0499. The moved-value fixture separately produces its expected compiler error. This is an explicit qualification, not an unannounced rewrite of the source.

## Error states
`Option` represents absence; `Result` represents success or a named failure. Use structs/enums to express data rather than inventing sentinel coordinates. The binary contract stores confidence presence separately. The JSON validator emits code/location/message errors, so a caller can distinguish a duplicate frame from missing metadata or a failed hash.

The trajectory parser validates header, bounded count, byte length, fields, monotonic order and finite values before reporting a mean. The capture-manifest path checks camera IDs, dimensions, frame identity/time, relative paths, file existence, size and optional hashes. It rejects paths outside the selected root including symlink escapes. A full capture manifest and the original one-trial SPL excerpt are not the same input: we do not invent camera identities or image dimensions absent from the source.

## Build, predict, break
Cargo selects the crate; the lockfile pins dependencies; the vendored source configuration reuses the existing course crates. In a private prepared project, that configuration points back to the original vendor directory. Recreate the copy after moving the course rather than assuming the absolute path remains correct.

Predict the valid binary's count and unknown-confidence behavior. Run unit tests offline. Try truncation and a copied manifest with repeated camera/frame IDs. Inspect the structured errors. Then compile the isolated borrow and move failures, read the diagnostics and repair them without reflexively adding clones everywhere. The default valid application must not contain those intentional failures.

## Extend toward engineering
Traits can abstract a validator/predictor interface; iterators express transformations; typed units can prevent a pixels/metres mix. None of them proves the mathematical model is valid. A memory-safe parser can still implement the wrong unit conversion. `cargo fmt`, tests and clippy serve different purposes. Thread safety, Send/Sync and channel ownership belong to a later bounded concurrency exercise, not an automatic claim about every use of the tape in the existing native course.

## Exit gate
Explain the owner of each buffer, which functions borrow/mutate/allocate, the difference between absence and error, why the compile-fail fixture genuinely overlaps borrows, and what a successful manifest check cannot establish (calibration accuracy, consent, dataset rights or independent scientific validity).
