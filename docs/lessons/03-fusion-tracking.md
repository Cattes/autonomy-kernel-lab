# Sensor geometry, LiDAR, fusion and tracking

**Weeks 7–9 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

3D point cloud, coordinate transforms, camera projection, BEV grid, and tracked agents.

## Code / ML objective

Transform points across LiDAR/ego/camera frames, rasterize BEV, then implement a tracker.

## Mojo kernel track

**K5: point-cloud transform + projection.** Apply the LiDAR→ego→camera 4×4
transforms and pinhole projection to every point. Try array-of-structs vs
structure-of-arrays layouts and measure the difference.

**K6: BEV rasterization.** Scatter points into a bird's-eye-view grid using
atomic adds (point count and mean intensity per cell), then compact the
occupied cells with a prefix sum. Measure how atomic contention changes with
grid resolution.

Puzzles first: 14 (prefix sum), 27 (block-wide operations and histogram binning).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

Reprojection error, track ID switches, and pose error on tiny scenarios.

## Required artifacts

- A runnable Python reference and tests.
- A parameterized visual replay of the transformation or decision.
- At least one sanity case and one intentionally broken case.
- Quantitative quality and performance results with methodology.
- A short report linking a screenshot, code commit, and test results.

## Constraints

Keep the first iteration synthetic or very small. Add large public datasets
only when the reference is proven. Do not use visual correctness as a
substitute for numerical testing.
