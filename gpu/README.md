# M2 Mojo GPU lab

This environment is specifically for **Apple silicon macOS**, not for the
Linux GitHub Actions runners.

```bash
pixi install --all --locked
pixi run mojo --version
```

Go through the official GPU intro tutorial:
https://max.modular.com/stable/gpu/intro-tutorial/

Then follow the [Mojo kernel track](../docs/mojo-track.md): kernels K1–K12,
one folder per lesson (`lesson01/`, `lesson02/`, ...). Lesson 01 starts with:
- `lesson01/vector_add.mojo` (K1: follow tutorial, verify real GPU output)
- `lesson01/normalize.mojo` (K2: your exercise, match Python reference)
- A measured benchmark comparing end-to-end vs kernel-only execution.

Mojo and MAX GPU APIs are evolving quickly. Keep the actual working kernel
source and the Pixi lockfile together, and document which version was tested
on your M2. This starter intentionally ships without unverified Mojo source.

## Verified on this M2 (2026-11-16)

- macOS 26.6.2, Xcode 26.3, Metal toolchain 17C7003j, pixi 0.84.2
- `default` env: `max==26.7` → **Mojo 1.2.0 (2016d0cd)**, the latest stable
- `nightly` env: **Mojo 1.3.0.dev2026111605 (ea4e6261)**
- Both: `DeviceContext()` reports **Apple M2**, API **metal**, and a GPU kernel
  compiles, launches and synchronizes

```bash
pixi install --all --locked
pixi run mojo file.mojo              # stable (use for lessons)
pixi run -e nightly mojo file.mojo   # newest nightly
pixi update -e nightly               # pull today's nightly
```

Mojo 1.x gotchas if you read older blog posts or examples:

- Standard library imports are prefixed with `std.`: `from std.sys import has_accelerator`
- GPU APIs live in the `max` package: `from max.gpu import thread_idx, block_idx`,
  `from max.gpu.host import DeviceContext`
- Atomics: `from std.atomic import Atomic`; int32 and float32
  `Atomic.fetch_add` both work on the M2
- `UnsafePointer` is deprecated in favor of `Pointer` (it still compiles,
  with a warning)
- `def` no longer implies `raises`; write `def main() raises:` when calling
  anything that can fail (e.g. creating a `DeviceContext`)
