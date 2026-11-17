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

Install Pixi: https://pixi.sh/

```bash
cd gpu
pixi install
pixi run mojo --version
```

The `gpu/pixi.toml` specifies the currently documented `max==26.7` stack.
If package availability changes, update the manifest deliberately and commit
the lockfile generated on your M2. Use the official GPU introduction:
https://max.modular.com/stable/gpu/intro-tutorial/

We will implement the first real Mojo kernel as a lesson deliverable.
A browser-based GPU animation is **not** proof that Mojo GPU code ran.

## 4. Resource limits (16 GB unified RAM)

- Start with synthetic inputs and short (10–30 s) real scenes.
- Only load one sensor modality at a time when datasets are large.
- Downsample point clouds for exploration; keep an untouched source sample externally.
- Treat 3D viewers and ML training as competing for unified memory.
- Don't install CUDA on macOS; CUDA/Triton tests will use cloud NVIDIA later.

## 5. Quick acceptance checklist

- [ ] `pytest -q` passes.
- [ ] Site launches via `zensical serve`.
- [ ] Both browser labs open.
- [ ] `pixi run mojo --version` runs on M2.
- [ ] Real GPU device discovered using official tutorial.
