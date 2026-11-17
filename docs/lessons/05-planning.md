# Behavior and motion planning

**Weeks 13–15 · Mojo compile-time metaprogramming**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Multiple candidate trajectories, collision zones, cost components, and selected path.

## Autonomy objective

Implement rule-based trajectory generation and scoring; investigate learned scoring.

## Data

[Argoverse 2](../datasets.md#argoverse-2-motion-forecasting) lane centerlines, drivable areas and other agents' tracks as planning scenarios, alongside synthetic ones.

## Mojo you'll learn

- **`comptime if` / `comptime for`:** unroll cost terms and specialize the
  planner at compile time.
- **Trait-based plugins:** each cost (collision, off-road, progress, comfort)
  implements a `Cost` trait, so planners are generic over their cost set.
- **Mojo from Python, properly:** expose the planner as a MAX custom op so a
  Python experiment can call it on GPU tensors.
- Builds `autonomy/planning.mojo`: trajectory sampling and pluggable costs.

## GPU kernels

**K9: trajectory cost evaluation.** Score K candidate trajectories × T
timesteps against M obstacles (collision distance, off-road, comfort) in one
kernel, then pick the best with a reduction. Find the K at which the GPU
beats NumPy end to end.

Then expose K9 to the Python planner as a **MAX custom op**, so Python calls
your kernel directly.

Puzzles first: 16 (tiled matmul), 17 (custom op), 19 (attention op).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

Collision/off-road/progress/comfort on deterministic scenarios.

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
