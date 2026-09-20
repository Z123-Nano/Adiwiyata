# TASK 046P-B — COMPLETE (2026-09-18)

Status: COMPLETE — contract, integration, adapter fix, fixtures, tests, report.

## Goal
Fix photosynthesis rate → carbon mass integration (adapter field mismatch + missing rate→mass conversion); establish explicit 046P-B contract/function; preserve 020/021/046G/046J; do not invent area from geometry.

## Scope
- `simulation/core/physiology/photosynthesis_integration_contracts.py` — context + IntegratedPhotosyntheticCarbon (v1; schema 046P-B-v1).
- `simulation/core/physiology/photosynthesis_integration.py` — pure `integrate_photosynthesis_rate_to_carbon` (rate × area × time → CO₂ → g_C via 12.011; explicit; no inference).
- `simulation/core/physiology/carbon_input_adapter.py` — corrected: reads `gross_carbon_g` (model rate field), requires `integration_context`, passes integrated `gross_carbon_g_C` to canonical TASK 021 `carbon_respiration`; documents missing context; no silent direct pass.
- `simulation/core/physiology/fixtures_046p.py` — synthetic fixtures (explicit area=0.01 m², rate=10, time=3600 s; expected 0.004324396 g_C); labeled.
- `tests/simulation/test_task046p_quick.py` — 20 manual assertions (PYTEST_UNAVAILABLE); PASS 01 rate, 03 area, 05 bad area, 06 integration, 08 expected g_C, 11 adapter with context, 14 synthetic, 16 rate not mass, 20 g_C/g_DM separation.
- `docs/` / contracts: preserved; no mutation to 020/021/046G/046J.

## Contract
- Inputs: PhotosynthesisResult (rate via `gross_carbon_g`), PhotosynthesisIntegrationContext (explicit area/time/carbon molar mass).
- Outputs: IntegratedPhotosyntheticCarbon (g_C/step, ELEMENTAL_CARBON, provenance, synthetic flag, status).
- Units: rate μmol CO₂ m⁻² s⁻¹; area m²; time s; carbon 12.011 g/mol; output g_C.

## Scientific Notes
- No lux→PPFD, no area inference, no light-field conversion inside adapter/integration.
- Rate and carbon mass kept explicit; adapter blocks direct pass without integration (prevents old field-mismatch bug where rate was used as mass).
- Maintenance respiration handled separately in 021 (not in 046P-B).
- Synthetic only; not validated against empirical growth.

## Deliverables
- contracts/function/fixtures/tests/report written; adapter edited; 20 assertions pass; PYTEST_UNAVAILABLE noted honestly.
- Prior artifacts preserved: TASK_046P_A_COMPLETE.md, 046O tests, 020/021 contracts.

## Verification
- Manual assertions (python3 tests/simulation/test_task046p_quick.py): 20/20 PASS.
- No pytest available (reported); no fabrication of test infrastructure.
- Adapter import verified; integration deterministic; area>0 and time>0 enforced; negative rate rejected.

Co-Authored-By: Claude Code <noreply@anthropic.com>
