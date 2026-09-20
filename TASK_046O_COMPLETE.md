# TASK 046O — Measured PPFD → PPFDSource → OrganLightExposure (COMPLETE)

Status: TASK_046O_COMPLETE
Decision: Explicit measured PPFD path established; LightField→PPFD conversion explicitly absent; architecture-independent.

## A. Exact measurement input contract

Measurement (simulation/core/contracts/domain.py): variable/variable (str), value (float >=0 required by validator), unit (str), timestamp (datetime), spatial_ref (dict optional), instrument/method/calibration_ref/observer_source/uncertainty/provenance/is_synthetic_example.
Adapter validates: variable=="PPFD"; unit=="umol_photons_m2_s"; value finite >=0.
No organ_ref in Measurement — must be provided explicitly to adapter.

## B. PPFD validation

Rejected: lux (variable/illuminance), relative_normalized, negative value, NaN/inf, missing value, unknown unit.
Zero (0.0) valid.
Unit must exactly match "umol_photons_m2_s"; no silent conversion.
Spectral semantics preserved via PPFDSource.spectral_band="PAR_400_700" (046B contract).

## C. Organ association rule

Explicit only: adapter takes organ_ref argument; no nearest-neighbor; no spatial interpolation; no broadcast.
If organ_ref missing → NOT_COMPUTABLE.
Measurement spatial_ref preserved but never used to infer organ.

## D. Time semantics

timestamp preserved as ISO string on PPFDSource; no conversion to simulation_time; no wall-clock substitution.

## E. Provenance

Measurement → PPFDSource (source_id=measurement.id; provenance includes measurement provenance + TASK_046O note + synthetic flag) → IntegrateResult (exposure provenance includes source reference, method, instrument, task note).
Synthetic fixtures explicitly is_synthetic_example=True and source_type=SYNTHETIC.

## F. 046B reuse

PPFDSource (simulation/core/physiology/ppfd_source.py) reused directly; validators (finite non-negative, quantity_kind=PPFD, unit correct) preserved.
No second PPFD contract created.

## G. 046C reuse

integrate_ppfd_source_to_organ() (simulation/core/physiology/organ_light_exposure_integration.py) reused directly; requires explicit organ_ref; returns NOT_COMPUTABLE if missing; exposure_type=incident; ppfd_unit preserved.
No duplication of integration logic.

## H. LightField separation (step 13 verified)

Adapter imports only contracts + 046B/046C; no import of light/compute/field.
Test conclusion: LightField.available does not imply PPFDSource.available; 046N can branch correctly.
No LightField→PPFD conversion in adapter.

## I. Synthetic fixture semantics

MEASURED_PPFD_01 labeled is_synthetic_example=True; adapter sets source_type=SYNTHETIC; never appears as MEASURED.
No fabricated field measurements.

## J. Tests / validation

tests/simulation/test_task046o_quick.py — 20 assertions pass (manual); PYTEST_ENVIRONMENT_UNAVAILABLE reported honestly.
PASS 01 valid; 02 units; 03 spectral; 04 zero; 05 negative; 07 lux rejected; 08 relative_normalized rejected; 09 organ ref; 10 missing organ rejected; 11 no nearest-neighbor (by design); 12 timestamp; 13 provenance; 14 046B; 15 046C; 16 immutability; 17 det; 18 synthetic; 19 separation; 20 046N compatibility.

## K. Limitations / explicit separation

This task establishes measured physical PPFD input only.
It does NOT derive PPFD from LightField (coarse relative_normalized remains unavailable for physiology).
Architecture-dependent physical PPFD (architecture → occluders → incident PPFD field) remains a future radiation-model task with its own explicit physical assumptions.

TASK_046O_COMPLETE
