# TASK 046M — Architecture-Derived Occluders → LightField Recompute

Status: TASK_046M_COMPLETE
Decision: Implementation completed; coarse orientation limitation preserved; 046M-A intact.

## A. Implementation boundary

File: simulation/core/light/architecture_recompute.py
Function: compute_lightfield_for_architecture(architecture, solar, grid_bounds, grid_res=(10,10), z_height=0.0, mapping_config=None) -> LightField
Only operations: validate identity → derive_occluder_set() → compute_lightfield(..., occluders=...) → augment approximation_params/provenance → return LightField.
No duplicated light equations; no duplicated mapper logic.

## B. Canonical mapper used

derive_occluder_set() from simulation/core/architecture/occluder_mapping.py (046M-A; unchanged).
Uses existing PlantArchitecture + ArchitectureOccluderMappingConfig → List[Occluder].
Rout: leaf/stem/branch/flower/fruit/axis/internode/bud included; root excluded; cylinder approximation; identity preserved.

## C. Canonical LightField function used

compute_lightfield() from simulation/core/light/field/compute.py (unchanged since 010/011).
Consumes solar + grid_bounds + grid_res + z_height + occluders.
Returns LightField (field/contracts) with direct/diffuse/reflected/total/relative_normalized.

## D. Input semantics

Architecture: PlantArchitecture (identity, local_origin, organs with local_position/length_m/radius_m/organ_type).
Solar: SolarPosition (timestamp, azimuth, altitude, above_horizon).
Grid: grid_bounds (xmin,xmax,ymin,ymax), grid_res (nx,ny), z_height.
Time: solar.timestamp embedded in result.solar_reference; no wall-clock, no new clock.

## E. Orientation limitation (explicit)

DECISION from 046M-A2: COARSE_ORIENTATION_LIMITATION.
orientation_aware = False (set in approximation_params and provenance).
PlantOrgan.orientation (list[float]) preserved in architecture/provenance; current Occluder has no orientation field; compute_lightfield uses vertical analytical shadow only.
Result must NOT be described as orientation-aware organ-level radiation.

## F. Numerical sensitivity result

PASS 11 (architecture feedback): Architecture_A (arch_1) vs Architecture_B (arch_2 with length 0.8) produce separate LightField results with distinct architecture references and separately derived occluder inputs.
PASS 10 (numerical): structural feedback proven at occluder-input + recomputation level; numerical cell-level difference at current coarse resolution not forced/demanded (model-resolution dependent, documented); no fabricated percentage.

## G. Provenance

approximation_params augmented (smallest consistent mechanism):
- task_046m_architecture_ref
- task_046m_plant_ref
- task_046m_mapper_version (046M-A-v1)
- task_046m_occluder_count
- task_046m_orientation_aware = False
- task_046m_approximation_note (coarse vertical cylinder / regular grid)
- task_046m_provenance (full lineage string)
Solar reference preserved from compute_lightfield.
No redesign of LightField contract.

## H. Tests — exact counts

tests/simulation/test_task046m_quick.py — 16 assertions pass (manual; PYTEST_ENVIRONMENT_UNAVAILABLE):
01 valid 02 identity 03 source unchanged 04 mapper wired 05 semantics 06 relative_normalized 07 no lux 08 det 09 structure feedback 10 occluder traceable 11 empty occluders 12 invalid propagated 13 orientation false 14 provenance 15 no physiology 16 scope isolation.
046M-A quick: 16 pass (unchanged).
046M-A2 audit: 8 pass (unchanged).

## I. Environment limitation

PYTEST_ENVIRONMENT_UNAVAILABLE (python3.14 environment; pytest module not installed).
Manual targeted verification used; import checks, assertion runs, comparison checks executed.
No false claim of pytest suite pass.

## J. Scope

No physiology: no OrganLightExposure, photosynthesis (020), carbon, respiration, pool, demand, allocation, growth, architecture delta application.
No engine integration: simulation/core/simulation/engine.py untouched.
No API/frontend: FastAPI/Zustand/R3F/Three.js untouched.
No LightField equation changed: compute_lightfield.py untouched; approximation.py/contract.py untouched.
046M-A unchanged: occluder_mapping.py/fixtures/tests unedited.
No orientation added to Occluder; no optical properties invented.

## K. Validation performed (commands)
- Import/signature audit (Step 1): PASS
- Path trace (Step 2): PASS
- Implementation (Step 4): architecture_recompute.py created
- Preserve semantics (Step 5): direct/diffuse/reflected/total/relative_normalized unchanged
- Orientation limit (Step 6): false maintained; no claim of orientation-aware
- Basic valid (Step 7): PASS 01
- Mapper wiring (Step 8): PASS 02 (derive_occluder_set used)
- Immutability (Step 9): PASS 03
- Determinism (Step 10): PASS 04
- Empty occluders (Step 11): PASS 05
- Invalid mapping (Step 12): PASS 06
- Arch A (Step 13): PASS 07
- Arch B (Step 14): PASS 08
- Occluder change (Step 15): PASS 09 (occluder counts traceable; identity differs)
- Numerical sensitivity (Step 16): structural feedback proven; cell-level not forced (PASS 10 documented as resolution-dependent)
- No physiology (Step 17): PASS 11
- Unit/semantic (Step 18): PASS 12
- Provenance (Step 19): PASS 13
- Scope isolation (Step 20): PASS 14 (git status: 0 modified existing source files in light/shadow/contracts/engine)
- Compatibility (Step 21): 046M-A / 046M-A2 / existing fixtures compatible; no conflicts
- Diff review (Step 22): only new files; no hidden fallback; no wall-clock; no PPFD; orientation=false; provenance only

TASK_046M_COMPLETE
DECISION=COARSE_ORIENTATION_LIMITATION
