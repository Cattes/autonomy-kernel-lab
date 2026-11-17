# Datasets

The course uses two small, real driving datasets. Together they cover every
module and fit comfortably on a 16 GB Mac.

| Dataset | What it gives you | On disk | Lessons |
|---|---|---|---|
| [nuScenes mini](#nuscenes-mini) | 10 scenes × 20 s of synchronized cameras, LiDAR, radar, calibration, ego poses and labelled 3D boxes with track IDs | 5.1 GB | 02 camera perception, 03 LiDAR, fusion and tracking |
| [Argoverse 2 motion forecasting](#argoverse-2-motion-forecasting) | 11 s scenarios of every agent's track plus a vector lane map | ~0.25 MB per scenario, 50 MB for the default 200 | 04 prediction, 05 planning, 06 control, 07 simulation |

## Download

1. Create a free [nuScenes account](https://www.nuscenes.org/sign-up) and
   accept the [terms of use](https://www.nuscenes.org/terms-of-use).
   Argoverse 2 needs no account.
2. Download both datasets and check them:

```bash
pixi run fetch-data
pixi run check-data
```

`fetch-data` asks you to confirm you accepted the nuScenes terms, downloads
the 4.2 GB nuScenes archive (resuming if interrupted), unpacks it into
`data/nuscenes/` and deletes the archive, then downloads 200 Argoverse 2
validation scenarios into `data/av2/`. Running it again skips whatever is
already there. You need about 10 GB free while it unpacks.

Useful variations:

| Command | Effect |
|---|---|
| `pixi run fetch-data av2` | Only Argoverse 2 |
| `pixi run fetch-data av2 --av2-scenarios 1000` | More scenarios (the first N, so a larger N adds to what you have) |
| `pixi run fetch-data nuscenes --accept-terms` | Skip the terms prompt, e.g. in a script |
| `pixi run fetch-data nuscenes --keep-archive` | Keep `data/raw/v1.0-mini.tgz` |

`check-data` prints what it found:

```text
nuScenes mini
  10 scenes, 404 keyframe samples (2 Hz), 31206 sensor files, 18538 3D box annotations
  LIDAR_TOP sweep: 34688 points × (x, y, z, intensity, ring), range 102.9 m
  CAM_FRONT image: 1600×900 RGB, fx = 1266.4 px

Argoverse 2 motion forecasting
  200 scenarios in val, 110 timesteps each (5 s observed + 6 s future, 10 Hz)
  11618 tracks (58 per scenario), 69 lane segments per scenario
```

## Licences and rules

Both datasets are licensed
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/):
non-commercial use, with attribution, and anything derived from them is
shared under the same licence. For this repository that means:

- **Never commit dataset files**, not even small slices. `data/nuscenes/`,
  `data/av2/` and `data/raw/` are gitignored.
- **CI has no data.** Tests that read a dataset must skip when it is missing
  (`pytest.mark.skipif(not path.exists(), reason=...)`); the correctness tests
  that run in CI use synthetic inputs.
- Screenshots and charts made from the data are fine in your lesson reports;
  credit the dataset.

## nuScenes mini

A 10-scene sample of [nuScenes](https://www.nuscenes.org/nuscenes) by
Motional: Boston Seaport and three Singapore districts. Seven scenes are in
daylight and three at night, one of them on wet roads. Each scene is about 20 s.

**Sensors** (12 channels):

| Channel | Sensor | Rate | Format |
|---|---|---|---|
| `CAM_FRONT`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`, `CAM_BACK`, `CAM_BACK_LEFT`, `CAM_BACK_RIGHT` | Cameras, 1600×900 | 12 Hz | JPEG |
| `LIDAR_TOP` | 32-beam spinning LiDAR | 20 Hz | `.pcd.bin` |
| `RADAR_FRONT`, `RADAR_FRONT_LEFT`, `RADAR_FRONT_RIGHT`, `RADAR_BACK_LEFT`, `RADAR_BACK_RIGHT` | Radars | 13 Hz | `.pcd` |

**Layout** of `data/nuscenes/`:

| Path | Contents |
|---|---|
| `v1.0-mini/*.json` | Metadata tables (32 MB) |
| `samples/<CHANNEL>/` | **Keyframes**: one per sensor at each annotated 2 Hz sample |
| `sweeps/<CHANNEL>/` | Every other frame between keyframes, not annotated |
| `maps/*.png` | Rasterized drivable-area maps |

**The tables** are lists of JSON records that point to each other by
`token`. The ones you will use:

| Table | Key fields | Used for |
|---|---|---|
| `scene` | `name`, `description`, `first_sample_token` | Picking a scene |
| `sample` | `timestamp`, `scene_token`, `prev` / `next` | One annotated moment (2 Hz) |
| `sample_data` | `filename`, `is_key_frame`, `timestamp`, `ego_pose_token`, `calibrated_sensor_token` | One sensor file |
| `calibrated_sensor` | `translation`, `rotation`, `camera_intrinsic` | Sensor pose on the car, camera matrix |
| `ego_pose` | `translation`, `rotation` | Car pose in the map at that file's timestamp |
| `sample_annotation` | `translation`, `size`, `rotation`, `instance_token`, `num_lidar_pts` | One labelled 3D box |
| `instance` | `category_token` | One tracked object across time (track ID) |

Conventions you will need in Lesson 03:

- **Units:** metres, radians, timestamps in **microseconds**.
- **Rotations** are quaternions ordered `[w, x, y, z]`.
- **Three frames:** a point in a sensor file is in the **sensor frame**;
  `calibrated_sensor` takes it to the **ego frame** (x forward, y left,
  z up, on the car); `ego_pose` takes it to the **global frame** (the map).
  Box annotations are in the global frame.
- **Cameras** use x right, y down, z forward; project with the 3×3
  `camera_intrinsic`. Images are already undistorted.
- **Boxes:** `translation` is the centre, `size` is `[width, length, height]`.
- **LiDAR files** (`.pcd.bin`) are a flat array of `float32`, five per point:
  x, y, z, intensity, ring index. In NumPy:
  `np.fromfile(path, dtype=np.float32).reshape(-1, 5)`. This is also easy to
  read directly from Mojo.
- Each camera and LiDAR runs on its own clock, so a keyframe's six images and
  sweep have slightly different timestamps and ego poses. Transform with the
  pose that belongs to each file.

The full schema is in the
[nuScenes devkit docs](https://github.com/nutonomy/nuscenes-devkit/blob/master/docs/schema_nuscenes.md).
We read the JSON ourselves rather than installing the devkit, so you see every
transform.

*Optional extras*, not needed for now: the nuScenes **map expansion** (vector
lanes, for prediction on nuScenes) and **CAN bus expansion** (steering and
wheel speeds) are separate downloads on the nuScenes site after you sign in.

## Argoverse 2 motion forecasting

[Argoverse 2](https://argoverse.github.io/user-guide/datasets/motion_forecasting.html)
by Argo AI has about 250,000 scenarios from six US cities. Each scenario is
11 s at 10 Hz (110 timesteps): the first 50 timesteps (5 s) are observed,
and the task is to predict the next 60 (6 s). The downloads come from the
**validation** split because it includes the ground-truth futures. Scenarios
are listed in ID order, which is effectively random.

**Layout:** `data/av2/motion-forecasting/val/<scenario_id>/` holds:

- `scenario_<id>.parquet`: one row per agent per timestep
- `log_map_archive_<id>.json`: the local vector map

**Scenario columns:**

| Column | Meaning |
|---|---|
| `track_id`, `object_type` | Agent ID; `vehicle`, `pedestrian`, `cyclist`, `bus`, `static`, ... |
| `object_category` | 0 track fragment, 1 unscored, 2 scored, **3 focal** (the agent to predict) |
| `timestep` | 0–109; `observed` is true for the first 50 |
| `position_x`, `position_y`, `heading` | Pose in the city frame (metres, radians) |
| `velocity_x`, `velocity_y` | Velocity (m/s) |
| `focal_track_id`, `city`, `scenario_id` | Same in every row |

Agents can appear and disappear partway through, so not every track has all
110 timesteps; handling the gaps is part of Lesson 04.

**Map:** `lane_segments` (each with a `centerline` polyline, left and right
boundaries, `predecessors`, `successors` and neighbour IDs, `lane_type` and
`is_intersection`), `drivable_areas` (polygons) and `pedestrian_crossings`.
Points are `{"x", "y", "z"}` in the same city frame as the tracks.

Read the parquet with `pyarrow` (already in the environment). We don't
install the `av2` package; the format is simple enough to load directly.

## How data reaches your Mojo code

Python loads files (JSON, JPEG through Pillow, Parquet through pyarrow) into
NumPy arrays, then hands them to your Mojo functions through
`bindings/autonomy_py.mojo`, the same way as in Lesson 01. Keep arrays
contiguous `float32`, and convert to the layout your kernel wants
(for example, structure-of-arrays for point clouds) in one place.
