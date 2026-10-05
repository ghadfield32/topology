# Optional development-container boundary

Use VS Code Remote–WSL first, with real toolchains and the existing uv environment in the Linux filesystem. The task requested Jupyter plus real projects, not a compulsory development container.

No untested omnibus image is declared ready. The existing Dockerfiles handle native batch execution; systems/deploy handles the small Go service. Their build dependencies and acceptance are separate. A full interactive development image needs C/C++/CMake, Node/tsc, Go, Rust/linker, the real Python lock and optional GPU/OpenCV/PyO3 tooling. Add and verify those only when the corresponding lesson requires them.

Do not overwrite an existing devcontainer.json in your repo. The new VS Code task file is named tasks.v17.example.json intentionally: merge its entries into your current configuration after review.
