# M2 Mojo GPU lab

This environment is specifically for **Apple silicon macOS**, not for the
Linux GitHub Actions runners.

```bash
pixi install
pixi run mojo --version
```

Go through the official GPU intro tutorial:
https://max.modular.com/stable/gpu/intro-tutorial/

Then implement:
- `lesson01/vector_add.mojo` (follow tutorial, verify real GPU output)
- `lesson01/normalize.mojo` (your exercise, match Python reference)
- A measured benchmark comparing end-to-end vs kernel-only execution.

Mojo and MAX GPU APIs are evolving quickly. Keep the actual working kernel
source and the Pixi lockfile together, and document which version was tested
on your M2. This starter intentionally ships without unverified Mojo source.

## Verified on this M2 (2026-11-16)

- macOS 26.6.2, Xcode 26.3, pixi 0.65.0
- `max==26.7` → `mojo --version` = **Mojo 1.2.0 (2016d0cd)**
- `DeviceContext()` reports **Apple M2**, API **metal**; `has_accelerator()` = True

Mojo 1.x gotchas if you read older blog posts or examples:

- Standard library imports are prefixed with `std.`: `from std.sys import has_accelerator`
- GPU APIs live in the `max` package: `from max.gpu import thread_idx, block_idx`,
  `from max.gpu.host import DeviceContext`
- `def` no longer implies `raises`; write `def main() raises:` when calling
  anything that can fail (e.g. creating a `DeviceContext`)
