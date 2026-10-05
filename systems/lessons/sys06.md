# sys06 — TypeScript: the application layer
**Source:** Stage 6. **Project:** trajectory evidence viewer; **connection:** topology Stage 11 representations and Stage 20 spatial evidence.

## Explain static types versus runtime data
JavaScript executes the program; TypeScript checks declared relationships before compilation and emits JavaScript. A JSON file is runtime input and is not made valid by a type assertion. Use `unknown`, test that it is an object, then narrow each field. `any` can bypass the very checks the exercise is meant to teach.

The source uses a discriminated union for loading/success/failure. Our `State` does the same: success has a validated trajectory; failure has an error. A switch on status determines which fields are available. Interfaces describe shape; type aliases can name unions; generics allow reusable functions while preserving relationships. Practice these concepts on the actual result schema, not unrelated syntax drills.

A Promise represents a result that will be available later. `async/await` is syntax for that asynchronous flow, not a separate thread. `File.text()` is awaited before parsing. Errors become a visible failure state. The file is never uploaded by this offline viewer.

## Implemented viewer
The input schema distinguishes observed and predicted trajectories, units=m, timestamps and limitations. Confidence may be null. `model.ts` performs runtime validation; it rejects wrong units, nonfinite values, non-increasing time, invalid confidence, missing trajectories and absent limitations. `viewer.ts` renders an orthographic projection of 3D coordinates with a horizontal viewing-angle slider. Observations and predictions use different line styles.

This is not a full Three.js renderer, learned reconstruction, calibrated camera view or production WMS frontend. Lines joining selected observations are display aids, not direct measurements at the intermediate times. This scope is displayed in the UI.

## Predict and build
Predict which fields are legal in each State alternative. Build with the project's tsc configuration; run the Node tests against the generated JavaScript. The current bundle was emitted using installed TypeScript 5.8.3. A reviewed npm lock should be resolved on a connected system; none is invented from a version string. Do not silently use a remote JavaScript CDN.

Load the `trajectory.json` produced by the integration demo. Change yaw and identify which view changes while the underlying data stay unchanged. Read the model's limitations before deciding what a curve means. The supplied file picker works locally; use a loopback HTTP server if your browser's local-file policy restricts your workflow.

## Break and apply
Try a copied file with units=ft, duplicate times or a string in x. A user-facing explanation should appear instead of a plausible but wrong plot. Add a new union state for unavailable geometry and make every display branch handle it. A schema version change should require a deliberate compatibility decision.

## Exit gate
Explain TypeScript's compile-time boundary, runtime validation, discriminated unions, async file reading, observed/predicted separation and the projection's limitations. Complete one private UI/validator change with a failing test and repair. Deno's native notebook kernel is an optional source-linked environment, not a requirement or an environment executed here.
