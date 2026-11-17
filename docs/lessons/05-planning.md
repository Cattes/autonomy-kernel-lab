# Behavior and motion planning

**Weeks 13–15 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Multiple candidate trajectories, collision zones, cost components, and selected path.

## Code / ML objective

Implement rule-based trajectory generation and scoring; investigate learned scoring.

## Mojo kernel track

**K9: trajectory cost evaluation.** Score K candidate trajectories × T
timesteps against M obstacles (collision distance, off-road, comfort) in one
kernel, then pick the best with a reduction. Find the K at which the GPU
beats NumPy end to end.

Then expose K9 to the Python planner as a **MAX custom op**, so Python calls
your kernel directly.

Puzzles first: 16 (tiled matmul), 17 (custom op), 19 (attention op).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

Collision/off-road/progress/comfort on deterministic scenarios.

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
