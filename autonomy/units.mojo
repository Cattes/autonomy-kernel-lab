"""Unit conversions and angle helpers: a worked example.

Shows the patterns you will reuse in every lesson:
- module-level `comptime` constants,
- plain functions on `Float64`,
- a function generic over any SIMD dtype and width, so the same code
  handles one value or a whole vector of values.
"""
from std.math import floor

comptime PI: Float64 = 3.141592653589793
comptime TWO_PI: Float64 = 2.0 * PI
comptime KPH_PER_MPS: Float64 = 3.6


def kph_to_mps(kph: Float64) -> Float64:
    """Convert kilometres per hour to metres per second."""
    return kph / KPH_PER_MPS


def mps_to_kph(mps: Float64) -> Float64:
    """Convert metres per second to kilometres per hour."""
    return mps * KPH_PER_MPS


def deg_to_rad(deg: Float64) -> Float64:
    return deg * (PI / 180.0)


def rad_to_deg(rad: Float64) -> Float64:
    return rad * (180.0 / PI)


def wrap_angle[
    dtype: DType, width: SIMDLength, //
](angle: SIMD[dtype, width]) -> SIMD[dtype, width]:
    """Wrap angles in radians to [-pi, pi).

    Heading errors in planning and control must be wrapped, or a car at
    179 degrees "steering to" -179 degrees turns the long way round.
    The `//` makes `dtype` and `width` inferred from the argument.
    """
    var two_pi = SIMD[dtype, width](TWO_PI)
    var pi = SIMD[dtype, width](PI)
    return angle - two_pi * floor((angle + pi) / two_pi)
