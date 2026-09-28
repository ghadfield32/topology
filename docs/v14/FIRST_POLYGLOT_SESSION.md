# First polyglot session: Stage 01

You are already on Stage 01, so do not restart Stage 00.

## 1. Python reference
```powershell
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_python_v14_01
```

## 2. Go
```powershell
python polyglot.py run --lang go --lab stage01
```
Read `polyglot/go/labs/stage01.go`. Reimplement `rankMod2` in a private copy, then test the 3x3 matrix by hand.

## 3. Rust
```powershell
python polyglot.py run --lang rust --lab stage01
```
Read `polyglot/rust/src/labs/stage01.rs` and `helpers.rs`. Reimplement the rank elimination after you can explain ownership of the copied matrix.

## 4. Compare
Write `my_work/polyglot/stage01/comparison.md` covering:
- why the real and F2 ranks differ;
- what data each implementation owns/mutates;
- how Go returns errors versus Rust `Result`;
- why passing the same test in three languages is not three independent scientific datasets.

## 5. Poux bridge
After the Stage 01 gate, run:
```powershell
python curriculum/extensions/poux_spatial_ai/bridge.py --repo . --output my_work/poux_bridge01
python polyglot.py run --lang go --lab poux_bridge
python polyglot.py run --lang rust --lab poux_bridge
```
Derive the count-weighted chunk mean first. Explain why the centroid is not a release point or a time average.
