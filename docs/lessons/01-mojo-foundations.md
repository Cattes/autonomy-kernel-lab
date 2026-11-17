# Lesson 01: Mojo foundations, from one pixel to the GPU

**Weeks 1–3 · Mojo basics, SIMD, multicore and GPU, applied to camera frames**

**Question:** A camera delivers `uint8` frames, and every perception model
wants `float32` input. How fast can you make that conversion in Mojo, and
what does each step (scalar → SIMD → multicore → GPU) actually buy you?

You will write the same small operation four ways:

\[
y_{h,w,c} = \frac{x_{h,w,c}}{255}
\]

It is simple on purpose. The interesting part is the language and the
hardware, not the math. At the end you will have your first `autonomy/`
module, its tests, Python bindings, and a measured chart comparing NumPy with
your four Mojo versions.

## Before you start

```bash
pixi run test        # Mojo tests + Python tests must pass
pixi run check-gpu   # should print: GPU: Apple M2 | API: metal
```

Read the worked example, which shows every pattern this lesson uses:

- [`autonomy/units.mojo`](https://github.com/Cattes/autonomy-kernel-lab/blob/main/autonomy/units.mojo): functions, `comptime` constants, a SIMD-generic function
- [`tests/mojo/test_units.mojo`](https://github.com/Cattes/autonomy-kernel-lab/blob/main/tests/mojo/test_units.mojo): Mojo tests with `TestSuite`
- [`bindings/autonomy_py.mojo`](https://github.com/Cattes/autonomy-kernel-lab/blob/main/bindings/autonomy_py.mojo): exposing Mojo to Python
- [`tests/test_units_bindings.py`](https://github.com/Cattes/autonomy-kernel-lab/blob/main/tests/test_units_bindings.py): checking Mojo against NumPy

Keep the [Mojo 1.2 notes](../mojo-track.md#mojo-12-notes) open; many examples
online use older syntax.

## Week 1: the language

**Read:** Mojo manual sections
[basics](https://mojolang.org/docs/manual/basics/),
[functions](https://mojolang.org/docs/manual/functions/),
[variables](https://mojolang.org/docs/manual/variables/),
[types](https://mojolang.org/docs/manual/types/),
[structs](https://mojolang.org/docs/manual/structs/),
[packages](https://mojolang.org/docs/manual/packages/) and
[testing](https://mojolang.org/docs/tools/testing/).

**Warm-up:** add `mps_to_kph` to the Python bindings and a pytest check for it.
You will touch all three layers (Mojo, binding, Python test) with a
one-line change.

**Exercise 1.1: a `Frame` type.** Create `autonomy/camera.mojo` with a struct
holding `height`, `width`, `channels` and the pixel bytes. Give it a
constructor that checks `channels` is 1, 3 or 4 (raise an `Error` otherwise)
and a method to read one pixel value at `(h, w, c)`.

**Exercise 1.2: scalar normalize.** Write `normalize_scalar`, a plain loop over
every byte that returns `float32` values. In `tests/mojo/test_camera.mojo`,
test 0 and 255, single-channel and RGBA frames, a 1×1 frame, and invalid
channel counts.

**Exercise 1.3: check it against NumPy.** Expose a function to Python that takes
a NumPy `uint8` array and fills a `float32` array (the
[notes](../mojo-track.md#mojo-12-notes) show how to get an array's memory in
Mojo). In pytest, compare it with `normalize_frame` from
`src/autonomy_lab/preprocess.py` on random frames of odd sizes.

## Week 2: making the CPU fast

**Read:** [SIMD types](https://mojolang.org/docs/manual/types/) and the
[`algorithm` docs](https://mojolang.org/docs/std/algorithm/).

**Exercise 1.4: SIMD.** Write `normalize_simd` using `vectorize`, so each step
converts a whole vector of bytes at once. Test it on lengths that are not a
multiple of the SIMD width.

**Exercise 1.5: multicore.** Write `normalize_parallel`: split the frame into rows
with `parallelize` and vectorize within each row.

**Measure.** Extend `scripts/benchmark_preprocess.py` to time NumPy and your
three Mojo versions at 64×64, 256×256 and 720×1280 through the bindings.
Then answer:

- At which frame size does `parallelize` start paying off, and why not
  earlier?
- How close does `normalize_simd` get to NumPy? NumPy runs compiled C here
  too.
- How much of your timing is the Python ↔ Mojo call itself? Measure an
  empty call.

## Week 3: the GPU

**Drill:** [GPU Puzzles](https://puzzles.modular.com/) 1–8 (map, zip,
guards, 2D map, broadcast, blocks, 2D blocks, shared memory). Clone the
puzzles repo separately and run them with `pixi run -e apple pXX`. Read the
manual's [GPU fundamentals](https://mojolang.org/docs/manual/gpu/fundamentals/).

**Explore:** [open the GPU tile explorer](../labs/gpu_tiles.html). It is a
**conceptual animation**, not a hardware trace. Use it to explain why
neighbouring threads reading neighbouring bytes (coalesced access) is faster
than strided access.

**K1: vector add.** Follow the
[official GPU tutorial](https://max.modular.com/stable/gpu/intro-tutorial/)
in `experiments/01_vector_add.mojo`. Confirm it runs on `Apple M2` and checks
every output element.

**K2: GPU normalize.** Add `normalize_gpu` to `autonomy/camera_gpu.mojo`: a
2D-grid kernel with one thread per pixel, guarded for widths that don't
divide your block size. Guard its tests with `has_accelerator()` so CI, which
has no GPU, skips them. Time kernel-only and end-to-end (including copies to
and from the GPU) separately.

- Where do launch and synchronization overhead show up?
- At what frame size, if any, does the GPU beat `normalize_parallel` end to
  end? Why can the kernel alone be fast while end to end loses?
- Why could a larger block size be slower?

*Stretch:* also produce channel-first (CHW) layout with per-channel mean/std,
which Lesson 02's model will need. Extend the Python reference first.

## Deliverables

- `autonomy/camera.mojo`, `autonomy/camera_gpu.mojo`, their Mojo tests, bindings and
  pytest checks against NumPy
- A chart of **measured** p50/p95 latency: NumPy, scalar, SIMD, parallel,
  GPU kernel-only, GPU end-to-end, at three frame sizes, with methodology
- One written failure or slowdown and its explanation
- Kernels K1 and K2 marked in `COURSE_PROGRESS.md` with the Mojo version used

## Exit checklist

- [ ] `pixi run test` passes, including your new Mojo and Python tests.
- [ ] All four Mojo versions match NumPy on odd-sized frames.
- [ ] K1 and K2 run on the M2 GPU.
- [ ] Latency chart and methodology recorded; one failure explained.
- [ ] You can explain, in your own words, what `vectorize`, `parallelize` and a
      GPU thread grid each parallelize over.

## Next

The `Frame` type and `normalize` become the input stage of
[Camera perception](02-camera-perception.md), where traits and generics let
the same preprocessing code handle different pixel types.
