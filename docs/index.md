# Autonomy Kernel Lab

**Learn Mojo by building a self-driving car's software stack, one visual experiment at a time.**

This course is for an experienced ML engineer who wants to learn **Mojo** and
**autonomous-driving systems** at the same time, on an **Apple M2 MacBook Air
with 16 GB RAM**. It takes about **24 weeks at 10 hours per week**.

## What you will build

A small autonomous-driving stack written in Mojo, the `autonomy` package,
growing module by module:

1. Camera-frame processing: Mojo basics, SIMD, multicore and your first GPU kernels
2. Camera perception: traits, generics and Python interop
3. Sensor geometry, LiDAR, fusion and tracking: value types, ownership, atomics
4. Multi-agent motion prediction: collections, references, GPU reductions
5. Behavior and motion planning: compile-time metaprogramming, custom ops
6. Vehicle control: functions as parameters, parallel MPC rollouts
7. Closed-loop simulation and safety evaluation: packaging, batched simulation
8. An integrated, profiled runtime that keeps data on the GPU

Every lesson has a visualization you can manipulate, Mojo code with tests,
a NumPy reference to check it against, and a measurable exit criterion.

## Start now

- [Machine setup](setup.md)
- [Mojo learning path](mojo-track.md): what Mojo you learn when, and Mojo 1.2 notes
- [Detailed roadmap](roadmap.md)
- [Datasets](datasets.md): nuScenes mini and Argoverse 2, and how to download them
- [How to complete a lesson](workflow.md)
- [Lesson 01: Mojo foundations, from one pixel to the GPU](lessons/01-mojo-foundations.md)
- [Interactive GPU tile explorer](labs/gpu_tiles.html)
- [Interactive LiDAR / camera fusion explorer](labs/lidar_fusion_lab.html)

## Course rules

- **Mojo first.** The stack is Mojo; Python checks it, visualizes it and trains models.
- Prefer **small real datasets and tiny reproducible scenes** over huge datasets.
- Run real **GPU experiments** on the M2 and keep reference implementations.
- Distinguish **educational animations** from measurements on real hardware.
- Keep sensor data, safety metrics and failure cases visible.
- Treat the project as a research simulator, never as road-ready vehicle software.
