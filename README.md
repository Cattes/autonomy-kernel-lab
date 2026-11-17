# Autonomy Kernel Lab

**Learn Mojo and autonomous driving together: 24 weeks of building a self-driving
software stack in Mojo, on an M2 MacBook Air (16 GB).**

Each module adds one subsystem of the driving stack (camera, LiDAR and
tracking, prediction, planning, control, simulation) to the `autonomy/` Mojo
package, teaches the Mojo language features it needs, and adds GPU kernels
for its hot spots. Python checks the Mojo code against NumPy references and
draws the visualizations. The destination is a small **closed-loop
autonomous-driving simulator**, not road-ready vehicle software.

Course site: https://cattes.github.io/autonomy-kernel-lab/

## Start here (Apple silicon Mac)

Prerequisites: macOS 15+, Xcode 16+ with the Metal toolchain, Git, and
[Pixi](https://pixi.sh/) 0.84+. Everything else (Mojo, Python, NumPy, pytest,
docs tools) comes from one environment pinned by `pixi.lock`.

```bash
git clone https://github.com/Cattes/autonomy-kernel-lab.git
cd autonomy-kernel-lab
pixi install --all --locked
pixi run check-gpu      # GPU: Apple M2 | API: metal
pixi run test           # Mojo tests + Python checks of the Mojo code
pixi run docs           # course site at http://127.0.0.1:8000
pixi run fetch-data     # before Lesson 02: nuScenes mini + Argoverse 2 (needs a free nuScenes account)
```

See [docs/setup.md](docs/setup.md) for details and troubleshooting, and
[docs/mojo-track.md](docs/mojo-track.md) for what Mojo you learn when.

## Repository layout

- `autonomy/` — **the Mojo driving stack you build**, one module per lesson
  (`units.mojo` is a worked example)
- `tests/mojo/` — Mojo tests (`pixi run test-mojo`)
- `bindings/` — exposes `autonomy` to Python as `autonomy_py` (`pixi run build-py`)
- `src/autonomy_lab/` — NumPy reference implementations and visualization helpers
- `tests/` — pytest checks of the Mojo code against the references
- `scripts/` — benchmarks, test runner, GPU check
- `experiments/` — throwaway Mojo programs (tutorials, puzzles, probes)
- `docs/` — course site: lessons, roadmap, interactive labs
- `data/` — downloaded datasets (`pixi run fetch-data`), never committed; see `docs/datasets.md`
- `COURSE_PROGRESS.md` — milestones, kernel tracker, experiment log
- `.github/workflows/` — CI (Mojo + Python tests on Linux CPU) and site publishing

## Course site

Every push to `main` rebuilds the site from `docs/` and publishes it to
GitHub Pages (`.github/workflows/docs.yml`).

## Our working agreement

Each lesson is a small, reviewable PR:
1. Read the lesson on the site and play with its visual lab.
2. Write the NumPy reference, then the Mojo implementation, then the GPU kernel.
3. Run `pixi run test` and record results using fixed seeds and scenario IDs.
4. Explain at least one failure you found.
5. Check the lesson's exit criteria and merge into `main`.
6. Only then start the next lesson.

Use an issue titled `Lesson NN: <topic>` and a branch such as `lesson/01-mojo-foundations`.
GitHub Actions run the Mojo and Python tests on Linux CPUs. **GPU kernel tests run
locally on the M2**; they skip themselves in CI. Cloud NVIDIA checks are added only when needed.

For each lesson, keep input artifacts small; do not commit dataset files (nuScenes, Argoverse 2),
trained model checkpoints, credentials, or large binary captures.

## Scope and safety

Educational simulation only. The repo intentionally makes no safety certification
or on-road driving claims. Dataset permissions and privacy terms must be honored.
