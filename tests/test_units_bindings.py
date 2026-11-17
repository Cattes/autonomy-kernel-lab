"""Check Mojo functions against a NumPy reference, called from Python.

This is the pattern for every lesson: NumPy is the oracle, Mojo is the
implementation, pytest compares them on many inputs.
"""
import numpy as np
import pytest

autonomy_py = pytest.importorskip("autonomy_py", reason="run `pixi run build-py` first")


def test_kph_to_mps():
    assert autonomy_py.kph_to_mps(36.0) == pytest.approx(10.0)


@pytest.mark.parametrize("angle", np.random.default_rng(7).uniform(-20, 20, 50))
def test_wrap_angle_matches_numpy(angle):
    reference = (angle + np.pi) % (2 * np.pi) - np.pi
    assert autonomy_py.wrap_angle(float(angle)) == pytest.approx(reference, abs=1e-12)
