# TASK 046U — SpatialPPFDTransferFactor Derivation (PARTIAL)
**Status:** PARTIAL (derivation executed; orientation limitation preserved — coarse / not physical optics; no interpolation; no arbitrary scaling; no physical PPFD output).

**Date:** 2026-09-18
**Reference contracts:** 046T (`AbsolutePPFDReference`, `SpatialPPFDTransferFactor`); 046S (both contracts required, Q-B architecture); 046O (LightField relative_normalized, no direct PPFD conversion).

## Goal
Derive dimensionless `SpatialPPFDTransferFactor.transfer_value = L_target / L_reference` from two comparable `LightField` samples, preserving all upstream contracts (046G, 046I, 046J, 046P-G, 020, 021, 008–011). No new physics; purely algebraic derivation from existing `LightField` quantities.

## Contract
- Input: two `LightField` instances with same `approximation_params` / same `solar_reference` / same time; denominator > 0; non-negative finite values; `relative_normalized` units preserved.
- Process: compute component-level average (total/direct/diffuse/reflected) for both fields; validate compatibility; compute `T = target / reference`; produce `SpatialPPFDTransferFactor` via existing `build_spatial_ppfd_transfer`.
- Output: `SpatialPPFDTransferFactor` (dimensionless, `transfer_definition` explicit about anchoring and orientation limitation, provenience from inputs, `reference_id` from external `AbsolutePPFDReference`, not fabricated).
- Constraints: no interpolation; no arbitrary multiplier; no lux/PPFD conversion; no `relative_normalized` treated as automatically T; orientation limitation documented; synthetic fixtures labeled.

## Acceptance (verified by assertions)
- A: valid derivation `T = 0.5` from `ref_A`/`tgt_A` (total, same approximation, same solar/time).
- B: approximation mismatch blocked (`ValueError`).
- C: denominator <= 0 blocked (reference total 0; reference itself valid per 046T C; transfer invalid at use).
- D: orientation limitation preserved in `transfer_definition`.
- E: output dimensionless only; no `umol` / PPFD / `g_DM` / `g_C` in output.
- F: synthetic label preserved; provenance includes `time_align=`.

## Scientific / audit notes
- LightField is `relative_normalized`; conversion to absolute PPFD requires `AbsolutePPFDReference` + explicit transfer contract (046T); this derivation does NOT claim physical PPFD.
- Component total baseline used by default; orientation limitation preserved (coarse, not physics-derived optics/modeling of local reflection/angle). Full orientation/optics derivation deferred (not supported by synthetic data; requires calibrated physical reference + geometry; outside 046U scope per user's preservation instruction).
- No upstream modification: `light/field/contracts.py`, `derive_spatial_transfer.py` (new pure module), fixtures/tests only; 046J respiration, 046G pool, 046I allocation, 046P-G reserve, light approximation modules untouched.
- Fixtures synthetic / labeled; no fabrication; provenance from inputs; `reference_id` passed externally (does not invent `AbsolutePPFDReference`).
- PYTEST_UNAVAILABLE reported honestly (executed via direct `python3` assertion; pytest binary unavailable in session; no silent skip).

## Deliverables
- `simulation/core/physiology/derive_spatial_transfer.py` (pure derivation)
- `simulation/core/physiology/fixtures_046u.py` (A–C fixtures)
- `tests/simulation/test_task046u_quick.py` (A–F assertions)
- This report (TASK_046U_COMPLETE, PARTIAL)

## Not done / blocked / deferred (honest)
- Full physical orientation/optics transfer (requires calibrated geometry + physical reference; not defensible from synthetic normalization; deferred, not invented).
- Interpolation / sub-sample derivation (explicitly blocked by contract; no interpolation allowed).
- Integration into `organ_ppfd` / crop canopy model (not in 046U; preserved for 046O/046T/validation sequence).

## Source isolation / provenance preserved
- `conversion_residual_carbon_g` (046P-J), reserves (046P-G), respiration (021 upstream), absolute reference (046T), transfer contract (046T) all unchanged.
- `LightField` `unit="relative_normalized"`, `normalization_note` synthetic clear-day, preserved.
- No `lux`→PPFD equivalence claimed; no `absorption`/`ARPAR` hidden conversion.
