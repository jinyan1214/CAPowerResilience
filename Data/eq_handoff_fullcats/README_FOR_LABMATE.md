# Earthquake / fragility handoff package

## Which network to use
- **`disagg/`** — Stage-2 CATS nodal networks. Use these for California earthquake mapping (bus coordinates).
- **`macro/`** — Stage-1 WECC ~33-zone networks. WECC-wide context only; not nodal inside California.

If this folder is `eq_handoff_fullcats/`, disagg is on **full California CATS** (~8.8k buses). If `eq_handoff/`, disagg may be the **SoCal-heavy clustered** layer.

## CSV files (per scenario folder)
| File | Contents |
|------|----------|
| `buses_all.csv` | **Every bus** (lon/lat, region, voltage) |
| `assets_all.csv` | **Every generator + storage unit** with capacity, coords, `damage_category` for fragility literature search |
| `assets_new_build_only.csv` | Subset where expansion added capacity |
| `branches_all.csv` | Lines, links, transformers |
| `storage_by_carrier.csv` | Storage summary by technology |

## .nc files
Include the NetCDF networks listed in `nc_manifest.txt` (same folder). Your colleague can load them with PyPSA: `pypsa.Network('path.nc')`.

## Storage / FEMA fragility note
FEMA HAZUS does not publish storage-specific curves. In this model, new storage is **grid-scale lithium-ion BESS**:
- `4hr_battery_storage` — 4-hour duration (dominant new build)
- `8hr_battery_storage` — 8-hour duration (`battery-hv`)
- Legacy brownfield may use carrier `battery`
For fragility, search literature for **grid-scale battery energy storage**, **containerized BESS**, or use a HAZUS **electrical equipment / industrial** proxy; duration (4h vs 8h) is an energy sizing choice, not a different physical plant class.

## Run stats
- **bau / macro**: 33 buses, 1063 assets (122 new), 136 branches
- **bau / disagg**: 8899 buses, 3041 assets (718 new), 10953 branches
- **conservative / macro**: 33 buses, 883 assets (31 new), 136 branches
- **conservative / disagg**: 8899 buses, 3031 assets (708 new), 10953 branches
- **aggressive / macro**: 33 buses, 793 assets (172 new), 136 branches
- **aggressive / disagg**: 8899 buses, 3290 assets (954 new), 10953 branches

## .nc manifest
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/elec_expanded_bau_macro_fullyear.nc`
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/cats_disagg_bau_fullcats_fullyear.nc`
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/elec_expanded_conservative_macro_fullyear.nc`
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/cats_disagg_conservative_fullcats_fullyear.nc`
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/elec_expanded_aggressive_macro_fullyear.nc`
- `/scratch/users/vdinov/pypsa-usa/workflow/results/networks/step4_scenarios/cats_disagg_aggressive_fullcats_fullyear.nc`
