# Vehicle control

**Weeks 16–18 · Mojo functions as values and benchmarking**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Animated bicycle model, target vs actual path, steering and jerk timeseries.

## Autonomy objective

Implement a kinematic bicycle simulator, PID tracker, and optionally small MPC.

## Data

Synthetic reference paths first, then [Argoverse 2](../datasets.md#argoverse-2-motion-forecasting) lane centerlines as real road geometry to track.

## Mojo you'll learn

- **Functions as parameters and closures:** pass dynamics models and
  controllers as compile-time function parameters.
- **Numerical integration** (Euler vs RK4) written once, generic over the
  model.
- **`std.benchmark`:** proper micro-benchmarks for controller latency
  budgets.
- Builds `autonomy/control.mojo`: kinematic bicycle model, PID, MPPI.

## GPU kernels

**K10: sampling-based MPC (MPPI).** Roll out thousands of noisy control
sequences through the kinematic bicycle model in parallel, score each one,
and compute the cost-weighted average control. Compare quality and latency
against the PID tracker at different sample counts.

Puzzles first: 27 (block-wide reductions).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

Cross-track error, heading error, acceleration and jerk.

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
