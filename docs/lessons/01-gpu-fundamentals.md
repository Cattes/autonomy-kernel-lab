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
pytest -q
python scripts/benchmark_preprocess.py
```

Inspect `src/autonomy_lab/preprocess.py` and tests. Add one new test for
edge values (0 and 255) and one for a non-divisible tile size.

## GPU task (implement next)

Follow the [official Mojo GPU tutorial](https://max.modular.com/stable/gpu/intro-tutorial/)
until you have compiled vector addition and observed successful **M2 GPU**
device execution. Then implement image normalization as a new kernel in `gpu/`.

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
