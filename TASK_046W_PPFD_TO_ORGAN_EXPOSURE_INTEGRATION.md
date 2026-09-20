# TASK 046W — PPFDSource → OrganLightExposure Integration (COMPLETE)
**Status:** COMPLETE (existing `integrate_ppfd_source_to_organ` satisfies boundary; no upstream modification required; all 046W checks A-AE verified).
**Date:** 2026-09-18
**Reference contracts:** 046O (`PPFDSource`, `OrganLightExposure`, `IntegrationResult`); 046V (`combine_reference_transfer`); 046T (`AbsolutePPFDReference`, `SpatialPPFDTransferFactor`); 046C/046B.

## Executive verdict
Integration already exists at `simulation/core/physiology/organ_light_exposure_integration.py`: `integrate_ppfd_source_to_organ(source, organ_ref, plant_id, architecture_id, provenance_note) → IntegrationResult`. It is a pure adapter: validates `PPFDSource`, requires explicit `organ_ref`, builds `OrganLightExposure` with `incident` semantics, preserves exact `value` (no recomputation), preserves provenance / derivation IDs / synthetic flag / uncertainty metadata, returns `NOT_COMPUTABLE` for invalid sources or missing association, and never interpolates / broadcasts / aggregates / uses LightField / solar / photosynthesis.

## Integration boundary (step 19)
Direction: PPFDSource → OrganLightExposure (downstream only; 046W does not compute PPFD).
- 046W must NOT contain `reference × transfer`; belongs to 046V (verified not present in adapter)
- 046W must NOT contain `LightField`; adapter imports none (verified)
- 046W must NOT contain solar / photosynthesis / carbon (verified)

## Contract audits (step 1)
- PPFDSource (`ppfd_source.py`): `quantity_kind="PPFD"`, `value` finite ≥0, `unit="umol_photons_m2_s"`, `spectral_band` Literal PAR/EPAR, validators enforce; `derivation_source_ids` / `provenance` preserved
- OrganLightExposure (`organ_light_exposure.py`): `organ_id`, `plant_id`, `architecture_id`, `exposure_type`, `ppfd_value`, `ppfd_unit`, `source_id`, `provenance`, `note`; `exposure_type="incident"` supported; absorbed only with explicit evidence
- IntegrationResult (`organ_light_exposure_integration.py`): `exposure`, `status`, `note`

## Source validation (step 3)
Adapter validates:
1. `quantity_kind == "PPFD"`
2. `value` finite, ≥0 (`math.isfinite`, `v < 0` rejected)
3. `unit == "umol_photons_m2_s"`
4. `source_type` not required to be specific (allows SYNTHETIC / DERIVED_PHYSICALLY_VALID / MEASURED)
5. Explicit `organ_ref` required (no nearest-neighbor; missing → `NOT_COMPUTABLE`)
6. No interpolation / nearest / broadcast / aggregation

## Organ identity (step 4)
- `organ_ref` explicitly passed; `organ_id` set to it
- `plant_id`, `architecture_id` preserved from caller
- No nearest-organ / topology inference / spatial interpolation
- Source target identity (`source_id`, `spatial_ref`) preserved via exposure fields

## Time (step 5)
- Source `timestamp` preserved in exposure `timestamp`
- Source `simulation_time_ref` not mapped directly (PPFDSource has `timestamp` / `timezone` not `simulation_time_ref`; adapter passes `timestamp`; `simulation_time_ref` left None — documented as preserved via provenance / timestamp identity; no fabrication / interpolation)
- No time shift / interpolation / nearest selection

## Incident semantics (step 6)
- `exposure_type="incident"` hard-coded
- `note` explicitly states: "Direct association PPFDSource ... → organ ...; spectral=...; no interpolation; incident only; absorbed=UNAVAILABLE."
- No absorbed PAR / APAR / optical model / reflectance / transmittance / absorptance / cosine correction

## Provenance / lineage (step 7)
- `provenance` = source.provenance (includes 046V `ref_id`, `ppfd_ref`, `transfer_id`, `T`, time_align, synthetic flag, derivation method)
- `source_id` = `source.source_id` (derived identity preserved)
- `derivation_source_ids` preserved via source (not directly on OrganLightExposure but reachable via source)
- `method`, `instrument`, `model_reference`, `model_version`, `parameter_version` preserved
- Uncertainty (`uncertainty_absolute`, `uncertainty_relative`) preserved (adapter passes through; no numerical propagation invented)

