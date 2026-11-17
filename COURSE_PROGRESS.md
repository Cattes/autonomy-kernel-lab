# Milestone tracker

Each milestone is a Mojo module in `autonomy/` plus its GPU kernels, checked
against a NumPy reference.

Treat exit criteria as evidence-based: links to commits, benchmark output, screenshots,
and short failure analysis. A lesson is complete when both the **visual** and the
**technical** artifacts are ready.

| Weeks | Milestone | State | Evidence |
|---|---|---|---|
| 1–3 | Mojo foundations / camera frames | Not started | |
| 4–6 | Camera perception | Not started | |
| 7–9 | Geometry, LiDAR, fusion and tracking | Not started | |
| 10–12 | Motion prediction | Not started | |
| 13–15 | Behavior and planning | Not started | |
| 16–18 | Dynamics and control | Not started | |
| 19–21 | Scenario simulation and safety evaluation | Not started | |
| 22–24 | Integrated runtime and capstone | Not started | |

## Mojo kernel tracker

See [docs/mojo-track.md](docs/mojo-track.md). A kernel is done when it matches
its reference (including odd sizes) on the M2 and has kernel-only and
end-to-end timings.

| Kernel | Module | State | Mojo version | Evidence |
|---|---|---|---|---|
| K1 vector add | 01 | Not started | | |
| K2 frame normalize | 01 | Not started | | |
| K3 fused preprocessing | 02 | Not started | | |
| K4 box-IoU matrix | 02 | Not started | | |
| K5 point transform + projection | 03 | Not started | | |
| K6 BEV rasterization | 03 | Not started | | |
| K7 batched trajectory rollout | 04 | Not started | | |
| K8 ADE/FDE reductions | 04 | Not started | | |
| K9 trajectory costs + custom op | 05 | Not started | | |
| K10 MPPI rollouts | 06 | Not started | | |
| K11 batched scenario stepping | 07 | Not started | | |
| K12 fused GPU-resident pipeline | 08 | Not started | | |

## Experiment log template

- **Lesson / commit:**
- **Input sample + random seed:**
- **Machine / OS / dependency versions:**
- **Correctness checks:**
- **Latency:** p50 / p95, sample size, warmup and synchronization methodology
- **Model-quality metric:** definition, baseline, result
- **Visual evidence:** screenshot or replay link
- **What failed and why:**
- **Next hypothesis:**
