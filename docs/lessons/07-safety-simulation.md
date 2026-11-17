# Simulation and evaluation

**Weeks 19–21 · Packaging and testing Mojo at scale**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Scenario timeline, edge-case categories, heatmap of failures and near misses.

## Autonomy objective

Run a repeatable set of cut-in, occlusion, yielding and sensor degradation scenarios.

## Data

Scenarios replayed from [Argoverse 2](../datasets.md#argoverse-2-motion-forecasting) tracks and maps, plus synthetic edge cases (cut-ins, occlusions) you generate.

## Mojo you'll learn

- **Packaging:** build `autonomy` into a `.mojopkg` with `mojo precompile`
  and use it from a separate tool.
  ([packages](https://mojolang.org/docs/manual/packages/))
- **Deterministic randomness:** seeded RNG so every scenario replays exactly.
- **Larger test suites:** scenario-based regression tests that run in CI.
- Builds `autonomy/sim.mojo`: scenarios, collision checks, safety metrics.

## GPU kernels

**K11: batched scenario stepping.** Step many scenarios at once, one thread
block per scenario, including collision checks. Measure how divergent
behavior (scenarios ending at different times) affects throughput, and how
memory alignment affects it.

Puzzles first: 35 (memory alignment).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

Per-category outcomes; show one measurable regression and improvement.

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
