# TASK 046X — OrganLightExposure → Photosynthesis Audit (COMPLETE)
Status: COMPLETE (audit only; existing 046D adapter valid; no upstream modifications; all executable assertions A-V pass).

## Executive verdict
TASK 020 (`photosynthesis.py`) uses incident PPFD directly: `A = (alpha * Amax * PPFD) / (alpha * PPFD + Amax)` with `PPFD` in `µmol photons m^-2 s^-1`. This matches `OrganLightExposure` (incident, PAR 400-700, same unit). No absorbed PAR / APAR / optical conversion required. Existing 046D adapter (`photosynthesis_from_organ_exposure`) passes `ppfd_value` directly; no recomputation, no interpolation, identity preserved, provenance preserved, source type preserved, zero valid, negative blocked upstream.

## Key findings (executable)
- 020 input: `PPFDInput.ppfd` (float, µmol/m²/s); `source` literal (synthetic/measurement/modeled/unknown)
- 020 output: `PhotosynthesisResult.gross_assimilation` (µmol CO2/m²/s rate); `gross_carbon_g` (integrated g_C per timestep) from 046P/021 — adapter passes rate path; no reintegration
- 020 equation: rectangular hyperbola; synthetic params (`PARAM_PROVENANCE` explicit); not calibrated
- 020 has no respiration term; 021 handles respiration separately (no duplication)
- Incident vs absorbed: 020 expects incident; if absorbed required → CONTRACT_GAP; not needed (020 uses incident directly)
- Measured (046O) + modeled (046V) paths converge at same 046D adapter (source-agnostic)
- Zero PPFD valid → rate 0 (verified C)
- Negative/non-finite blocked by upstream PPFDSource / OrganLightExposure validators
- No LightField / solar / interpolation / aggregation / nearest / broadcast / area inference in adapter
- Unit chain: PPFD µmol/m²/s → rate µmol CO2/m²/s (different var; no conversion)
- Time: instantaneous rate per exposure timestep; adapter passes current value; no integration inside 020

## Status per spec
COMPLETE — integration structurally correct, no missing contract for this boundary, no design change needed, no absorbed PAR gap.

## Files changed
New audit-only: fixtures_046x.py, test_task046x_quick.py, TASK_046X_ORGAN_EXPOSURE_PHOTOSYNTHESIS_AUDIT.md. Zero upstream modifications.

## Pytest
PYTEST_UNAVAILABLE (direct python3 assertions A-V verified).
