"""Camera-frame normalization baseline for Lesson 01.

The reference is vectorized NumPy and the tiled version is intentionally
a *CPU algorithm*. Neither is claimed to run a Mojo GPU kernel.
"""
from __future__ import annotations

import numpy as np

def normalize_frame(image: np.ndarray) -> np.ndarray:
    """Convert a uint8 H×W×C camera frame to float32 values in [0, 1]."""
    if image.ndim != 3 or image.shape[2] not in (1, 3, 4):
        raise ValueError("Expected H×W×C image with C=1, 3, or 4")
    if image.dtype != np.uint8:
        raise TypeError("Expected uint8 image")
    return image.astype(np.float32) * np.float32(1.0 / 255.0)

def normalize_frame_tiled(image: np.ndarray, tile_width: int = 32) -> np.ndarray:
    """CPU demonstration of tiling; for GPU experimentation later."""
    if not isinstance(tile_width, int) or tile_width < 1:
        raise ValueError("tile_width must be a positive integer")
    if image.ndim != 3 or image.shape[2] not in (1, 3, 4):
        raise ValueError("Expected H×W×C image with C=1, 3, or 4")
    if image.dtype != np.uint8:
        raise TypeError("Expected uint8 image")
    h, w, _ = image.shape
    out = np.empty(image.shape, dtype=np.float32)
    scale = np.float32(1.0 / 255.0)
    for x0 in range(0, w, tile_width):
        stop = min(w, x0 + tile_width)
        out[:, x0:stop, :] = image[:, x0:stop, :].astype(np.float32) * scale
    return out
