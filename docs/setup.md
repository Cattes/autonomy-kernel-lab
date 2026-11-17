# Machine setup (Apple M2 / 16 GB RAM)

One [Pixi](https://pixi.sh/) environment holds everything: Mojo/MAX, Python,
NumPy, pytest and the docs builder. It is pinned by `pixi.lock`, so a fresh
clone gets exactly the versions this course was tested with.

## 1. Prerequisites

- Apple silicon Mac, **macOS 15 or later**
- **Xcode 16 or later**, with the Metal toolchain (for GPU code)
- Git
- **Pixi 0.84 or newer**: install from https://pixi.sh/, update with
  `pixi self-update`. Older versions can't read the nightly MAX packages.

Check:

```bash
sw_vers
xcodebuild -version
xcodebuild -showComponent MetalToolchain   # Status should be: installed
pixi --version
```

If the Metal toolchain is missing or outdated:

```bash
xcodebuild -downloadComponent MetalToolchain
```

Modular's [hardware compatibility page](https://max.modular.com/gpu/hardware-compatibility/)
lists supported Apple chips (M1–M5).

## 2. Install

```bash
git clone https://github.com/Cattes/autonomy-kernel-lab.git
cd autonomy-kernel-lab
pixi install --all --locked
```

`--locked` fails instead of quietly installing different versions if
`pixi.lock` is out of date. There are two environments:

| Environment | Mojo | Use it for |
|---|---|---|
| `default` | 1.2.0 stable (MAX 26.7) | All lesson work; matches the official docs |
| `nightly` | latest `1.3.0.dev` build | Trying the newest compiler and APIs: `pixi run -e nightly ...` |

## 3. Verify

```bash
pixi run mojo-version   # Mojo 1.2.0
pixi run check-gpu      # GPU: Apple M2 | API: metal
pixi run test           # Mojo tests, then Python bindings + pytest
pixi run docs           # course site at http://127.0.0.1:8000
```

## 4. Get the data (before Lesson 02)

Lesson 01 needs no data. Before Lesson 02, create a free
[nuScenes account](https://www.nuscenes.org/sign-up), then:

```bash
pixi run fetch-data   # nuScenes mini (4.2 GB download) + 200 Argoverse 2 scenarios
pixi run check-data
```

See [Datasets](datasets.md) for licences, formats and options.

## Everyday commands

| Command | What it does |
|---|---|
| `pixi run test` | All Mojo tests (`tests/mojo/`) and all Python tests |
| `pixi run test-mojo` | Only the Mojo tests |
| `pixi run build-py` | Compile `bindings/autonomy_py.mojo` so Python can `import autonomy_py` |
| `pixi run mojo run -I . file.mojo` | Run any Mojo file that imports `autonomy` |
| `pixi run bench` | The preprocessing benchmark |
| `pixi run fetch-data` | Download the course datasets into `data/` |
| `pixi run check-data` | Check the datasets are complete and readable |
| `pixi run docs` | Serve the course site locally |
| `pixi shell` | A shell with `mojo`, `python` and `pytest` on the PATH |

Changing dependencies: edit `pixi.toml`, run `pixi install --all`, and commit
the updated `pixi.lock`. To try today's nightly, run `pixi update -e nightly`.
When a new stable MAX ships, bump the `max` pin deliberately.

## Resource limits (16 GB unified RAM)

- Start with synthetic inputs, then the course's small datasets (about 5 GB on disk).
- Load one sensor modality at a time when datasets are large.
- Downsample point clouds for exploration; keep an untouched sample elsewhere.
- 3D viewers, ML training and GPU kernels all share the same unified memory.
- Don't install CUDA on macOS; NVIDIA-only experiments use a rented cloud GPU.

## Troubleshooting

- **`failed to run the pass manager` when running GPU code:** the Metal
  toolchain is missing or mid-update. Check with
  `xcodebuild -showComponent MetalToolchain`, re-run the download command
  above, or retry after an update finishes.
- **Code from a blog post doesn't compile:** it probably predates Mojo 1.0.
  See the [Mojo 1.2 notes](mojo-track.md#mojo-12-notes).
- **`import autonomy_py` fails in Python:** run `pixi run build-py` first.
  `pixi run test` does this for you.

## Verified

2026-11-16 on an Apple M2 / 16 GB, macOS 26.6.2, Xcode 26.3, Metal toolchain
17C7003j, Pixi 0.84.2: both environments report `Apple M2` with API `metal`
and compile and run GPU kernels; `pixi run test` passes.
