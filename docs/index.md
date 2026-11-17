# Autonomy Kernel Lab

**Build an autonomous-driving research prototype, one visual experiment at a time.**

This course is aimed at an experienced ML engineer using an **Apple M2 MacBook Air
with 16 GB RAM**. It is designed for approximately **24 weeks / 10 hours per week**.

## What you will build

A small autonomous-driving pipeline that progressively adds:

1. GPU-aware preprocessing (Mojo and Python reference)
2. Camera perception
3. Sensor geometry, LiDAR projection, fusion, tracking and localization
4. Multi-agent motion prediction
5. Behavior and motion planning
6. Vehicle control
7. Closed-loop simulation and difficult-scenario evaluation
8. Runtime profiling and a GPU optimization portfolio

Every lesson contains a visualization you can manipulate, executable code, tests,
and a measurable exit criterion.

## Start now

- [Machine setup](setup.md)
- [Detailed roadmap](roadmap.md)
- [How to complete a lesson](workflow.md)
- [Lesson 01 — GPU tiling and camera-frame normalization](lessons/01-gpu-fundamentals.md)
- [Interactive GPU tile explorer](labs/gpu_tiles.html)
- [Interactive LiDAR / camera fusion explorer](labs/lidar_fusion_lab.html)

## Course rules

- Prefer **tiny reproducible scenes** over huge datasets.
- Run real **GPU experiments** on the M2 and keep CPU reference implementations.
- Distinguish **educational animations** from profiling real hardware.
- Keep sensor data, safety metrics, and failure cases visible.
- Treat the project as a research simulator, never as road-ready vehicle software.
