# Autonomy Kernel Lab

**24 weeks of visual-first autonomous-driving ML and GPU programming, built incrementally on an M2 MacBook Air (16 GB).**

This is a self-study course *and* a growing research prototype. Each lesson adds code,
a visualization, tests, a benchmark, and a written reflection. The destination is a
small **closed-loop autonomous-driving simulator**, not road-ready vehicle software.

## Start here (M2 / macOS)

Prerequisites: Apple silicon Mac, macOS 15+, Xcode 16+ (with the Metal toolchain),
Git, [uv](https://docs.astral.sh/uv/) and [Pixi](https://pixi.sh/) 0.84+.
Both environments are pinned by lockfiles: `uv.lock` (Python 3.12, docs, tests)
and `gpu/pixi.lock` (Mojo/MAX). You can start the docs and Python lessons
before setting up Mojo.

```bash
git clone https://github.com/Cattes/autonomy-kernel-lab.git
cd autonomy-kernel-lab
uv sync --locked --extra dev     # creates .venv from uv.lock
uv run zensical serve
```

Open http://127.0.0.1:8000 and browse the course.

In another terminal, run:

```bash
uv run pytest -q
uv run python scripts/benchmark_preprocess.py
```

For the Mojo GPU environment on your M2:

```bash
cd gpu
pixi install --all --locked              # stable + nightly, from pixi.lock
pixi run mojo --version                  # Mojo 1.2.0 (stable, default)
pixi run -e nightly mojo --version       # newest nightly
```

If the Metal toolchain is missing, see `docs/setup.md`. Follow the official
GPU introduction for a first compiled GPU kernel:
https://max.modular.com/stable/gpu/intro-tutorial/

**Important:** The Python baseline and educational browser animations are included.
The first production Mojo GPU kernel is an exercise to implement with the official
tutorial; it is intentionally *not* represented as a finished working kernel.

## Course site and code live together

- `docs/` — published course pages, visual labs, milestone contracts
- `docs/labs/` — standalone interactive HTML visualizations, no server dependency
- `src/autonomy_lab/` — Python reference code shared between lessons
- `tests/` — correctness tests runnable on Mac and in CI
- `scripts/` — lightweight baseline experiments and benchmarks
- `gpu/` — M2-specific Mojo/MAX environment and kernel exercises
- `data/` — instructions for fetching small data samples; datasets are never committed
- `COURSE_PROGRESS.md` — completed work and notes
- `.github/workflows/` — CPU tests and automatic GitHub Pages publication

## Publish with GitHub Pages

1. Create an empty repository on GitHub called `autonomy-kernel-lab` (no README or .gitignore).
2. From this extracted folder:
   ```bash
   git init
   git add .
   git commit -m "Create visual autonomy course"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/autonomy-kernel-lab.git
   git push -u origin main
   ```
3. On GitHub select **Settings → Pages → Source: GitHub Actions**.
4. Open the **Actions** tab, and once the docs workflow completes,
   visit `https://YOUR_USERNAME.github.io/autonomy-kernel-lab/`.
5. Update `zensical.toml` with your actual `site_url` if you want canonical URLs.

Private repositories on GitHub Pages depend on your GitHub plan; read
https://docs.github.com/en/pages/ before choosing visibility.

## Our working agreement

Each lesson is a small, reviewable PR:
1. Read the lesson on the site and play with its visual lab.
2. Implement a baseline, then the acceleration/ML enhancement.
3. Run unit tests and record the results using fixed seeds and scenario IDs.
4. Explain at least one failure you found.
5. Check the lesson's exit criteria and merge into `main`.
6. Only then start the next lesson.

Use an issue titled `Lesson NN: <topic>` and a branch such as `lesson/01-gpu-basics`.
GitHub Actions test the Python/docs part of each PR. **Apple GPU kernel tests must be run
locally on the M2**, and cloud CUDA/Triton checks will be added only when needed.

For each lesson, keep input artifacts small; do not commit licensed Waymo datasets,
trained model checkpoints, credentials, or large binary captures.

## Scope and safety

Educational simulation only. The repo intentionally makes no safety certification
or on-road driving claims. Dataset permissions and privacy terms must be honored.
