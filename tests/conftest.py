"""Make the compiled Mojo bindings (build/autonomy_py.so) importable.

`pixi run test-py` builds them first via the `build-py` task.
"""
import pathlib
import sys

BUILD = pathlib.Path(__file__).resolve().parents[1] / "build"
sys.path.insert(0, str(BUILD))
