# How we will complete each lesson

## Deliverable contract

Each lesson has five artifacts:
1. **Concept notebook/page**: clear mental model with a small mathematical example.
2. **Interactive visualization**: change a parameter, break the system, explain the change.
3. **Reference implementation**: deterministic CPU or tested Python code.
4. **ML or GPU implementation**: optimized kernel or trained model, as appropriate.
5. **Evaluation**: unit tests, a quality/latency metric, and one analyzed failure.

## Suggested Git workflow

```bash
git checkout main
git pull
git checkout -b lesson/01-gpu-basics

# Implement, run tests, and update the evidence log.

git add .
git commit -m "Lesson 01: add frame normalization baseline"
git push -u origin lesson/01-gpu-basics
```

Open a Pull Request to `main`, review test outputs and visual evidence, then
merge when the exit criteria pass. Each merge automatically republishes the
website.

## Learning roles

- **You:** implement the exercise, make hypotheses, run measurements, explain failures.
- **Course mentor:** provide the next lesson specification, code-review the solution,
  refine the visualization, and propose increasingly realistic experiments.
- **CI:** run CPU reference tests and website-build checks. M2 GPU validation is local.

## Evidence standard

Do not write “10× faster” without specifying hardware, data shape, baseline,
warmup, synchronization, sample count, and p50/p95 measurement method.
A GPU kernel that is fast by itself may still lose end-to-end after launch
overheads or data transfers. Preserve both measurements.
