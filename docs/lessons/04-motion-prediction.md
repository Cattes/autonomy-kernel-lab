# Multi-agent motion prediction

**Weeks 10–12 · Mojo collections, references and error handling**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Past tracks and animated competing future trajectories with probabilities.

## Autonomy objective

Start with constant velocity, then fit a small sequence predictor on Argoverse 2 scenarios.

## Data

[Argoverse 2 motion forecasting](../datasets.md#argoverse-2-motion-forecasting): 5 s of observed agent tracks and 6 s of ground-truth future per scenario, plus the lane map. Start with the 200 scenarios `pixi run fetch-data` downloads.

## Mojo you'll learn

- **Collections:** `Dict` of agent id → history, `Optional` for missing
  observations, `List`s of structs.
- **Structs that own other structs**, and references with origins so you can
  read histories without copying them.
- **Error handling:** `raises`, custom errors for malformed scenes.
  ([errors](https://mojolang.org/docs/manual/errors/))
- Python's role: train a small sequence model in PyTorch; Mojo handles
  features, rollouts and metrics.
- Builds `autonomy/prediction.mojo`: agent histories, baselines, ADE/FDE.

## GPU kernels

**K7: batched trajectory rollout.** Roll out every agent × every predicted mode
over the horizon in parallel (constant velocity first, then your model's
outputs).

**K8: metrics on the GPU.** Compute ADE/FDE per mode, minADE/minFDE per agent,
and a softmax over mode scores using warp- and block-level reductions.

Puzzles first: 15 (axis sum), 18 (softmax), 24–26 (warp operations).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

ADE/FDE and minADE/minFDE on held-out scenes; inspect missed modes.

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
