# sys03 — C++ ↔ Python with pybind11
**Source:** Stage 3. **Role:** keep Python for investigation and expose the already tested C++ kernel rather than maintaining another formula inside the binding.

## Explain the boundary
A native extension is a compiled library imported into a particular Python runtime. The function signature is a contract about types, shapes, ownership and errors. Python lists converted into C++ vectors imply copying; a NumPy-buffer interface would require a separate dtype/stride/lifetime design. The current binding intentionally uses simple sequences to keep the first boundary inspectable. Do not advertise it as zero-copy.

`bindings.cpp` wraps `shape::predict` and `shape::mst_deaths`. Its three-coordinate check occurs before constructing Vec3. C++ validation exceptions become Python errors through pybind11. The mathematical kernel is shared with the CLI, so a Python import is another access path to the same implementation, not an independent mathematical algorithm. The separate Python formula is the independent control.

## Predict and build
Predict `shape_cpp.predict([0,0,2],[1,0,3],.5)` before importing it. CMake uses the active Python interpreter and Development.Module. The usual build finds a separately installed pybind11 configuration. This delivery also supports an explicitly specified inspected header directory; its build used headers already shipped in the installed PyTorch distribution. Those headers and the compiler are not copied into the ZIP.

Prepare sys03, then check the private project. The `SHAPE_PYBIND` target compiles an actual extension. Import the resulting file with the same Python that configured it; inspect `module.__file__`. Do not copy a Linux `.so` into a Windows environment or treat a matching filename as ABI compatibility.

## Break
Try a two-coordinate position and negative time. Explain where each fails. Deliberately change the kernel in the private project, rebuild, restart the Python process and verify the changed behavior is visible. An old imported module in a live kernel can survive a filesystem rebuild; fresh processes avoid mistaking stale loaded code for the new code.

## Apply and benchmark
Use the measured-data demo: Python defines the fit/test protocol, C++ evaluates the model, Python compares predictions and plots residuals. A useful benchmark separates wrapper conversion, native computation and end-to-end application latency. For tiny vectors the boundary overhead may dominate. Record an observed result before concluding that moving code was worthwhile.

The source's pybind11 path is implemented here. OpenCV-specific native work is the next optional project. General distribution wheels, release CI across OS/architectures, zero-copy NumPy buffers and GIL-release behavior are deeper exercises, not automatically passed by this simple module.

## Exit gate
Explain how Python finds the compiled library, where data copies occur, which source contains the actual model, how an exception crosses the boundary, and why comparing the CLI with its own binding is not an independent scientific validation. Show the separate Python calculation and one invalid-input test.
