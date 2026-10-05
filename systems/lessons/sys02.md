# sys02 — Modern C++: a real numerical project
**Source:** Stage 2 and its basketball-trajectory capstone. **Topology connection:** exact controls, H0 connectivity and MST at Stages 02/08/09, geometry at 14 and dynamics at 24.

## Explain the language decisions
C++20 is the explicit baseline in CMake. Value parameters make values available to the callee; references refer to existing objects; `const T&` communicates read-only access through that reference, not universal immutability of every alias. `auto` infers a type, while `const` limits mutation. Work through `test_concepts.cpp` before the numerical library.

`std::vector` owns a dynamic sequence; `std::array` has fixed size; `std::string` manages characters. `std::unordered_map` supports lookup but should not be trusted for a scientific output order without sorting. `std::optional` represents an absent value; `std::variant` represents alternatives. A missing observation must not be turned into a zero vector simply to avoid an optional case.

RAII ties resource cleanup to an object's lifetime. The vector buffers and file streams clean themselves up; `std::unique_ptr` models one owner when dynamic ownership is actually needed. Do not introduce `shared_ptr` merely because another language has garbage collection. It adds shared-ownership semantics that your design must justify.

Copying a vector creates separate element storage. `std::move` is a cast that permits move-aware overloads; it is not by itself a universal promise of a transfer or speedup. A moved-from standard object remains valid but its content may be unspecified. The concept test checks the destination, not an assumed source contents. Small templates such as `square<T>` explain type-general code; there is no requirement to learn template metaprogramming before topology. Use standard algorithms like accumulate/sort where they communicate intent.

## The project
`include/shape.hpp` declares the public interfaces. `src/shape.cpp` implements them. `tests/` contains independent exact controls. CMake builds a library, a trajectory executable and tests. This is a genuine project boundary: notebooks inspect outputs and do not replace the compiler.

The simple model is p(t)=p0+v0*t+(0,0,-g*t²/2). It assumes fixed gravity, no spin, no drag and no impacts. Its inputs must be finite, time nonnegative and g positive. `trajectory_cpp` validates CLI numbers including trailing garbage. It emits a CSV at specified sample times. Python independently calculates the same formula, fits initial state only on declared fitting rows, and evaluates later selected rows.

The topological kernel independently computes MST edge lengths and radius-connected components on bounded point sets. For a unit square, three MST edges each have length one; the radius graph has four components below one and one component at one. These H0 controls are not general persistent H1/H2 or alpha complexes. The existing native topology implementations remain the place for those covered protocols.

## Predict, implement and debug
Derive the projectile's z at t=0.5 from z0=2, vz=3 and g=9.81. Then inspect the CLI's conversion to the vector fields. Build with `cmake -S cpp -B build; cmake --build build; ctest --test-dir build --output-on-failure`. Use the private project's exact paths. Put a debugger breakpoint at `predict`, inspect p/v/t/g, step into validation, then inspect the return. A backtrace explains the caller chain, not the physics.

## Break and apply
Try negative gravity, nonfinite data, a malformed count and an empty MST cloud; predict the error. Add tests before changing the behavior. Compare an intentionally changed acceleration coefficient with the independent Python control: it should disagree. Restore it and rerun.

Only after correctness, measure CPU/wall time, allocation and repeated steady-state calls. Do not compare a fresh compilation against a warmed Python process. The provided project demonstrates boundaries and correctness; it does not claim a language-wide speedup. Later add spin only when you can define the state, force law and evidence for its parameters; a `spin` input with no modeled effect would be misleading.

## Exit gate
Explain value/reference, ownership, RAII, copying/moving, build/link/test steps, the model's assumptions, an exact topology control and the observed held-out error. Submit one private code change, a failing test followed by a repair, and a limitation statement.
