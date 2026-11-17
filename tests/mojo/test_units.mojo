"""Mojo-side tests. Run all of them with `pixi run test-mojo`."""
from std.testing import assert_almost_equal, assert_true, TestSuite

from autonomy.units import PI, kph_to_mps, mps_to_kph, deg_to_rad, wrap_angle


def test_speed_round_trip() raises:
    assert_almost_equal(kph_to_mps(36.0), 10.0)
    assert_almost_equal(mps_to_kph(kph_to_mps(123.4)), 123.4)


def test_deg_to_rad() raises:
    assert_almost_equal(deg_to_rad(180.0), PI)


def test_wrap_angle_scalar() raises:
    assert_almost_equal(wrap_angle(Float64(3.0 * PI / 2.0)), -PI / 2.0)
    assert_almost_equal(wrap_angle(Float64(0.25)), 0.25)


def test_wrap_angle_simd() raises:
    # One call wraps four float32 angles at once.
    var angles = SIMD[DType.float32, 4](0.0, 4.0, -4.0, 7.0)
    var wrapped = wrap_angle(angles)
    for i in range(4):
        assert_true(wrapped[i] >= -Float32(PI) and wrapped[i] < Float32(PI))


def main() raises:
    TestSuite.discover_tests[__functions_in_module()]().run()
