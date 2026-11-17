"""Very small CPU baseline only — not a GPU benchmark.

Run with `pixi run bench`. Lesson 01 extends it with your Mojo versions
(through the `autonomy_py` bindings). For GPU measurements, use device
synchronization and time kernel-only and end-to-end separately.
"""
from __future__ import annotations

import statistics
import time
import numpy as np
from autonomy_lab.preprocess import normalize_frame, normalize_frame_tiled

def measure(fun, image, count=30):
    for _ in range(5):
        fun(image)
    readings = []
    for _ in range(count):
        t0 = time.perf_counter()
        fun(image)
        readings.append((time.perf_counter() - t0) * 1000)
    readings.sort()
    return statistics.median(readings), readings[int(0.95 * (count - 1))]

def main():
    rng = np.random.default_rng(7)
    for h, w in [(64, 64), (256, 256), (720, 1280)]:
        image = rng.integers(0, 256, size=(h, w, 3), dtype=np.uint8)
        a, b = measure(normalize_frame, image), measure(normalize_frame_tiled, image)
        print(f"{h}×{w}: NumPy CPU median/p95={a[0]:.3f}/{a[1]:.3f} ms; "
              f"tiled CPU median/p95={b[0]:.3f}/{b[1]:.3f} ms")
    print("These are CPU baselines. No claim is made about Mojo or GPU execution.")

if __name__ == "__main__":
    main()
