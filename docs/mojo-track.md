# Mojo learning path

This course teaches **Mojo and autonomous driving together**. You build the
driving stack in Mojo, lesson by lesson, in the `autonomy/` package. Each
module teaches a slice of the Mojo language, at least one GPU kernel, and
one subsystem of a self-driving car. You learn each piece of Mojo at the
point where the driving problem needs it.

## Who writes what

| Language | Role | Lives in |
|---|---|---|
| **Mojo** | The driving stack itself: data types, algorithms, CPU and GPU kernels | `autonomy/`, `tests/mojo/` |
| Mojo → Python | Exposes your Mojo functions to Python | `bindings/autonomy_py.mojo` |
| Python | NumPy reference implementations (test oracles), data loading, visualization, ML training | `src/autonomy_lab/`, `tests/`, `scripts/` |

Python stays where Mojo isn't the right tool yet. Training neural networks
uses PyTorch (with Apple's MPS GPU backend), plotting uses matplotlib or the
browser labs, and NumPy is the independent "known good" answer your Mojo
code is checked against.

## Language ladder

Each module introduces new Mojo concepts, used immediately in the stack.

| Module | Mojo language | Mojo performance & GPU | Builds in `autonomy/` |
|---|---|---|---|
| 01 Mojo foundations | `def`, `var`, types, `raises`, structs, `List`, SIMD types, modules and packages, `TestSuite` tests, calling Mojo from Python | `vectorize`, `parallelize`, first GPU kernels | `camera`: frame type and normalization (scalar → SIMD → multicore → GPU) |
| 02 Camera perception | Traits, generics, compile-time parameters, calling Python libraries (NumPy, PyTorch) from Mojo | Fused kernels, shared-memory tiling | `camera`: resize, preprocessing; `detection`: boxes, IoU, NMS |
| 03 Geometry, LiDAR, fusion, tracking | Operator overloading, value semantics, ownership and argument conventions (`imm`, `mut`, `var`, `^`), `Span` and pointers, data layout | Atomics, scatter, prefix sum | `geometry`: `Vec3`, `Pose`, transforms; `lidar`: BEV grid; `tracking`: Kalman filter |
| 04 Motion prediction | Collections (`Dict`, `Optional`), structs that own other structs, origins and references, error handling | Reductions, warp and block primitives | `prediction`: agent histories, rollouts, ADE/FDE |
| 05 Planning | Compile-time metaprogramming (`comptime if`/`for`), trait-based plugins | Python-callable MAX custom ops | `planning`: trajectory generation, pluggable costs |
| 06 Control | Functions as parameters and closures, numerical integration, `std.benchmark` | Thousands of parallel rollouts (MPPI) | `control`: bicycle model, PID, MPPI |
| 07 Simulation & safety | Packaging (`mojo precompile`), deterministic RNG, larger test suites | Batched simulation, divergence, alignment | `sim`: scenarios, collision checks, metrics |
| 08 Capstone | Designing a Mojo codebase: APIs, layering, performance budgets | Kernel fusion, GPU-resident pipeline | `runtime`: the integrated loop |

## GPU kernel ladder

| Module | Kernel | New GPU concepts | GPU Puzzles first |
|---|---|---|---|
| 01 | **K1** vector add (official tutorial) | threads, blocks, host ↔ device buffers, `synchronize()` | 1–3 |
| | **K2** camera-frame normalize | 2D grids, bounds guards, kernel vs end-to-end timing | 4–8 |
| 02 | **K3** fused resize + normalize + HWC→CHW | gather reads, bilinear interpolation, fusion | 11, 13 |
| | **K4** pairwise box-IoU matrix for NMS | N×N grids, shared-memory tiling | 12, 16 |
| 03 | **K5** point-cloud transform + projection | batched 4×4 transforms, structure-of-arrays layout | 2, 5 |
| | **K6** BEV rasterization | scatter vs gather, **atomics**, prefix-sum compaction | 14, 27 |
| 04 | **K7** batched multi-modal trajectory rollout | many tiny problems, per-thread loops | 6–7 |
| | **K8** minADE / minFDE + mode softmax | reductions, warp and block primitives | 15, 18, 24–26 |
| 05 | **K9** candidate-trajectory costs (+ MAX custom op) | 3D work decomposition, argmin, Python interop | 16, 17, 19 |
| 06 | **K10** MPPI rollouts | parallel bicycle-model rollouts, weighted reduction | 27 |
| 07 | **K11** batched scenario stepping | one block per scenario, divergence, alignment | 35 |
| 08 | **K12** fused, GPU-resident pipeline | profiling-driven optimization, transfer elimination | review |

The [Mojo GPU Puzzles](https://puzzles.modular.com/) are the drills; the
kernels are where you apply them to driving data.

## Rules for every piece of Mojo code

1. **Reference first.** A NumPy reference with tests in `src/autonomy_lab/`.
2. **Mojo tests.** `tests/mojo/test_<module>.mojo`, run by `pixi run test-mojo`.
3. **Cross-check from Python.** Expose the function in `bindings/autonomy_py.mojo`
   and compare it against the NumPy reference in pytest on many random inputs.
4. **Edge cases.** Odd sizes that don't divide the SIMD width or GPU block
   size, empty and 1-element inputs, extreme values.
5. **Two timings for GPU code.** Kernel-only and end-to-end (including
   host ↔ device copies) p50/p95, with warmup, synchronization and sample
   count. See the [workflow](workflow.md).
6. **One failure.** Write down one case where your Mojo version was slower,
   wrong or surprising, and why.

`autonomy/units.mojo` is a worked example that already follows all of these.
Read it, its tests and its binding before writing your first module.

## What works on the M2

Checked on this machine with Mojo 1.2.0 (2026-11-16):

- Structs, traits, generics, SIMD, `vectorize`, `parallelize`, Python interop
  in both directions, and `TestSuite` tests: **work**.
- GPU kernel launch, host/device buffers, synchronization: **work**.
- Integer and `float32` atomic add: **work** (exact results on a histogram test).

From the [GPU Puzzles support matrix](https://puzzles.modular.com/howto.html):
puzzles 1–8, 11–19, 23–28 and 35 run on Apple GPUs. The GPU debugger,
sanitizer, profiler, occupancy, bank-conflict and tensor-core puzzles are
NVIDIA-only. On the Mac you debug with small inputs, prints and comparison
against the reference, and you measure with careful timing. If the capstone
needs a real profiler, rent a cloud NVIDIA GPU for that experiment.

## Mojo 1.2 notes

Mojo changes quickly, and most blog posts and older examples predate 1.0.
These are the differences we hit while setting up this course:

| Topic | Mojo 1.2 |
|---|---|
| Standard library imports | `from std.math import sqrt`, `from std.testing import ...` |
| GPU and CPU-parallel APIs | `from max.gpu import thread_idx`, `from max.gpu.host import DeviceContext`, `from max.algorithm import parallelize` |
| Functions that can fail | `def` no longer implies `raises`; write `def main() raises:` |
| Argument conventions | `imm` (read-only borrow, the default), `mut`, `var` (owned; pass with `x^` to transfer). The old `read` keyword was removed |
| List literals | `[1, 2, 3]` is a fixed-size `Array`; write `var xs: List[Int] = [1, 2, 3]` for a growable list |
| `Span` | Built in, no import needed: `def total(s: Span[Int, _]) -> Int` accepts a `List` |
| Tests | No `mojo test` command. A test file's `main` runs `TestSuite.discover_tests[__functions_in_module()]().run()` |
| Compile-time code | `comptime X = ...`, `comptime if`, `comptime for` |
| Inferred parameters | Put `//` after parameters that should be inferred: `def f[dtype: DType, width: SIMDLength, //](x: SIMD[dtype, width])` |
| SIMD width parameter type | `SIMDLength`, not `Int` |
| `parallelize` | `parallelize(func, num_work_items)`, the function is an argument |
| Pointers | `UnsafePointer` is deprecated in favor of `Pointer`; `ptr.load`/`ptr.store` are now `unsafe_load`/`unsafe_store` |
| Atomics | `from std.atomic import Atomic`, then `Atomic.fetch_add(ptr, value)` |
| Python → Mojo | `PythonModuleBuilder` in `std.python.bindings`. Build with `pixi run build-py`; the automatic `mojo.importer` can't see the `autonomy` package and doesn't rebuild when imported files change |
| NumPy arrays in Mojo | `UnsafePointer[Float32, MutAnyOrigin](unsafe_from_address=Int(py=arr.ctypes.data))` gives you the array's memory |

## References

- [Mojo manual](https://mojolang.org/docs/manual/) and
  [standard library](https://mojolang.org/docs/std/)
- [Official GPU tutorial](https://max.modular.com/stable/gpu/intro-tutorial/)
- [Mojo GPU Puzzles](https://puzzles.modular.com/)
