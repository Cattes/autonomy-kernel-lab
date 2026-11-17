# How we will complete each lesson

## Deliverable contract

Each lesson has five artifacts:
1. **Concept page**: a clear mental model with a small mathematical example.
2. **Interactive visualization**: change a parameter, break the system, explain the change.
3. **NumPy reference**: small, obviously-correct Python code in `src/autonomy_lab/`.
4. **Mojo implementation**: the real thing, in `autonomy/`, plus GPU kernels where
   they pay off. Mojo tests in `tests/mojo/`, and pytest checks against the
   reference through `bindings/autonomy_py.mojo`.
5. **Evaluation**: a quality and latency metric, and one analyzed failure.

The [Mojo learning path](mojo-track.md) lists the rules all Mojo code follows.

## Suggested Git workflow

While the course itself is still being prepared, changes go straight to
`main`. Once lessons start, each one is a branch and a pull request:

```bash
git checkout main
git pull
git checkout -b lesson/01-mojo-foundations

# Implement, run `pixi run test`, and update the evidence log.

git add .
git commit -m "Lesson 01: scalar normalize in Mojo"
git push -u origin lesson/01-mojo-foundations
```

Open a pull request to `main`, review test output and visual evidence, then
merge when the exit criteria pass. Each merge republishes the website.

## Learning roles

- **You:** implement the exercise, make hypotheses, run measurements, explain failures.
- **Course mentor:** provide the next lesson specification, code-review the solution,
  refine the visualization, and propose increasingly realistic experiments.
- **CI:** runs the Mojo tests (on CPU), the Python tests against your Mojo bindings,
  and the website build, on Linux. GPU tests skip themselves there; GPU
  validation happens on your M2.

## Evidence standard

Do not write “10× faster” without specifying hardware, data shape, baseline,
warmup, synchronization, sample count, and p50/p95 measurement method.
A GPU kernel that is fast by itself may still lose end-to-end after launch
overheads or data transfers. Preserve both measurements.
