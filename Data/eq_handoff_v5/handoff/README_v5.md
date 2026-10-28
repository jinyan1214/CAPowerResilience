# Earthquake handoff v5 (Stage A v5 + disaggregation v5, 2026-10-25)

Supersedes v3 and v4 (both stay in place). v5 rebuilds Stage A with existing plants kept at installed capacity (the v3/v4 Stage A force-retired existing fleets above 2 GW per zone) and config-driven scenarios. One folder per scenario:
`<scenario>/disagg/`.

## What changed from v3

- **`buses_all.csv` is byte-for-byte identical to v3** (verified for every scenario; see
  `handoff_v4_check.json`). Your bus-keyed substation files (`capacity_substation.csv`,
  `damage_substation.csv`) stay valid as they are.
- **`assets_all.csv` is keyed by `asset_key`**, the PyPSA component name, not by row number.
  The key is stable: it does not change if rows are added, removed or reordered, and the same
  asset has the same key in every scenario (e.g. `CATS_gen_123` for an existing CATS plant).
  Please key damage files by `asset_key` (the column `asset_id` = row index is gone).
- **All generators with p_nom > 0 are included, existing and new** (v3 handoff damage covered
  only new builds), plus all storage units.
- Existing California plants now have real technologies (from the CATS EIA fuel types) and
  therefore real `damage_category` values (v3 put all 2,149 of them in "other"). Their
  capacity follows Stage A for each scenario (retirements, `p_nom_mw`).
- New: `in_california` and `outside_shaking_footprint` (True for out-of-state zone assets;
  these are single-bus zones outside the shaking footprint and can be left undamaged).
- `branches_all.csv`: same rows as v3; `total_mw` now includes the reinforcement of local
  lines/transformers (`reinforcement_mw`, `v3_total_mw` for comparison).

## Columns of assets_all.csv

asset_key, asset_type (generator / storage_unit), carrier, damage_category, bus, lon, lat,
v_nom_kv, region, zone (Stage A zone), in_california, outside_shaking_footprint, p_nom_mw,
existing_mw, new_mw, is_new_build, max_hours / energy_mwh (storage), cats_fuel_type (EIA fuel
type for existing CATS plants), source (how the asset was derived), plant_id and
p_nom_after_mw (same values as asset_key / p_nom_mw; kept for compatibility).

## Counts

- bau: 2,863 assets (2,690 in California, 173 outside the footprint); 8,899 buses
- conservative: 2,868 assets (2,695 in California, 173 outside the footprint); 8,899 buses
- aggressive: 2,895 assets (2,722 in California, 173 outside the footprint); 8,899 buses

## asset_key across scenarios

- 3,005 distinct keys: 2,773 in all three scenarios, 75 in two, scenario-specific bau 26, conservative 29, aggressive 102.
- Mismatched keys (same key, different bus/carrier/type): 0. Existing CATS plants with more than one key: 0.
- Scenario-specific keys are assets that exist in only that scenario (its new builds, or existing plants another scenario retired).

## Suggested fragility mappings for carriers without a v3 category (damage_category = "other")

- **CCS gas (`CCGT-95CCS`) and hydrogen CTs (`hydrogen_ct`)**: HAZUS generation plant, same size class as a gas
  plant of that capacity.
- **Waste (`waste`)**: HAZUS small generation plant.
- **Floating offshore wind (`offwind_floating`)**: no turbine fragility; damage only through its onshore
  substation (the CATS bus it connects to, already in your substation files).

(None of these are new builds in v5's California, where CCS and H2 are off; they can appear out of state.)

## Reinforcement in v5 (branches_all.csv)

`reinforcement_mw` = rating added to the existing branch: rating-only uprates (at most 2x, impedance unchanged)
plus `parallel_circuits_added` circuits identical to the original branch on the same corridor (same buses and
voltage; the corridor's impedance falls accordingly). Rows are identical to v3: parallel circuits are stored on the
existing branch, so a substation outage removes them with the corridor.
