# TASK 046M-A — PlantArchitecture → Light Occluder Mapping (COMPLETE)

Status: COMPLETED (mapping layer only; 046M recomputation remains blocked until mapping feeds compute_lightfield)

## A. LightField input boundary after mapping

Before 046M-A: compute_lightfield consumed (solar, grid_bounds, grid_res, z, occluders) — architecture not accepted.
After 046M-A: architecture → ArchitectureOccluderSet → list[Occluder] can be passed as occluders to compute_lightfield.
No change to compute_lightfield equation or contract.

## B. Architecture fields actually consumed by mapping

From PlantOrgan (actual contract fields verified):
- id, plant_id, architecture_id (identity)
- organ_type → explicit include/exclude rule (leaf/stem/branch/flower/fruit/axis/internode/bud INCLUDE; root EXCLUDE by default)
- local_position [x,y,z]
- orientation [dx,dy,dz] — preserved in provenance notes only; shadow model uses vertical extent (not full rotation)
- length_m → occluder height_m
- radius_m → occluder dimensions (radius)
- status — not used for occlusion (only identity check)

From PlantArchitecture: architecture_id, plant_id, local_origin → position offset; coordinate_frame noted (plant_local assumed); organs list.
No consumption of topology, geometry_metadata, provenance, schema_version (only preserved in result provenance).

## C. Reuse of canonical LightField calculation

Mapping reuses shadow/model.py Occluder contract (existing, unchanged) — geometry literal ["box","wall","cylinder","point","other"] preserved; dimensions tuple preserved; position tuple preserved; height_m preserved.
No new radiation model; no duplicate compute_lightfield.
Thin boundary only.

## D. Time semantics

Mapping is stateless / pure; no simulation clock, no timestep, no wall-clock substitution. Time preserved by caller (compute_lightfield uses solar.timestamp). Explicit.

## E. Units preserved

All mapping outputs in meters (m): position (m), dimensions (m), height_m (m). LightField output remains relative_normalized (0-1) — no conversion, no lux, no PPFD influence introduced at mapping layer.

## F. Provenance / status / determinism

Mapping result carries: source_architecture_id, source_plant_id, mapping_config_ref (046M-A-v1), mapped/excluded organ lists, approximation_notes (cylinder/vertical), provenance string with count and source reference, is_synthetic_example=True.
Identical architecture + config → identical model_dump_json() (verified PASS 11).
Status AVAILABLE / NOT_COMPUTABLE explicit; missing identity → NOT_COMPUTABLE (not default/empty).

## G. Immutability / no mutation

- PlantArchitecture unmodified (verified PASS 02/15).
- PlantOrgan unmodified (deep list preserved; no field writes).
- ArchitectureGrowthDelta untouched.
- compute_lightfield untouched.
- No engine change.
- No front-end / API / Zustand change.

## H. Scientific approximation explicitly documented

Approximation: structural organs represented as vertical cylinders (height = length_m; radius = radius_m or 0.05 default). Shadow model (direct_shadow) already treats occluder as vertical extent with position; orientation vector not fully simulated (only vertical projection used). This is explicitly documented in approximation_notes and acknowledged as coarser than full 3D polygon radiation; sufficient for structural-feedback boundary, not a full radiosity model.

## I. Tests / validation

- pytest unavailable (python3.14); targeted manual verification used.
- 16 assertions pass (test_task046m_a_quick.py): availability, source unchanged, identity, occluders produced, root excluded, leaf mapped, cylinder geometry, position, height, radius, determinism, provenance, no light computation, missing arch blocked, immutability, structural feedback (arch_A vs arch_B distinct results).
- Import of simulate/core/architecture/occluder_mapping.py and fixtures_046m_a.py verified.
- No broken references to deleted modules.

## J. Explicit exclusions per spec

- OrganLightExposure (046C) NOT executed.
- Photosynthesis (020–023, 046D/E/F) NOT executed.
- Carbon / allocation / growth (046G/I/J) NOT executed.
- No lux→PPFD conversion.
- No relative_normalized→PPFD reinterpretation.
- No engine integration (engine.py unmodified).

## K. Limitation / next step for 046M

Mapping layer is complete; 046M (LightField_(N+1) recomputation) now can be opened by passing ArchitectureOccluderSet.occluders into compute_lightfield with architecture-derived grid bounds if needed. The structural-feedback loop Architecture_(N) → LightField_(N) → ... → Architecture_(N+1) → LightField_(N+1) is now bounded by an explicit architecture→occluder contract rather than an invented direct coupling.

Audit date: 2026-09-17
Source of truth: filesystem + import + manual assertions (git optional only)
LOCAL_AUDIT_COMPLETE