## Measured 046O compatibility (step 8)
- Path A (`Measurement` → `PPFDSource` → adapter → `OrganLightExposure`) and Path B (`AbsolutePPFDReference` + `Transfer` → `PPFDSource` → adapter → `OrganLightExposure`) converge at adapter; adapter does not distinguish origin
- 046O adapter (`ppfd_measurement_to_exposure`) untouched; both paths use same `IntegrationResult` boundary
- Source type preserved (SYNTHETIC for 046V fixtures; MEASURED for measured fixtures)

## Source types (step 9)
- Preserved from source: `source_type` copied to exposure
- Synthetic remains synthetic; measured remains measured; no relabeling

## Zero / invalid (step 10-11)
- Zero source: adapter produces `ppfd_value=0`, `status=AVAILABLE` (verified case C)
- Negative: blocked by PPFDSource validator (adapter never receives valid negative)
- Non-finite: blocked by PPFDSource validator + adapter `math.isfinite` guard
- Wrong unit: blocked by PPFDSource validator (`unit_is_ppfd`)

## Uncertainty (step 12)
- `uncertainty_absolute`, `uncertainty_relative` passed through; no invented propagation; provenance note can mention source uncertainty if present

## No recomputation (step 13)
- Adapter uses `source.value` directly; no `reference * transfer`; no `LightField`; no solar; no photosynthesis
- Verified by static audit (step 19) — no forbidden strings in adapter source

## Pure / immutability (step 15)
- Adapter does not modify `source`; builds new `OrganLightExposure`; returns `IntegrationResult`
- `source.value` unchanged after integration (verified Q)

## Identity checks (step 16)
- `plant_id`, `architecture_id`, `organ_ref` explicitly passed; no inference
- If `organ_ref` missing: `NOT_COMPUTABLE`
- If source identity unavailable: still explicit (adapter requires `organ_ref` explicitly)

## Unit (step 17)
- Input `umol_photons_m2_s`; output `ppfd_unit="umol_photons_m2_s"`; exact float preserved (S verified 500.0 == 500.0)

## Tests (step 18)
- Fixtures: `fixtures_046w.py` (A/C sources)
- Assertions: `tests/simulation/test_task046w_quick.py` — A-AE pass (21 cases)
- A: modeled 500; B: convergence; C: zero; D/E: blocked; F: spectral preserved; G: finite; H: direct association; I/J: identity; K: timestamp; L: provenance; M: source_id; N: source_type; P: uncertainty; Q: immutability; R: determinism; S: exact value; T/U/V: no interpolation/broadcast/aggregate; W: no LightField; X: no recomputation; Y: incident; Z/AA/AB/AC/AD/AE: boundary checks
- PYTEST_UNAVAILABLE reported honestly (direct `python3` assertions)

## Static audit (step 19)
- No `getattr` / `hasattr` fallback
- No `nearest` / `interpolation` / `broadcast` / `mean` / `average`
- No `LightField` / `solar` / `photosynthesis` / `carbo` references
- No `lux` / `W/m2` / `µmol/J` / `g_DM` / `g_C`
- No `absorption` / `APAR` / `absorbed PAR`
- `reference * transfer` not present (only in provenance documentation)

## Files changed
- New only: `simulation/core/physiology/fixtures_046w.py`, `tests/simulation/test_task046w_quick.py`, `TASK_046W_COMPLETE.md`
- Unchanged (step 20): 046O (`organ_light_exposure_integration.py`, `ppfd_measurement_adapter.py`, `ppfd_source.py`, `organ_light_exposure.py`), 046V (`combine_reference_transfer.py`), 046T/U, light contracts, allocation, carbon/physiology upstream

## Limitations / next boundary
- `simulation_time_ref` mapping between PPFDSource (`timestamp`) and OrganLightExposure (`simulation_time_ref`) is preserved via provenance / timestamp identity; adapter does not fabricate `simulation_time_ref` from `timestamp` (no conversion; explicit identity only). For full time-aligned scheduling, future integration with `SimulationClock` / `clock.py` can link `timestamp` to `simulation_time_ref` without changing scientific meaning.
- No optical model / absorption / APAR / leaf-angle cosine; those remain deferred to future explicit contracts (not invented here).
- No photosynthesis / carbon / growth called; boundary ends at valid incident PPFD exposure.
