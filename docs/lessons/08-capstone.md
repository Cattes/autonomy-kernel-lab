# Integrated runtime and capstone

**Weeks 22–24 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Synchronized perception → prediction → planner → controller replay with a latency timeline.

## Code / ML objective

Integrate simplified pipeline and optimize a profiled GPU bottleneck.

## Mojo kernel track

**K12: fuse and keep data on the GPU.** Profile the integrated pipeline, take
the two hottest adjacent stages, fuse them or chain them without copying
back to the host, and report the end-to-end gain against your earlier
kernels. Apple GPUs have no Mojo profiler, so use careful timing. Optionally
repeat the experiment on a rented NVIDIA GPU with its profiler.

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

Baseline vs optimized p50/p95; quality and safety metrics; clear limitations.

## Required artifacts

- A runnable Python reference and tests.
- A parameterized visual replay of the transformation or decision.
- At least one sanity case and one intentionally broken case.
- Quantitative quality and performance results with methodology.
- A short report linking a screenshot, code commit, and test results.

## Constraints

Keep the first iteration synthetic or very small. Add large public datasets
only when the reference is proven. Do not use visual correctness as a
substitute for numerical testing.
