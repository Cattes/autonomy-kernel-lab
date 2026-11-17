# Vehicle control

**Weeks 16–18 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Animated bicycle model, target vs actual path, steering and jerk timeseries.

## Code / ML objective

Implement a kinematic bicycle simulator, PID tracker, and optionally small MPC.

## Mojo kernel track

**K10: sampling-based MPC (MPPI).** Roll out thousands of noisy control
sequences through the kinematic bicycle model in parallel, score each one,
and compute the cost-weighted average control. Compare quality and latency
against the PID tracker at different sample counts.

Puzzles first: 27 (block-wide reductions).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

Cross-track error, heading error, acceleration and jerk.

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
