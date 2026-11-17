# Camera perception

**Weeks 4–6 · Mojo traits, generics and Python libraries from Mojo**

*Milestone contract: the full lesson is written when you reach it.*

## Visualization you will build

Driving video with object boxes, segmentation masks, confidence, and model error views.

## Autonomy objective

Train or evaluate a small perception model against a reference; feed it frames preprocessed by your Lesson 01 Mojo code.

## Data

[nuScenes mini](../datasets.md#nuscenes-mini) camera images (six cameras, 1600×900), with the 3D boxes projected into each image as ground truth.

## Mojo you'll learn

- **Traits and generics:** define an image-operation trait so resize,
  normalize and color conversion share one interface, generic over pixel
  `DType`. ([traits](https://mojolang.org/docs/manual/traits/),
  [parameters](https://mojolang.org/docs/manual/parameters/))
- **Compile-time parameters:** image size and channel count as parameters,
  so the compiler specializes the hot loops.
- **Calling Python from Mojo:** load frames and run a pretrained PyTorch model
  (on Apple's MPS backend) from Mojo, with Mojo doing preprocessing and
  postprocessing. ([Python interop](https://mojolang.org/docs/manual/python/))
- Builds `autonomy/camera.mojo` (resize, preprocessing) and
  `autonomy/detection.mojo` (boxes, IoU, NMS).

## GPU kernels

**K3: fused resize + normalize + HWC→CHW.** Replace the Lesson 01 normalize with
the full preprocessing a perception model needs, in one kernel. Compare
against the same three steps run as separate kernels.

**K4: pairwise box-IoU matrix.** Compute IoU for all N×N detection pairs on
the GPU, tiling boxes through shared memory. The greedy NMS loop can stay on
the CPU at first; measure where the crossover N is.

Puzzles first: 11 (pooling), 12 (dot product), 13 (convolution), 16 (matmul).

See the [Mojo learning path](../mojo-track.md) for the rules all Mojo code follows.

## Proof of completion

mIoU or mAP, per-scene failures, preprocessing and inference latency.

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
