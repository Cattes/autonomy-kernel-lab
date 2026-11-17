# Integrated runtime and capstone

**Weeks 22–24 · Designing and optimizing a Mojo system**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Synchronized perception → prediction → planner → controller replay with a latency timeline.

## Autonomy objective

Integrate simplified pipeline and optimize a profiled GPU bottleneck.

## Mojo you'll learn

- **API design:** clean module boundaries between perception, prediction,
  planning and control.
- **Performance budgets:** measure every stage, then optimize the biggest one.
- **Keeping data on the GPU** across stages instead of copying back to the
  host between them.
- Builds `autonomy/runtime.mojo`: the integrated closed loop.

## GPU kernels

**K12: fuse and keep data on the GPU.** Profile the integrated pipeline, take
the two hottest adjacent stages, fuse them or chain them without copying
back to the host, and report the end-to-end gain against your earlier
kernels. Apple GPUs have no Mojo profiler, so use careful timing. Optionally
repeat the experiment on a rented NVIDIA GPU with its profiler.

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

Baseline vs optimized p50/p95; quality and safety metrics; clear limitations.

## Required artifacts

- Mojo implementation in `autonomy/` with Mojo tests.
- A NumPy reference, and pytest checks of the Mojo code against it.
- A parameterized visual replay of the transformation or decision.
- At least one sanity case and one intentionally broken case.
- Quantitative quality and performance results with methodology.
- A short report linking a screenshot, code commit, and test results.

## Constraints

Keep the first iteration synthetic or very small, and move to the course
datasets only when the reference is proven. Do not use visual correctness as a
substitute for numerical testing.
