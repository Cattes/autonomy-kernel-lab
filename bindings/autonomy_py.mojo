"""Python bindings for the `autonomy` Mojo package.

Build with `pixi run build-py`; Python then does `import autonomy_py`
(tests/conftest.py puts build/ on sys.path). Add one `def_function` line
per Mojo function you want to test or visualize from Python.
"""
from std.os import abort
from std.python import PythonObject
from std.python.bindings import PythonModuleBuilder

from autonomy.units import kph_to_mps, wrap_angle


@export
def PyInit_autonomy_py() abi("C") -> PythonObject:
    try:
        var m = PythonModuleBuilder("autonomy_py")
        m.def_function[py_kph_to_mps]("kph_to_mps", docstring="km/h -> m/s")
        m.def_function[py_wrap_angle]("wrap_angle", docstring="wrap radians to [-pi, pi)")
        return m.finalize()
    except e:
        abort(String("error creating autonomy_py module: ", e))


def py_kph_to_mps(kph: PythonObject) raises -> PythonObject:
    return PythonObject(kph_to_mps(Float64(py=kph)))


def py_wrap_angle(angle: PythonObject) raises -> PythonObject:
    return PythonObject(wrap_angle(Float64(py=angle)))
