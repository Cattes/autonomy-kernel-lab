# Simulation and evaluation

**Weeks 19–21 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Scenario timeline, edge-case categories, heatmap of failures and near misses.

## Code / ML objective

Run a repeatable set of cut-in, occlusion, yielding and sensor degradation scenarios.

## Mojo kernel track

**K11: batched scenario stepping.** Step many scenarios at once, one thread
block per scenario, including collision checks. Measure how divergent
behavior (scenarios ending at different times) affects throughput, and how
memory alignment affects it.

Puzzles first: 35 (memory alignment).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

Per-category outcomes; show one measurable regression and improvement.

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
