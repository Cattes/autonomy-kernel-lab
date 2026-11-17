# Sensor geometry, LiDAR, fusion and tracking

**Weeks 7–9 · Mojo value types, ownership and data layout**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

3D point cloud, coordinate transforms, camera projection, BEV grid, and tracked agents.

## Autonomy objective

Transform points across LiDAR/ego/camera frames, rasterize BEV, then implement a tracker.

## Data

[nuScenes mini](../datasets.md#nuscenes-mini): `LIDAR_TOP` sweeps, camera images, sensor calibration and ego poses for the transforms, and annotated boxes with track IDs for scoring the tracker.

## Mojo you'll learn

- **Operator overloading and value semantics:** `Vec3`, `Mat4` and `Pose` as
  SIMD-backed structs with `+`, `-` and `*`, so geometry code reads like the
  math. ([operators](https://mojolang.org/docs/manual/operators/))
- **Ownership and argument conventions:** `imm`, `mut`, `var` and `^` transfers
  when passing point clouds around without copying.
  ([ownership](https://mojolang.org/docs/manual/values/ownership/))
- **Spans and pointers:** views into large point buffers.
  ([pointers](https://mojolang.org/docs/manual/pointers/))
- **Data layout:** array-of-structs vs structure-of-arrays, measured.
- Builds `autonomy/geometry.mojo`, `autonomy/lidar.mojo` (BEV grid) and
  `autonomy/tracking.mojo` (Kalman filter, assignment).

## GPU kernels

**K5: point-cloud transform + projection.** Apply the LiDAR→ego→camera 4×4
transforms and pinhole projection to every point. Try array-of-structs vs
structure-of-arrays layouts and measure the difference.

**K6: BEV rasterization.** Scatter points into a bird's-eye-view grid using
atomic adds (point count and mean intensity per cell), then compact the
occupied cells with a prefix sum. Measure how atomic contention changes with
grid resolution.

Puzzles first: 14 (prefix sum), 27 (block-wide operations and histogram binning).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

Reprojection error, track ID switches, and pose error on tiny scenarios.

## Required artifacts

- Mojo implementation in `autonomy/` with Mojo tests.
- A NumPy reference, and pytest checks of the Mojo code against it.
- A parameterized visual replay of the transformation or decision.
- At least one sanity case and one intentionally broken case.
- Quantitative quality and performance results with methodology.
- A short report linking a screenshot, code commit, and test results.

## Constraints

Keep the first iteration synthetic or very small, and move to the course
datasets only when the reference is proven. Do not use visual correctness as a
substitute for numerical testing.
