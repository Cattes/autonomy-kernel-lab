# Sensor geometry, LiDAR, fusion and tracking

**Weeks 7–9 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

3D point cloud, coordinate transforms, camera projection, BEV grid, and tracked agents.

## Code / ML objective

Transform points across LiDAR/ego/camera frames, rasterize BEV, then implement a tracker.

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
