"""Report whether Mojo can see a GPU (`pixi run check-gpu`)."""
from std.sys import has_accelerator
from max.gpu.host import DeviceContext


def main() raises:
    comptime if not has_accelerator():
        print("No GPU found: Mojo will run CPU code only.")
    else:
        var ctx = DeviceContext()
        print("GPU:", ctx.name(), "| API:", ctx.api())
