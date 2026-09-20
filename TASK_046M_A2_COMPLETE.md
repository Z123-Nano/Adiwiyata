# TASK 046M-A2 — Occluder Orientation & Optical Semantics Audit

Status: TASK_046M_A2_COMPLETE
DECISION=COARSE_ORIENTATION_LIMITATION

## A. Existing Occluder semantics (verified from code, not inferred)

Contract: simulation/core/shadow/model.py — Occluder(BaseModel)
Fields (exact): id (str), geometry (Literal["box","wall","cylinder","point","other"]), position (tuple[float,float,float]), dimensions (tuple[float,float,float]), height_m (float).
No fields: orientation, rotation, axis, direction, normal, endpoints, local coordinate frame, material/reflectance/transmittance/absorption.
Geometry interpretation: vertical occluder on horizontal plane; shadow direction derived from solar azimuth (sun_direction), not from occluder orientation; shadow length = height / tan(altitude) (vertical projection only).

## B. Existing PlantOrgan orientation semantics (verified)

Contract: simulation/core/contracts/domain.py — PlantOrgan(BaseModel)
Field: orientation: Optional[list[float]] = direction vector [dx,dy,dz] normalized.
Not Euler angles, not quaternion, not transform object; simple normalized direction vector.
Local coordinate frame: plant_local (coordinate_frame on PlantArchitecture) with local_origin.

## C. Mapping behavior (046M-A verified unchanged)

derive_occluder_set() maps:
- local_position + local_origin → Occluder.position
- length_m → Occluder.height_m
- radius_m → Occluder.dimensions (radius)
- organ_type → include/exclude rule
Orientation (list[float]) is preserved only in result.provenance / approximation_notes; it is NOT mapped to Occluder.geometry, not to dimensions, not to position, and not used by compute_lightfield.
Mapping remains pure; no mutation; no light computation.

## D. LightField behavior (verified from compute

compute_lightfield() (simulation/core/light/field/compute.py) accepts: solar, grid_bounds, grid_res, z_height, occluders.
Per-point direct: sun_above_horizon + shadow check through direct_shadow() which uses occluder.position/dimensions/height_m + solar azimuth.
No reference to occluder.orientation, rotation, or organ direction.
Shadow is analytical vertical projection; cylinder geometry treated as vertical extent at position.
Therefore: orientation does NOT influence LightField calculation.

## E. Application impact assessment

Classification: MODERATE.
Reasoning (qualitative, not fabricated numeric):
- FSPM literature confirms leaf angle / orientation can materially alter light interception, canopy light profiles, and dry-mass production; those effects are model- and scenario-specific.
- Current LightField is a coarse regular-grid approximation (resolution ~10x10) with synthetic vertical occluders and first-order reflected approximation; it does not resolve organ-level light angles or realistic canopy transmission.
- Ignoring orientation at current resolution does not introduce a false confidence of accurate interception, because the approximation is explicitly coarse and documented as such.
- However, for a digital-twin feedback loop (Architecture_(N+1) → LightField_(N+1) → physiology), orientation-agnostic shadow means structural changes that primarily alter leaf angle (rather than position/size) will not be reflected in light recomputation. This limitation must be acknowledged when interpreting downstream predictions.
No fabricated percentage presented; effect is scenario-dependent and model-dependent.

## F. Scientific limitation (explicit)

Current mapping is:
- orientation-agnostic at the light-computation boundary (Occluder has no orientation field; compute_lightfield does not use one).
- axis-aligned approximation: cylinder vertical axis fixed to world Z (up); shadow length is vertical projection; no tilt, no rotation, no leaf-angle distribution.
- coarser than full 3D polygon/radiation representation; sufficient for structural-feedback boundary (position + size + vertical shadow), not sufficient for realistic organ-level light interception.
- NOT described as realistic light interception; approximation_notes in mapping + this report document limitation.
- Occluder ≠ organ optical property model: no reflectance, transmittance, absorption, or radiative transfer coefficients added (preserved per spec Step 6).

## G. Decision

COARSE_ORIENTATION_LIMITATION.

Reason: existing Occluder contract lacks orientation fields; compute_lightfield uses only vertical analytical shadow; no minimal contract fix makes this orientation-aware without inventing new occluder semantics or altering the light equation. Blocking 046M (recomputation) is unnecessary (mapping is complete for coarse approximation), but 046M must document that its output is coarse and orientation-agnostic. No source change required; 046M-A remains intact.

## H. Required next step for 046M

Proceed with 046M (LightField_(N+1) recomputation) only with explicit acknowledgment in result provenance / notes that:
- architecture-derived occluders are vertical cylinders (position + size + fixed vertical axis);
- organ orientation is preserved in architecture/provenance but does not affect shadow calculation;
- LightField output remains approximate / relative_normalized and must not be interpreted as realistic organ-level PPFD or absorption.
If future science requires orientation-sensitive interception, the minimum missing contract is an Occluder orientation field (plus compute_lightfield update to use it) — out of scope for 046M-A2, which is audit-only.

## I. Explicit exclusions / integrity checks

- Oxcluder fields unchanged (id/geometry/position/dimensions/height_m).
- No lux→PPFD; no relative_normalized→PPFD.
- No photosynthesis / carbon / allocation / growth executed.
- No engine integration.
- No frontend / API change.
- 046M-A mapping unmodified (verified PASS 07).
- PYTEST_ENVIRONMENT_UNAVAILABLE; targeted inspection tests (PASS 01–08) performed manually.

## J. Tests performed

PASS 01: Occluder import OK
PASS 02: Occluder fixture OK
PASS 03: fields verified (5 fields, no orientation)
PASS 04: PlantOrgan orientation = list[float] verified
PASS 05: mapping uses position/dims/height; orientation not in occluder geometry
PASS 06: compute_lightfield params = solar, grid_bounds, grid_res, z_height, occluders (no orientation param)
PASS 07: occluder_mapping unchanged (not edited for orientation)
PASS 08: no physiology in audit path

TASK_046M_A2_COMPLETE
DECISION=COARSE_ORIENTATION_LIMITATION
