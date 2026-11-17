import numpy as np
import pytest

from autonomy_lab.preprocess import normalize_frame, normalize_frame_tiled

def test_normalization_endpoints():
    frame = np.array([[[0, 255, 128]]], dtype=np.uint8)
    got = normalize_frame(frame)
    np.testing.assert_allclose(got, [[[0., 1., 128 / 255]]], rtol=0, atol=1e-7)
    assert got.dtype == np.float32

@pytest.mark.parametrize("tile_width", [1, 3, 16, 32, 128])
def test_tiled_odd_width(tile_width):
    frame = np.random.default_rng(7).integers(0, 256, size=(5, 37, 3), dtype=np.uint8)
    np.testing.assert_array_equal(normalize_frame_tiled(frame, tile_width), normalize_frame(frame))

@pytest.mark.parametrize("fn", [normalize_frame, normalize_frame_tiled])
def test_input_validation(fn):
    with pytest.raises(TypeError):
        fn(np.zeros((10, 10, 3), dtype=np.float32))
    with pytest.raises(ValueError):
        fn(np.zeros((10, 10), dtype=np.uint8))

def test_bad_tile_width():
    with pytest.raises(ValueError):
        normalize_frame_tiled(np.zeros((2, 2, 3), dtype=np.uint8), 0)
