"""Check the downloaded datasets are complete and readable.

    pixi run check-data

Prints a short summary of each dataset in data/ and exits with an error if
something is missing or malformed. Run `pixi run fetch-data` first.
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NUSCENES = DATA / "nuscenes"
AV2 = DATA / "av2" / "motion-forecasting"

AV2_TIMESTEPS = 110  # 5 s observed + 6 s future at 10 Hz
AV2_FOCAL = 3        # object_category of the track to predict


def _table(name: str) -> list[dict]:
    return json.loads((NUSCENES / "v1.0-mini" / f"{name}.json").read_text())


def check_nuscenes() -> list[str]:
    if not (NUSCENES / "v1.0-mini" / "scene.json").exists():
        return ["nuScenes mini not found: run `pixi run fetch-data nuscenes`"]
    problems = []

    scenes, samples = _table("scene"), _table("sample")
    sample_data, annotations = _table("sample_data"), _table("sample_annotation")
    calibrated = {c["token"]: c for c in _table("calibrated_sensor")}
    sensors = {s["token"]: s for s in _table("sensor")}

    def channel(sd: dict) -> str:
        return sensors[calibrated[sd["calibrated_sensor_token"]]["sensor_token"]]["channel"]

    keyframes = [sd for sd in sample_data if sd["is_key_frame"]]
    missing = [sd["filename"] for sd in keyframes if not (NUSCENES / sd["filename"]).exists()]
    if missing:
        problems.append(f"nuScenes: {len(missing)} keyframe files missing, e.g. {missing[0]}")

    lidar = next(sd for sd in keyframes if channel(sd) == "LIDAR_TOP")
    raw = np.fromfile(NUSCENES / lidar["filename"], dtype=np.float32)
    if raw.size % 5:
        problems.append(f"nuScenes: {lidar['filename']} is not a multiple of 5 float32 values")
    points = raw.reshape(-1, 5)

    cam = next(sd for sd in keyframes if channel(sd) == "CAM_FRONT")
    with Image.open(NUSCENES / cam["filename"]) as image:
        if image.size != (cam["width"], cam["height"]):
            problems.append(f"nuScenes: {cam['filename']} is {image.size}, metadata says {cam['width']}x{cam['height']}")
        image_size, image_mode = image.size, image.mode

    print("nuScenes mini")
    print(f"  {len(scenes)} scenes, {len(samples)} keyframe samples (2 Hz), "
          f"{len(sample_data)} sensor files, {len(annotations)} 3D box annotations")
    print(f"  channels: {', '.join(sorted({channel(sd) for sd in keyframes}))}")
    print(f"  LIDAR_TOP sweep: {len(points)} points × (x, y, z, intensity, ring), "
          f"range {np.linalg.norm(points[:, :3], axis=1).max():.1f} m")
    print(f"  CAM_FRONT image: {image_size[0]}×{image_size[1]} {image_mode}, "
          f"fx = {calibrated[cam['calibrated_sensor_token']]['camera_intrinsic'][0][0]:.1f} px")
    return problems


def check_av2() -> list[str]:
    scenario_dirs = sorted(p for split in AV2.glob("*") if split.is_dir() for p in split.iterdir() if p.is_dir())
    if not scenario_dirs:
        return ["Argoverse 2 not found: run `pixi run fetch-data av2`"]
    problems = []
    types: collections.Counter[str] = collections.Counter()
    cities: collections.Counter[str] = collections.Counter()
    agents = lanes = 0

    for d in scenario_dirs:
        sid = d.name
        parquet, map_json = d / f"scenario_{sid}.parquet", d / f"log_map_archive_{sid}.json"
        if not (parquet.exists() and map_json.exists()):
            problems.append(f"Argoverse 2: {sid} is incomplete; re-run `pixi run fetch-data av2`")
            continue
        cols = pq.read_table(parquet, columns=["track_id", "object_type", "object_category",
                                               "timestep", "num_timestamps", "city"]).to_pydict()
        if cols["num_timestamps"][0] != AV2_TIMESTEPS or max(cols["timestep"]) != AV2_TIMESTEPS - 1:
            problems.append(f"Argoverse 2: {sid} does not have {AV2_TIMESTEPS} timesteps")
        focal_tracks = {t for t, c in zip(cols["track_id"], cols["object_category"]) if c == AV2_FOCAL}
        if len(focal_tracks) != 1:
            problems.append(f"Argoverse 2: {sid} has {len(focal_tracks)} focal tracks, expected 1")
        first_row = {}
        for track, kind in zip(cols["track_id"], cols["object_type"]):
            first_row.setdefault(track, kind)
        types.update(first_row.values())
        cities[cols["city"][0]] += 1
        agents += len(first_row)
        lanes += len(json.loads(map_json.read_text())["lane_segments"])

    n = len(scenario_dirs)
    print("Argoverse 2 motion forecasting")
    print(f"  {n} scenarios in {', '.join(sorted({d.parent.name for d in scenario_dirs}))}, "
          f"{AV2_TIMESTEPS} timesteps each (5 s observed + 6 s future, 10 Hz)")
    print(f"  {agents} tracks ({agents / n:.0f} per scenario), {lanes / n:.0f} lane segments per scenario")
    print(f"  tracks: {', '.join(f'{k} {v}' for k, v in types.most_common())}")
    print(f"  cities: {', '.join(f'{k} {v}' for k, v in cities.most_common())}")
    return problems


def main() -> None:
    problems = check_nuscenes()
    print()
    problems += check_av2()
    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\nAll datasets look good.")


if __name__ == "__main__":
    main()
