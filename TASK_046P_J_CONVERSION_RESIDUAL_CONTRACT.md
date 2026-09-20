# TASK 046P-J — ConversionResidualContract (explicit boundary; no destination implemented)
Status: TASK_046P_J_COMPLETE (contract executable, tests pass, gating enforced); OVERALL CARBON LEDGER remains PARTIAL (retention < 1 residual unmodeled until NSC/loss contract exists).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; sources: 046P-H audit + executable repo + provided research.

## 1. Executive verdict
Explicit ConversionResidualContract created (pure, immutable, validated). Baseline destination = UNMODELED. STORAGE and LOSS permitted only with explicit references (gating enforced). No NSC/storage/loss/remobilization/respiration/geometry mutation implemented. 046J executable unchanged; 046G/046I/046P-G unchanged. Conservation identity at growth boundary is arithmetic (allocated = structural + residual) but biological closure remains PARTIAL until physical destination contract implemented.

## 2. Research basis (supplied context only)
FSPM distinguishes source, allocation, structural, reserve/NSC, respiration, other fluxes; NSC/reserve may be additional sink when relevant; structural biomass and NSC distinct; residual must not automatically become respiration/heat/reserve/NSC/exudation/mortality without explicit contract. Used only for framing; no external claims.

## 3. Executable 046J equation (verified, unmodified)
structural = allocated × growth_retention_fraction (ge 0..1, synthetic SYNTHETIC)
biomass = structural / carbon_fraction_of_dry_biomass (gt 0..1, synthetic)
Result provenance: "TASK 021 respiration handled upstream; no second respiration deduction." No NSC/storage/loss fields.

## 4. Contract definition (new file)
File: simulation/core/physiology/conversion_residual_contract.py
Class: ConversionResidualContract (Pydantic BaseModel, v1)
Fields: result_id, plant_id, architecture_id, source_allocation_id, allocated_carbon_g, retention, structural_carbon_g, conversion_residual_carbon_g, destination (UNMODELED/STORAGE/LOSS), storage_reference (required if STORAGE), loss_reference (required if LOSS), status, timestep, simulation_time_ref, provenance, note, schema_version, parameter_version, is_synthetic_example.
Validation: structural equation; residual equation; conservation identity; destination gating; negative allocation rejected; retention [0,1]; no getattr/hasattr fallback.
Function: build_conversion_residual_contract (pure, no mutation of inputs or upstream contracts).

## 5. Conservation equation (accounting identity at boundary)
allocated_carbon_g = structural_carbon_g + conversion_residual_carbon_g
Verified by model_validator (tolerance 1e-6). This is an arithmetic decomposition, not biological closure until destination is defined.

## 6. Meaning of residual (explicit)
conversion_residual_carbon_g = allocated × (1 − retention)  [g_C]. When retention < 1, explicitly identified, preserved, reported; not silently lost; not automatically reserve/respiration/NSC/loss.

## 7. UNMODELED baseline rationale
Matches executable (no destination contract exists). Explicitly documents that carbon accounting stops at structural + residual; physical destination requires future contract. Prevents silent disappearance. Status in contract note: "UNMODELED unless STORAGE/LOSS contract provided; PARTIAL until destination defined."

## 8. Relationship to 046P-G reserve
Strict invariant preserved: reserve_next = unallocated_carbon_g (allocation surplus only). Conversion residual never enters reserve_next (verified: no adapter; test F asserts separation; 046P-G unchanged). Only if future explicit STORAGE transition contract defines storage→reserve path may merge occur; not now.

## 9. Relationship to TASK 021 respiration
Respiration accounted upstream (046J provenance). Residual is NOT respiration; contract destination excludes RESPIRATION option (only UNMODELED/STORAGE/LOSS). No second deduction; no respiration field; no subtraction from residual.

## 10. Relationship to g_DM (046J boundary preserved)
Contract quantities all g_C (structural, residual, allocated, retention as fraction). No conversion_residual_g_DM. Biomass conversion remains only at 046J (structural / carbon_fraction → g_DM). Boundary clean.

## 11. STORAGE gating
If destination=STORAGE: model_validator requires storage_reference (explicit reference to storage-state/transition contract). No storage state created; no remobilization; no capacity; no NSC dynamics. Gating prevents silent storage assignment.

## 12. LOSS gating
If destination=LOSS: model_validator requires loss_reference (explicit loss-process provenance). No loss process defined; no respiration equated; no heat/exudation/mortality assigned automatically. Gating prevents silent loss classification.

## 13. Test results (synthetic labeled A-T, assertions only)
A retention 1.0 (residual 0); B retention 0.5 (residual 0.5); C retention 0; D surplus vs residual distinct; E respiration not double; F reserve unchanged; G identity; H units g_C; I negative rejected; J retention out of range rejected; K immutability; L determinism; M identity/provenance preserved; N STORAGE gated; O LOSS gated; P UNMODELED valid; Q no hidden fallbacks; R no reserve mutation; S no RESPIRATION option; T timestep identity.
All pass (python direct; exit 0). PYTEST_UNAVAILABLE reported honestly.

## 14. pytest status
Direct execution pass; pytest unavailable; not falsely claimed.

## 15. Files changed / unchanged
Created:
- simulation/core/physiology/conversion_residual_contract.py
- simulation/core/physiology/fixtures_046p_j.py
- tests/simulation/test_task046p_j_quick.py
- TASK_046P_J_CONVERSION_RESIDUAL_CONTRACT.md
Unchanged (preserved): 046J growth_derivation/growth_conversion_params/fixtures; 046G pool; 046I allocation; 046P-G post_allocation_state; 046P-H audit; 020/021 upstream.

## 16. Limitations / future contracts
- Contract executable; physical destination not implemented (deliberate per scope).
- Overall carbon ledger remains PARTIAL when retention < 1 (unmodeled residual).
- Future needed: ConversionResidualContract extension with STORAGE reference (NSC state + remobilization) OR LOSS reference (calibrated loss process). Only then can ledger claim closure for retention < 1.
- No active storage dynamics added (explicitly excluded per Step 12).
- No empirical calibration of retention (remains synthetic).
- g_C/g_DM boundary preserved; no conversion to g_DM inside contract.
