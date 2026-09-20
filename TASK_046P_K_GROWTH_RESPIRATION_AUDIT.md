# TASK 046P-K — Growth Respiration / Retention Semantic Audit
Status: TASK_046P_K_B — CONVERSION_EFFICIENCY_ONLY (retention = structural conversion fraction; residual unmodeled; growth respiration NOT supported by executable; double-count blocked by 021 upstream + 046J provenance).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; executable source = truth.

## 1. Executive verdict (B)
Retention is a structural conversion coefficient only (`growth_retention_fraction`, synthetic/un calibrated, description: "Fraction of allocated carbon retained for structural biomass"). The conversion residual (`allocated × (1 − retention)`) is NOT growth respiration; executable 046J explicitly says "no second respiration deduction" and has no growth-respiration field. TASK 021 respiration is upstream (`gross → net` via `respiration = gross * rate`). Interpreting residual as growth respiration would double-subtract carbon. Decision: B; A blocked; C unnecessary (interpretation already constrained); D not needed.

## 2. Supplied scientific basis (used as context)
FSPM distinguishes maintenance respiration, growth respiration, structural growth, NSC, reserve, other fluxes; growth respiration can be modeled as fraction of allocated carbon; but must be explicitly defined. Not automatically inferred from structural conversion coefficient.

## 3. TASK 046J executable semantics (verified, unmodified)
- `growth_conversion_params.py` line 10: `growth_retention_fraction` described as "Fraction of allocated carbon retained for structural biomass".
- `growth_derivation.py`: `structural = allocated * parameters.growth_retention_fraction`; `biomass = structural / carbon_fraction`; no respiration term; no construction-cost term.
- `fixtures_046j.py`: synthetic SYNTHETIC, provenance "TASK_046J synthetic; not calibrated".
- No fields: growth_respiration, construction_respiration, respiration_cost, loss, NSC.

## 4. TASK 021 executable semantics (verified, unmodified)
- `simulation/core/carbon/carbon.py`: `carbon_respiration(gross, rate=0.15)` → `respiration = gross * rate`; `net = gross - respiration`.
- Plant-level; upstream of pool/allocation; no organ-level growth respiration; no separate growth-respiration process.
- Provenance: "TASK_021 carbon/respiration v1".

## 5. Retention interpretation
Execution confirms: retention is structural conversion fraction (fraction of allocated carbon that becomes structural carbon). Not declared as growth efficiency, construction cost, biomass retention (in biological sense), or growth respiration. Synthetic parameter; not calibrated.

## 6. Conversion residual interpretation (from 046P-H / 046P-J)
`conversion_residual = allocated × (1 − retention)` = `UNMODELED_CONVERSION_RESIDUAL`. Contract `ConversionResidualContract` (046P-J) records it explicitly with `destination = UNMODELED`; `STORAGE`/`LOSS` gated; `RESPIRATION` excluded from vocabulary. Residual is NOT respiration.

## 7. Growth respiration compatibility (A vs B)
A (`GROWTH_RESPIRATION_SUPPORTED`) requires executable evidence that residual = growth respiration. Evidence against:
- 046J parameter name/description never mentions respiration or construction cost.
- 046J provenance (line 114): "TASK 021 respiration handled upstream; no second respiration deduction." → explicitly forbids second respiration at growth boundary.
- No growth-respiration field or equation in 046J.
- 021 already subtracts respiration at gross→net stage; applying again at allocated→structural would double-subtract.
- Residual is documented as UNMODELED (046P-H / 046P-I / 046P-J), not respiration.
Thus A is REFUSED by executable.

B (`CONVERSION_EFFICIENCY_ONLY`) supported: retention acts as structural conversion coefficient; residual remains unmodeled; no biological destination claimed.

## 8. Double-count audit (resolved)
Path: Photosynthesis gross → 021 respiration (gross → net) → CarbonPool (available) → 046I allocation (allocated) → 046J structural (allocated × retention) → residual (allocated − structural).
If residual interpreted as respiration: carbon subtracted at 021 AND at 046J = double subtraction.
If residual interpreted as reserve (046P-G): 046P-G reserve = unallocated (allocation surplus), not conversion residual — verified separate (test L from 046P-J).
If residual interpreted as NSC: no NSC contract exists (046P-J excludes).
No hidden path merges residual into respiration/reserve/NSC.
Verdict: NO double-count risk under B (residual unmodeled); double-count would occur only if interpreted as respiration (A) or reserve/NSC without contract.

## 9. Conservation equations (current executable)
At 021: gross = net + respiration (with rate 0.15 default).
At 046G: available = reserve + current_net (may be negative; sign preserved).
At 046I: source_pos = max(available, 0); allocated + unallocated ≈ source_pos (1e-6).
At 046J: structural = allocated × retention; biomass = structural / carbon_fraction.
At 046P-J boundary: allocated = structural + conversion_residual (accounting identity); biological closure PARTIAL until destination defined.
No equation claims biological closure for retention < 1.

## 10. Reserve relationship (preserved)
046P-G: reserve_next = unallocated_carbon_g (only). Contract 046P-J: conversion_residual explicitly excluded from reserve; STORAGE gating requires future contract. Unmodified.

## 11. NSC relationship (preserved, distinct)
No NSC state/transition/contract exists in executable. Residual not classified as NSC by 046J or 046P-J. NSC requires separate future contract.

## 12. Final decision (B)
B — CONVERSION_EFFICIENCY_ONLY.
Retention is a structural conversion coefficient; conversion residual is unmodeled; growth respiration is NOT supported by executable semantics; double-count risk prevents A; no ambiguity requires D; C unnecessary because interpretation already constrained.

## 13. Required future contract
If biological closure at growth boundary is desired when retention < 1, one of:
- Explicit growth-respiration contract (separate from 021, with calibrated coefficient, provenance, organ-level or plant-level distinction); OR
- Explicit NSC/storage contract with remobilization; OR
- Accept PARTIAL (current baseline) with residual explicitly documented as unmodeled.
Current recommendation: keep B; document PARTIAL; pursue future destination contract only when measurements support calibration.

## 14. Files inspected (read, unchanged)
- simulation/core/growth/growth_derivation.py (046J executable — audited)
- simulation/core/growth/growth_conversion_params.py (param contract)
- simulation/core/carbon/carbon.py (021 respiration — audited)
- simulation/core/physiology/conversion_residual_contract.py (046P-J — unchanged)
- TASK_046P_H_PARTIAL.md / TASK_046P_I_CONVERSION_RESIDUAL_DECISION.md (preceding audits)
- fixtures/tests from 046P-J (verified unchanged)

## 15. Files changed
None (audit only; no modification per Step 12 policy). Report only.

## 16. Tests / audits
Used 046P-J assertions (A-T pass) to verify: retention equation, structural/biomass derivation, no reserve mutation, no respiration double, immutability, determinism, provenance, gating, units. No new code modifications.

## 17. pytest status
Direct python verification pass; pytest unavailable; reported honestly.

## 18. Limitations
- Decision based on executable semantics + source provenance; no independent calibration of retention value.
- Biological growth-respiration mechanism is plausible scientifically (research basis) but unsupported by repository contracts; requires future explicit contract if needed.
- Residual remains unmodeled; ledger PARTIAL for retention < 1.
