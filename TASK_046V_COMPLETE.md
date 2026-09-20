# TASK 046V — Organ-Level Absolute Incident PPFD Derivation (COMPLETE)
**Status:** COMPLETE (all 21 checks A-AB verified; physical PPFD executable; 046O boundary preserved; upstream untouched).
**Date:** 2026-09-18

## Executive verdict
Smallest explicit adapter `combine_reference_transfer_to_ppfd_source` multiplies `AbsolutePPFDReference.ppfd_value` (µmol photons m^-2 s^-1, PAR 400-700) by validated `SpatialPPFDTransferFactor.transfer_value` (dimensionless) to produce `PPFDSource` with `value` in µmol/m²/s, `quantity_kind="PPFD"`, `status=AVAILABLE`, incident-only semantics, provenance linking both contracts, no borrowed physics from photosynthesis / carbon / growth.

## Equation (legal only when all 10 conditions verified)
PPFD_target = PPFD_ref × T
- PPFD_ref: `AbsolutePPFDReference.ppfd_value` (≥0, finite, `unit="umol_photons_m2_s"`, `spectral_band="PAR_400_700"` or `EPAR_400_750`)
- T: `SpatialPPFDTransferFactor.transfer_value` (≥0, finite, `transfer_unit="dimensionless"`, same `reference_id`, same `simulation_time_ref`, `component="total"` baseline; per-component deferred)
- Output: `PPFDSource.value` same unit; `derivation_source_ids=[ref_id, transfer_id]`

## Reference geometry (step 4 — explicit, no silent swap)
- `AbsolutePPFDReference.reference_geometry`: ABOVE_CANOPY / OPEN_SKY / GARDEN_REFERENCE_PLANE / LOCAL_REFERENCE_SENSOR / OTHER_EXPLICIT
- `SpatialPPFDTransferFactor` has NO `reference_geometry`; denominator context = reference geometry
- Adapter requires `reference_geometry_compatible=True`; if false → `NOT_COMPUTABLE`; no automatic mapping; orientation/optics limitations preserved (coarse)

## Time / spectral / unit / identity checks (verified by adapter + tests)
- Time exact (`ref.simulation_time_ref == xfer.simulation_time_ref`); no interpolation; mismatch → `NOT_COMPUTABLE`
- Spectral domain preserved (PAR_400_700); unsupported -> `NOT_COMPUTABLE` (reference model validates)
- Unit preserved (`umol_photons_m2_s`); rejected by `PPFDSource` validator if wrong
- Reference identity (`reference.ref_id == transfer.reference_id`); mismatch -> `NOT_COMPUTABLE`
- Zero reference allowed (`ppfd_ref == 0` → target `0`, no epsilon fabrication)
- Negative reference / non-finite -> `ERROR`; negative transfer blocked by contract (`ge=0`); non-finite blocked
- T > 1 allowed (no clamp); T == 0 allowed (target 0)

## Incident / absorbed boundary (step 8, 20)
- `exposure_type` implicit = incident; `note` explicitly states "No absorbed PAR / APAR / optical model applied"
- No reflectance/transmittance; no leaf-angle cosine; no absorption coefficient; no `g_C`/`g_DM`
- No `lux`, `W/m²`, `µmol/J`

## Organ identity (step 9)
- `target_organ_id` preserved on adapter call; `derivation_source_ids` links to source contracts; no nearest-organ lookup / interpolation / topology inference
- Source ID deterministic (`derived_{ref_id}_{transfer_id}_{organ}`)

## Provenance / lineage (step 10, 13)
- `provenance` includes `ref_id`, `ppfd_ref`, `transfer_id`, `T`, `time_align`, `component`, `synthetic`
- `derivation_method` documented explicitly
- Synthetic fixtures labeled (`is_synthetic_example`); measured fixtures (`REF_A` `source_type="MEASURED"`) preserved
- `uncertainty_absolute` preserved via provenance note; propagation deferred (not fabricated)

## Direct/diffuse/reflected (step 16)
- Baseline `component="total"`; per-component derivation deferred; adapter allows non-total with explicit deferred note; no independent direct×T_direct etc.

## 046O relationship (step 12)
- `046O` (measured PPFD → `PPFDSource` → `OrganLightExposure`) untouched; adapter produces `PPFDSource` that could serve as `046O` input, but does not modify 046O contracts or assume all measured points are valid references.

## Static audit (step 22)
- No `getattr`/`hasattr` fallback; no `lux`; no `W/m2`; no `µmol/J`; no `g_DM`; no `absorbed`; no `ARPAR`; no `interpolation`; no `nearest`; no `epsilon`; no arbitrary multiplier; no hidden relative_normalized×constant

## Tests (step 21)
- Fixtures: `fixtures_046v.py` (A/B/C/D/K/U synthetic)
- Assertions: `tests/simulation/test_task046v_quick.py` — A–AB pass (21 assertions)
- A: 1000×0.5=500; B: 1.5→1500; C: 0→0; D: T=0→0; I: time mismatch blocked; K: geometry incompatible blocked; L: identity mismatch blocked; M: provenance/derivation IDs; N: provenance preserved; O: synthetic labeling; P: uncertainty preserved; Q: immutability; R: determinism; S: unit integrity; T/U/V/W/X/Y/Z/AA/AB: boundary checks

## Files changed (only new / unmodified upstream)
- New: `simulation/core/physiology/combine_reference_transfer.py`
- New: `simulation/core/physiology/fixtures_046v.py`
- New: `tests/simulation/test_task046v_quick.py`
- New: `TASK_046V_COMPLETE.md`
- Unchanged: `absolute_ppfd_reference.py`, `spatial_ppfd_transfer_factor.py`, `ppfd_source.py`, `organ_light_exposure.py`, `derive_spatial_transfer.py`, fixtures/tests 046T/U, light contracts, carbon/physiology upstream

## Pytest status
`PYTEST_UNAVAILABLE` (direct `python3` assertions verified; pytest binary not available in session; no silent skip)

## Orientation limitation (step 16, preserved)
`note` states orientation/optics limitations preserved (coarse); full physical surface-irradiance / angle / local-reflection model deferred; not invented.

## Next step
Integration into `OrganLightExposure` (046O path): `PPFDSource` → `OrganLightExposure(incident, ppfd_value=...)`; calibration/validation against measured sensors required before biological use; no photosynthesis/carbon called.
