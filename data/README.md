# Data

Datasets live here but are **never committed**. Download them with:

```bash
pixi run fetch-data    # nuScenes mini + 200 Argoverse 2 scenarios
pixi run check-data    # confirm they are complete and readable
```

| Folder | Contents |
|---|---|
| `nuscenes/` | nuScenes v1.0-mini: `v1.0-mini/` metadata tables, `samples/` keyframes, `sweeps/` intermediate frames, `maps/` |
| `av2/motion-forecasting/<split>/<scenario_id>/` | Argoverse 2 scenario tracks (`.parquet`) and map (`.json`) |
| `raw/` | Download archives (removed after extraction unless `--keep-archive`) |
| `processed/` | Your cached, derived arrays |

All of these are gitignored. Both datasets are licensed CC BY-NC-SA 4.0 for
non-commercial use; nuScenes also requires an account. See
[docs/datasets.md](../docs/datasets.md) for licences, file formats and
coordinate frames.
