# Lesson 01 — GPU tiles and image normalization

**Weeks 1–3 · Camera preprocessing meets GPU memory layout**

**Question:** If a camera provides a `uint8` image, how does the arrangement of
GPU work affect the cost of turning it into normalized floating-point input?

## Start with the animation

[Open the interactive GPU tile explorer](../labs/gpu_tiles.html)

Move through different tile widths and processing orders. The viewer is a
**conceptual animation**, not a hardware trace. Your task is to explain the
difference between consecutive and strided reads and why contiguous accesses
can improve throughput.

## Reference task

For an input `H × W × C` image of bytes, implement:

\[
y_{h,w,c} = \frac{x_{h,w,c}}{255}
\]

You'll compare a NumPy reference and a deliberately tiled CPU implementation
before writing a real Mojo GPU kernel.

```bash
uv run pytest -q
uv run python scripts/benchmark_preprocess.py
```

Inspect `src/autonomy_lab/preprocess.py` and tests. The endpoint (0/255) and
non-divisible tile cases are already covered. Add tests for single-channel and
RGBA frames (C=1 and C=4), and for a 1×1 frame. Your Mojo kernel will
need the same edge cases.

## Mojo kernel track

This module starts the [Mojo kernel track](../mojo-track.md) with two kernels.

**Drill first:** [GPU Puzzles](https://puzzles.modular.com/) 1–8 (map, zip,
guards, 2D map, broadcast, blocks, 2D blocks, shared memory). They all run on
the M2 with `pixi run -e apple pXX` in the puzzles repo.

**K1: vector add.** Follow the
[official Mojo GPU tutorial](https://max.modular.com/stable/gpu/intro-tutorial/)
and save the result as `gpu/lesson01/vector_add.mojo`. Confirm it reports
`Apple M2` and checks every output element.

**K2: camera-frame normalize.** Write `gpu/lesson01/normalize.mojo`: a 2D-grid
kernel turning a `uint8` H×W×C frame into `float32` in `[0, 1]`. Match
`normalize_frame` from the Python reference, including widths that don't
divide your block size. Time it at 64×64, 256×256 and 720×1280, reporting
kernel-only and end-to-end numbers separately.

*Stretch:* also output channel-first (CHW) layout with per-channel mean/std,
which is what Lesson 02's model will need. Extend the Python reference first.

Don't confuse Python loops, a browser animation, and **real GPU execution**.

### Questions to answer

- Why could a larger tile be slower?
- What does a memory coalescing pattern change?
- Where do launch and synchronization overhead occur?
- Can a fused preprocessing kernel beat NumPy? What about PyTorch MPS?
- What does performance look like at 64×64 versus 720×1280?

## Visualization deliverable

Save a screenshot or short screen capture of your tile explorer settings and
a separate *measured* latency chart from your real benchmark data. Display
both in the lesson page when finished.

## Exit checklist

- [ ] NumPy reference tests pass.
- [ ] Explain how a tile maps onto work items.
- [ ] Official Mojo GPU vector-add tutorial runs on the M2.
- [ ] Your first Mojo preprocessing kernel matches the reference within tolerance.
- [ ] Record median/p95 kernel and end-to-end timings with methodology.
- [ ] Publish a chart and an observed failure or slowdown.

## Next integration

This normalization function becomes the input transform used in the
[Camera Perception](02-camera-perception.md) module.
