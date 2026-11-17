# 24-week roadmap

You learn **Mojo and autonomous driving together**: every module adds one
subsystem of the driving stack to the `autonomy/` Mojo package, teaches the
Mojo language features that subsystem needs, and adds GPU kernels for its
hot spots.

| Weeks | Module | Mojo language | GPU kernels | Visual lab | Exit evidence |
|---|---|---|---|---|---|
| 1–3 | [01 Mojo foundations](lessons/01-mojo-foundations.md) | Basics, structs, SIMD, tests, Python bindings | K1 vector add, K2 frame normalize | GPU tiles, memory layout | Four Mojo versions match NumPy; measured latency chart |
| 4–6 | [02 Camera perception](lessons/02-camera-perception.md) | Traits, generics, Python libraries from Mojo | K3 fused preprocessing, K4 IoU matrix | Masks, boxes, confidence, errors | mIoU or mAP + latency |
| 7–9 | [03 LiDAR, fusion, tracking](lessons/03-fusion-tracking.md) | Operators, ownership, spans, data layout | K5 point transform/projection, K6 BEV rasterization | Point cloud → camera overlay → BEV → tracks | Reprojection + tracking metrics |
| 10–12 | [04 Prediction](lessons/04-motion-prediction.md) | Collections, references, error handling | K7 batched rollout, K8 ADE/FDE reductions | Agent histories and alternative futures | ADE/FDE and scenario breakdown |
| 13–15 | [05 Planning](lessons/05-planning.md) | Compile-time metaprogramming, trait plugins | K9 trajectory costs (+ MAX custom op) | Candidate trajectories, costs, risk | Collision/off-road/progress/comfort |
| 16–18 | [06 Control](lessons/06-control.md) | Functions as parameters, closures, benchmarking | K10 MPPI rollouts | Bicycle model and controller telemetry | Tracking error, jerk, acceleration |
| 19–21 | [07 Simulation & safety](lessons/07-safety-simulation.md) | Packaging, deterministic RNG, test suites | K11 batched scenario stepping | Scenario timeline and failure heatmap | Reproducible safety evaluation |
| 22–24 | [08 Capstone](lessons/08-capstone.md) | Designing a Mojo system | K12 fused, GPU-resident pipeline | Synchronized decision replay and latency timeline | End-to-end performance report |

The [Mojo learning path](mojo-track.md) has the full language and kernel
ladders, the GPU Puzzles to do first, what works on the M2, and notes on
Mojo 1.2 syntax.

## Lesson release rule

We will write each future lesson **when we reach it**, based on the previous
milestone's results. The pages for lessons 02–08 are *milestone contracts*, not
fully authored lessons.

## Project data flow

```text
Sensor observation
    ├─ Perception ─────────────┐
    └─ Localization / map ─────┤
                              v
                       Tracking & prediction
                              |
                              v
                        Motion planning
                              |
                              v
                         Controller
                              |
                              v
                   Simulated vehicle dynamics
                              |
                 Closed-loop replay and metrics

      Every stage is Mojo code in autonomy/, checked against NumPy
      references; GPU kernels (K1–K12) accelerate the hot spots.
```

## Data

The course uses two small, real datasets; see [Datasets](datasets.md) for
licences, formats and how to download them with `pixi run fetch-data`.

| Dataset | Used in |
|---|---|
| [nuScenes mini](datasets.md#nuscenes-mini): 10 scenes of camera, LiDAR, radar, calibration and 3D boxes | 02 camera perception, 03 LiDAR, fusion and tracking |
| [Argoverse 2 motion forecasting](datasets.md#argoverse-2-motion-forecasting): agent tracks and lane maps | 04 prediction, 05 planning, 06 control, 07 simulation |

The closed-loop simulator for modules 06–08 is your own Mojo code (a
kinematic bicycle model stepping replayed scenarios), not a photorealistic
renderer. [Waymax](https://github.com/waymo-research/waymax) and the
[Waymo Open Dataset](https://waymo.com/open/) remain optional stretch goals:
they need a licence agreement, are large for 16 GB, and run mostly on the
CPU on a Mac.

References:
- https://www.nuscenes.org/nuscenes
- https://argoverse.github.io/user-guide/datasets/motion_forecasting.html
- https://max.modular.com/stable/gpu/intro-tutorial/
