"""Download the course datasets into data/ (never committed).

    pixi run fetch-data                       # nuScenes mini + 200 Argoverse 2 scenarios
    pixi run fetch-data av2 --av2-scenarios 50
    pixi run fetch-data nuscenes --accept-terms

nuScenes mini (~4.2 GB download, ~4.5 GB on disk) goes to data/nuscenes/.
Argoverse 2 motion-forecasting scenarios (~0.4 MB each) go to
data/av2/motion-forecasting/<split>/. Re-running skips what is already there,
and an interrupted nuScenes download resumes where it stopped.

Only the Python standard library is used, so this runs before anything else.
See docs/datasets.md for licences and file formats.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tarfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "autonomy-kernel-lab-fetch/1.0"

NUSCENES_URL = "https://www.nuscenes.org/data/v1.0-mini.tgz"
NUSCENES_TERMS = "https://www.nuscenes.org/terms-of-use"
NUSCENES_FREE_GB = 10

AV2_BUCKET = "https://argoverse.s3.amazonaws.com"
AV2_PREFIX = "datasets/av2/motion-forecasting"
S3_NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}


def _show(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def _open(url: str, headers: dict[str, str] | None = None):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    return urllib.request.urlopen(request, timeout=60)


def _download(url: str, dest: Path, *, resume: bool = False, progress: bool = False) -> None:
    """Download url to dest via dest.part, resuming a partial file if asked."""
    part = dest.with_name(dest.name + ".part")
    have = part.stat().st_size if (resume and part.exists()) else 0
    headers = {"Range": f"bytes={have}-"} if have else {}
    with _open(url, headers) as response:
        if have and response.status != 206:  # server ignored the range: start over
            have = 0
        total = have + int(response.headers.get("Content-Length", 0))
        with open(part, "ab" if have else "wb") as out:
            done, next_report = have, 0.0
            while chunk := response.read(1 << 20):
                out.write(chunk)
                done += len(chunk)
                if progress and total and done / total >= next_report:
                    print(f"  {done / 1e9:5.2f} / {total / 1e9:.2f} GB ({100 * done / total:3.0f}%)", flush=True)
                    next_report += 0.05
    if total and part.stat().st_size != total:
        raise RuntimeError(f"{dest.name}: got {part.stat().st_size} bytes, expected {total}; re-run to resume")
    part.replace(dest)


def _confirm_nuscenes_terms(accept: bool) -> None:
    print(f"nuScenes is licensed CC BY-NC-SA 4.0 for non-commercial use: {NUSCENES_TERMS}")
    print("You need a nuScenes account and must have accepted these terms.")
    if accept:
        return
    if not sys.stdin.isatty():
        sys.exit("Re-run with --accept-terms once you have accepted the nuScenes terms of use.")
    if input("Have you registered and accepted the terms? [y/N] ").strip().lower() not in {"y", "yes"}:
        sys.exit("Skipped nuScenes. Register at https://www.nuscenes.org/sign-up first.")


def fetch_nuscenes(data_dir: Path, *, accept_terms: bool, keep_archive: bool) -> None:
    target = data_dir / "nuscenes"
    if (target / "v1.0-mini" / "scene.json").exists():
        print(f"nuScenes mini already in {_show(target)}")
        return
    _confirm_nuscenes_terms(accept_terms)

    raw = data_dir / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    archive = raw / "v1.0-mini.tgz"
    if not archive.exists():
        free_gb = shutil.disk_usage(data_dir).free / 1e9
        if free_gb < NUSCENES_FREE_GB:
            sys.exit(f"Only {free_gb:.1f} GB free; nuScenes mini needs about {NUSCENES_FREE_GB} GB while unpacking.")
        print(f"Downloading {NUSCENES_URL}")
        _download(NUSCENES_URL, archive, resume=True, progress=True)

    print(f"Extracting into {_show(target)}")
    staging = data_dir / "nuscenes.partial"
    shutil.rmtree(staging, ignore_errors=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(staging, filter="data")
    staging.replace(target)
    if not keep_archive:
        archive.unlink()
    print("nuScenes mini ready.")


def _list_av2_scenarios(split: str, count: int) -> list[str]:
    """First `count` scenario IDs of a split, in the bucket's (sorted) order."""
    ids: list[str] = []
    token = None
    while len(ids) < count:
        query = {"list-type": "2", "prefix": f"{AV2_PREFIX}/{split}/", "delimiter": "/",
                 "max-keys": str(min(1000, count - len(ids)))}
        if token:
            query["continuation-token"] = token
        with _open(f"{AV2_BUCKET}/?{urllib.parse.urlencode(query)}") as response:
            tree = ET.fromstring(response.read())
        ids += [p.text.rstrip("/").rsplit("/", 1)[-1] for p in tree.findall("s3:CommonPrefixes/s3:Prefix", S3_NS)]
        token_el = tree.find("s3:NextContinuationToken", S3_NS)
        if token_el is None:
            break
        token = token_el.text
    return ids[:count]


def fetch_av2(data_dir: Path, *, split: str, count: int) -> None:
    target = data_dir / "av2" / "motion-forecasting" / split
    print(f"Listing the first {count} Argoverse 2 '{split}' scenarios")
    ids = _list_av2_scenarios(split, count)

    jobs = []
    for sid in ids:
        for name in (f"scenario_{sid}.parquet", f"log_map_archive_{sid}.json"):
            dest = target / sid / name
            if not dest.exists():
                jobs.append((f"{AV2_BUCKET}/{AV2_PREFIX}/{split}/{sid}/{name}", dest))
    if not jobs:
        print(f"All {len(ids)} scenarios already in {_show(target)}")
        return

    def get(job: tuple[str, Path]) -> None:
        url, dest = job
        dest.parent.mkdir(parents=True, exist_ok=True)
        _download(url, dest)

    print(f"Downloading {len(jobs)} files into {_show(target)}")
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, _ in enumerate(pool.map(get, jobs), 1):
            if i % 100 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)} files", flush=True)
    print(f"Argoverse 2: {len(ids)} scenarios ready.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="*", choices=["nuscenes", "av2"],
                        help="which datasets to fetch (default: both)")
    parser.add_argument("--av2-scenarios", type=int, default=200, help="number of Argoverse 2 scenarios (default 200)")
    parser.add_argument("--av2-split", choices=["train", "val", "test"], default="val",
                        help="Argoverse 2 split to sample from (default val)")
    parser.add_argument("--accept-terms", action="store_true",
                        help="confirm you accepted the nuScenes terms of use (skips the prompt)")
    parser.add_argument("--keep-archive", action="store_true", help="keep data/raw/v1.0-mini.tgz after extracting")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data", help="where to put the data (default data/)")
    args = parser.parse_args()
    datasets = args.datasets or ["nuscenes", "av2"]

    data_dir = args.data_dir.resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    if "av2" in datasets:
        fetch_av2(data_dir, split=args.av2_split, count=args.av2_scenarios)
    if "nuscenes" in datasets:
        fetch_nuscenes(data_dir, accept_terms=args.accept_terms, keep_archive=args.keep_archive)


if __name__ == "__main__":
    main()
