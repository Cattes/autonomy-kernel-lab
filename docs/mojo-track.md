# Mojo kernel track

Every module ships at least one **real Mojo GPU kernel that runs on the M2**,
next to its Python reference. The kernels get harder as the course goes on:
each one adds GPU concepts the previous ones didn't need. By week 24 you have
12 tested, benchmarked kernels that form one GPU-accelerated driving
pipeline.

Budget roughly **3–4 of the ~10 weekly hours** for this track. The
[Mojo GPU Puzzles](https://puzzles.modular.com/) are the drill exercises; the
kernels below are where you apply them to driving data.

## Kernel ladder

| Module | Kernel | New GPU concepts | Puzzles first |
|---|---|---|---|
| 01 GPU fundamentals | **K1** vector add (official tutorial) | threads, blocks, host ↔ device buffers, `synchronize()` | 1–3 |
| | **K2** camera-frame normalize: `uint8` HWC → `float32` | 2D grids, bounds guards, layout, kernel vs end-to-end timing | 4–8 |
| 02 Camera perception | **K3** fused resize + normalize + HWC→CHW | gather reads, bilinear interpolation, kernel fusion | 11, 13 |
| | **K4** pairwise box-IoU matrix for NMS | N×N work grids, shared-memory tiling, matmul-style reuse | 12, 16 |
| 03 LiDAR, fusion, tracking | **K5** point-cloud transform + camera projection | batched 4×4 transforms, structure-of-arrays layout | 2, 5 |
| | **K6** BEV rasterization (scatter into a grid) | scatter vs gather, **atomics** and contention, prefix-sum compaction | 14, 27 |
| 04 Motion prediction | **K7** batched multi-modal trajectory rollout | many tiny problems, per-thread loops | 6–7 |
| | **K8** minADE / minFDE + mode softmax | reductions, warp and block primitives | 15, 18, 24–26 |
| 05 Planning | **K9** candidate-trajectory cost evaluation | 3D work decomposition (trajectory × time × obstacle), argmin | 16, 19 |
| | Expose K9 to Python as a MAX custom op | Python ↔ Mojo interop | 17 |
| 06 Control | **K10** sampling-based MPC (MPPI) rollouts | thousands of parallel bicycle-model rollouts, weighted reduction | 27 |
| 07 Simulation & safety | **K11** batched scenario stepping + collision checks | one block per scenario, divergence, memory alignment | 35 |
| 08 Capstone | **K12** fuse your two hottest stages, keep data on the GPU | profiling-driven optimization, transfer elimination | review |

## Rules for every kernel

1. **Reference first.** A NumPy reference with tests lives in `src/autonomy_lab/`.
2. **Correctness.** The Mojo kernel matches the reference within a stated
   tolerance, including **odd sizes** that don't divide the block size.
3. **Two timings.** Report kernel-only and end-to-end (including host ↔ device
   copies) p50/p95, with warmup, synchronization and sample count. See the
   [workflow](workflow.md) evidence standard.
4. **One failure.** Write down one case where the GPU version is slower, wrong
   or surprising, and why.
5. **Location.** Code goes in `gpu/lessonNN/`. Record the Mojo version you tested
   with, since the API changes quickly.

## What works on the M2

Checked on this machine (Mojo 1.2.0, 2026-11-16):

- Kernel launch, host/device buffers and synchronization: **work**.
- Integer and `float32` atomic add (`from std.atomic import Atomic`): **work**.
  An 8-bin histogram over 4096 elements came out exact for both.

From the [GPU Puzzles support matrix](https://puzzles.modular.com/howto.html):

- **Work on Apple GPUs:** puzzles 1–8, 11–19, 23–28 and 35. That covers shared
  memory, reductions, prefix sum, matmul, MAX custom ops, and warp- and
  block-level operations.
- **NVIDIA-only:** the GPU debugger and sanitizer (9–10), PyTorch-driven
  puzzles (20–22), synchronization primitives, profiling, occupancy and bank
  conflicts (29–32), tensor cores (33) and clusters (34).

So on the Mac, you debug with small inputs, prints and comparisons against
the reference, and you profile with careful wall-clock timing. If the
capstone needs a real profiler or tensor cores, rent a cloud NVIDIA GPU for
that experiment.

## Track progress

Mark each kernel in [`COURSE_PROGRESS.md`](https://github.com/Cattes/autonomy-kernel-lab/blob/main/COURSE_PROGRESS.md)
when it passes its tests on the M2.
