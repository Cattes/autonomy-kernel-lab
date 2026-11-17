# Multi-agent motion prediction

**Weeks 10–12 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Past tracks and animated competing future trajectories with probabilities.

## Code / ML objective

Start with constant velocity and fit a small sequence predictor using limited Waymo Motion scenes.

## Mojo kernel track

**K7: batched trajectory rollout.** Roll out every agent × every predicted mode
over the horizon in parallel (constant velocity first, then your model's
outputs).

**K8: metrics on the GPU.** Compute ADE/FDE per mode, minADE/minFDE per agent,
and a softmax over mode scores using warp- and block-level reductions.

Puzzles first: 15 (axis sum), 18 (softmax), 24–26 (warp operations).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

ADE/FDE and minADE/minFDE on held-out scenes; inspect missed modes.

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
