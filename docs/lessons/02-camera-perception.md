# Camera perception

**Weeks 4–6 · Milestone contract (lesson content will be developed together)**

This is the roadmap-level contract for the module. Its detailed teaching
materials and exercises will be written after the preceding milestone.

## Visualization you will build

Driving video with object boxes, segmentation masks, confidence, and model error views.

## Code / ML objective

Train or evaluate a small perception model against a reference; connect its preprocessing to Lesson 01.

## Mojo kernel track

**K3: fused resize + normalize + HWC→CHW.** Replace the Lesson 01 normalize with
the full preprocessing a perception model needs, in one kernel. Compare
against the same three steps run as separate kernels.

**K4: pairwise box-IoU matrix.** Compute IoU for all N×N detection pairs on
the GPU, tiling boxes through shared memory. The greedy NMS loop can stay on
the CPU at first; measure where the crossover N is.

Puzzles first: 11 (pooling), 12 (dot product), 13 (convolution), 16 (matmul).

See the [Mojo kernel track](../mojo-track.md) for the rules every kernel follows.

## Proof of completion

mIoU or mAP, per-scene failures, preprocessing and inference latency.

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
