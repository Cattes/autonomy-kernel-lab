# 24-week roadmap

The course adds to **one growing prototype**, with one visual experiment and one
measurement package per module.

| Weeks | Subsystem | Visual lab | Exit evidence |
|---|---|---|---|
| 1–3 | GPU fundamentals | Animated tiles, memory layout, pipeline timing | 3 kernels, correctness tests, timing methodology |
| 4–6 | Camera perception | Video masks, boxes, confidence, error inspection | mIoU or mAP + latency |
| 7–9 | Geometry, LiDAR, fusion, tracking | Raw point cloud → calibrated camera overlay → BEV → tracks | Reprojection + tracking / localization metrics |
| 10–12 | Prediction | Agent histories and alternative futures | ADE/FDE and scenario breakdown |
| 13–15 | Planning | Candidate trajectories, costs, risk visualizer | Collision/off-road/progress/comfort |
| 16–18 | Control | Bicycle model animation and controller telemetry | Tracking error, jerk, acceleration |
| 19–21 | Simulation/evaluation | Scenario timeline and failure heatmap | Fixed reproducible safety evaluation |
| 22–24 | Runtime/capstone | Synchronized decision and runtime profiler | End-to-end performance report |

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

      GPU kernels optimize measured bottlenecks across the stages.
```

Waymax supplies structured scene-state simulation; it is not a replacement
for a photorealistic camera/LiDAR renderer. We will initially develop camera
perception and Waymax simulation as separate exercises.

Research references:
- https://waymo.com/open/
- https://github.com/waymo-research/waymax
- https://max.modular.com/stable/gpu/intro-tutorial/
