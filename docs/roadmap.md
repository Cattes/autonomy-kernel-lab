# 24-week roadmap

The course adds to **one growing prototype**, with one visual experiment and one
measurement package per module.

| Weeks | Subsystem | Visual lab | Mojo kernels | Exit evidence |
|---|---|---|---|---|
| 1–3 | GPU fundamentals | Animated tiles, memory layout, pipeline timing | K1 vector add, K2 frame normalize | Kernels match reference, timing methodology |
| 4–6 | Camera perception | Video masks, boxes, confidence, error inspection | K3 fused preprocessing, K4 IoU matrix | mIoU or mAP + latency |
| 7–9 | Geometry, LiDAR, fusion, tracking | Raw point cloud → calibrated camera overlay → BEV → tracks | K5 point transform/projection, K6 BEV rasterization | Reprojection + tracking / localization metrics |
| 10–12 | Prediction | Agent histories and alternative futures | K7 batched rollout, K8 ADE/FDE reductions | ADE/FDE and scenario breakdown |
| 13–15 | Planning | Candidate trajectories, costs, risk visualizer | K9 trajectory costs (+ MAX custom op) | Collision/off-road/progress/comfort |
| 16–18 | Control | Bicycle model animation and controller telemetry | K10 MPPI rollouts | Tracking error, jerk, acceleration |
| 19–21 | Simulation/evaluation | Scenario timeline and failure heatmap | K11 batched scenario stepping | Fixed reproducible safety evaluation |
| 22–24 | Runtime/capstone | Synchronized decision and runtime profiler | K12 fused, GPU-resident pipeline | End-to-end performance report |

The [Mojo kernel track](mojo-track.md) has the concepts each kernel teaches,
the GPU Puzzles to do first, and what works on the M2.

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

      Mojo GPU kernels (K1–K12) accelerate each stage, measured end to end.
```

Waymax supplies structured scene-state simulation; it is not a replacement
for a photorealistic camera/LiDAR renderer. We will initially develop camera
perception and Waymax simulation as separate exercises.

Research references:
- https://waymo.com/open/
- https://github.com/waymo-research/waymax
- https://max.modular.com/stable/gpu/intro-tutorial/
