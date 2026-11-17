# Machine setup (Apple M2 / 16 GB RAM)

This setup separates lightweight documentation/Python work from the Mojo/MAX GPU environment.

## 1. Tools and prerequisites

- Apple silicon M2, **macOS 15 or later**
- **Xcode / Xcode Command Line Tools 16 or later**
- Python 3.11+, Git and a browser
- Pixi for the Mojo MAX toolchain

Check:

```bash
sw_vers
xcodebuild -version
python3 --version
git --version
```

If your macOS installation needs the Metal toolchain:

```bash
xcodebuild -downloadComponent MetalToolchain
```

Modular compatibility docs:
https://max.modular.com/gpu/hardware-compatibility/

## 2. Install the Python reference code and site generator

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
zensical serve
```

Open `http://127.0.0.1:8000/` for the course website.

## 3. Install Mojo/MAX separately

Install Pixi (https://pixi.sh/), version **0.84 or newer**. Older versions
cannot read the nightly MAX package metadata. Update with `pixi self-update`.

```bash
cd gpu
pixi install --all
pixi run mojo --version             # stable: Mojo 1.2.0 (MAX 26.7)
pixi run -e nightly mojo --version  # nightly: Mojo 1.3.0.devYYYYMMDDHH
```

`gpu/pixi.toml` defines two environments:

| Environment | Channel | Use it for |
|---|---|---|
| `default` | `conda.modular.com/max` | Lesson work; matches the official docs (`max==26.7`) |
| `nightly` | `conda.modular.com/max-nightly` | Trying the newest compiler and APIs |

Refresh the nightly with `pixi update -e nightly`. When a new stable MAX
ships, bump the `max` pin deliberately and commit the regenerated
`pixi.lock`. Use the official GPU introduction:
https://max.modular.com/stable/gpu/intro-tutorial/

Nightly builds can deprecate APIs the tutorial still uses (for example
`ctx.name()` → `ctx.device().get_name()` in 1.3.0.dev). If a tutorial
snippet warns or fails on nightly, try it on `default` first.

We will implement the first real Mojo kernel as a lesson deliverable.
A browser-based GPU animation is **not** proof that Mojo GPU code ran.

## 4. Resource limits (16 GB unified RAM)

- Start with synthetic inputs and short (10–30 s) real scenes.
- Only load one sensor modality at a time when datasets are large.
- Downsample point clouds for exploration; keep an untouched source sample externally.
- Treat 3D viewers and ML training as competing for unified memory.
- Don't install CUDA on macOS; CUDA/Triton tests will use cloud NVIDIA later.

## 5. Quick acceptance checklist

- [x] `pytest -q` passes.
- [x] Site launches via `zensical serve`.
- [x] Both browser labs open.
- [x] `pixi run mojo --version` runs on M2.
- [x] Real GPU device discovered using official tutorial.

Verified on 2026-11-16, Apple M2 / 16 GB, macOS 26.6.2, Xcode 26.3, Metal
toolchain 17C7003j, Pixi 0.84.2, Python 3.14.3. Both Mojo environments
report `Apple M2` with API `metal`, and both compile and run a GPU kernel.

If a GPU kernel fails with `failed to run the pass manager`, check the Metal
toolchain with `xcodebuild -showComponent MetalToolchain`. Re-run
`xcodebuild -downloadComponent MetalToolchain` if it is missing, or retry
after an update finishes.
