"""Run every tests/mojo/test_*.mojo file; exit non-zero if any fails.

Mojo 1.x has no `mojo test` command: each test file is a program whose
`main` runs a `TestSuite`. GPU tests should guard themselves with
`has_accelerator()` so they skip on CPU-only machines such as CI.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    files = sorted((ROOT / "tests" / "mojo").glob("test_*.mojo"))
    if not files:
        print("no Mojo tests found")
        return 0
    failed = []
    for f in files:
        rel = f.relative_to(ROOT)
        print(f"== {rel}", flush=True)
        result = subprocess.run(["mojo", "run", "-I", str(ROOT), str(f)], cwd=ROOT)
        if result.returncode != 0:
            failed.append(str(rel))
    print(f"\n{len(files) - len(failed)}/{len(files)} Mojo test files passed")
    for name in failed:
        print(f"FAILED: {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
