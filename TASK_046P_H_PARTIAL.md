# TASK 046P-H — 046J Carbon Conversion / Retention Boundary Audit (PARTIAL)
Status: TASK_046P_H_PARTIAL — executable 046J equation verified; retention semantics explicit; conversion residual identified; destination contract missing; no invented sink; double-count clean.
Date: 2026-09-18; Mode: LOCAL/OFFLINE; sources: executable repo + provided research basis only.

## 1. Executive verdict
MODEL H-A (structural conversion efficiency) supported by executable. retention = growth_retention_fraction ∈ [0,1], applied as structural = allocated × retention; biomass = structural / carbon_fraction. Residual when retention < 1 is UNACCOUNTED_CONVERSION_RESIDUAL (not reserve, not respiration, not NSC, not heat, not exudation — no executable destination defined). Status PARTIAL because full end-to-end carbon conservation requires either retention = 1.0 or an explicit conversion-residual destination contract; neither is currently executable.

## 2. Actual 046J executable equations (verified from growth_derivation.py)
structural_carbon_increment_g_C = allocated_carbon_g × growth_retention_fraction
biomass_increment_g_DM = structural_carbon_increment_g_C / carbon_fraction_of_dry_biomass
new_biomass_g_DM = max(previous_biomass_g_DM, 0.0) + biomass_increment_g_DM
Constraints: allocated ≥ 0; previous ≥ 0; negative inputs blocked (NOT_COMPUTABLE, original preserved in provenance, no silent clamp).
Conversion residual (derived, not in executable result):
conversion_residual_carbon_g = allocated_carbon_g − structural_carbon_increment_g_C = allocated × (1 − retention)
Unit: g_C → structural g_C → biomass g_DM (046J boundary explicit; 046P-G/023 conversion boundary preserved).

## 3. Meaning of retention (executed, not inferred)
Parameter contract: GrowthConversionParameters.growth_retention_fraction ∈ [0,1], synthetic source (SYNTHETIC), provenance states "not calibrated". Executable applies it as multiplicative partition into structural carbon. It is a structural conversion fraction, not a generic efficiency coefficient alone (it partitions allocated carbon into structural vs unaccounted), and not a storage pool coefficient (no storage mechanics). Interpretation = MODEL H-A, with the explicit addition that the non-structural portion is unaccounted until a destination contract is defined.

## 4. Meaning of conversion residual (explicit, not merged)
conversion_residual_carbon_g = allocated × (1 − retention). For retention = 0.5, allocated = 1.0 → residual = 0.5 g_C. This residual is NOT:
- unallocated_carbon_g (allocation surplus — distinct, from 046I result, handled by 046P-G reserve rule)
- respiration (handled upstream by 046J provenance: "TASK 021 respiration handled upstream; no second respiration deduction")
- reserve_next (046P-G applies only to unallocated allocation surplus; growth residual never returned to pool; verified by construction: no adapter links growth result to reserve)
- NSC / storage / heat / exudation / mortality (no executable contracts exist for these destinations)
Therefore: unaccounted conversion residual. Must not be silently assigned to any category.

## 5. Relationship to respiration
Executable provenance explicitly states respiration is handled upstream (TASK 021) and no second deduction occurs at 046J. Audit confirms: no respiration field, no deduction equation, no loss classification in OrganGrowthResult. Retention < 1 does NOT imply respiratory loss; it implies incomplete structural conversion with undefined destination.

## 6. Relationship to allocation surplus (046P-G distinction preserved, not merged)
- Allocation surplus = unallocated_carbon_g from SourceSinkAllocationResult (046I); reserve_next = unallocated (MODEL A).
- Conversion residual = allocated × (1 − retention) from 046J; separate from surplus; never enters reserve; verified by absence of growth→reserve adapter and by structural assertion in test L.
No merge permitted without explicit contract.

## 7. Double-count audit (clean)
Tested paths:
- allocated → structural biomass (correct)
- same allocated → reserve (NO: no adapter; growth result never feeds reserve)
- structural → biomass AND separate respiration deduction (NO: provenance "no second respiration")
- retention residual → reserve while respiration already upstream (NO: residual unaccounted; no hidden sink)
- residual counted in both structural and biomass (NO: biomass derives from structural / carbon_fraction, not independently added)
Result: NO double-count path exists in executable code or adapters.

## 8. Carbon conservation status
When retention = 1.0: structural = allocated; biomass = structural / fraction; previous biomass preserved; conservation closed at growth boundary (assuming sub-1 carbon_fraction accounts for non-carbon mass correctly — fraction parameter is synthetic/un calibrated; note says "not calibrated").
When retention < 1.0: executable computes structural and biomass correctly but does not account for (1−retention)×allocated. Conservation is NOT closed at growth boundary. Status = PARTIAL (not BLOCKED — executable functions; missing only destination contract for residual). Recommended: either enforce retention=1 for closed ledger, or create explicit ConversionResidualContract defining destination.

## 9. Recommended next contract (explicit, not invented)
Create `ConversionResidualContract` / `PostGrowthCarbonState` defining:
- conversion_residual_carbon_g (explicit output)
- allowed destinations: storage/NSC (with NSC contract), respiration (only if separate from 021), structural_remobilization, or explicit loss (with calibrated coefficient and provenance)
- constraint: reserve_next (046P-G) must NOT include this residual unless destination = storage and an explicit storage→reserve transition contract defines the path
- status options: RESIDUAL_UNACCOUNTED, RESIDUAL_TO_STORAGE, RESIDUAL_TO_RESPIRATION (separate), NOT_COMPUTABLE (if retention boundary missing)
Until this exists: retention < 1 must be reported with unaccounted residual (current correct behavior); must NOT be silently mapped to reserve, respiration, or any other category.

## 10. Files changed / unchanged
Created:
- simulation/core/growth/fixtures_046p_h.py (A-C fixtures, synthetic)
- tests/simulation/test_task046p_h_quick.py (O assertions A-O, synthetic)
- TASK_046P_H_PARTIAL.md (this report)
Unchanged (preserved per rules / explicit audit requirement):
- simulation/core/growth/growth_derivation.py (046J executable — NOT modified; audited only)
- simulation/core/growth/growth_conversion_params.py (046J params — unchanged)
- simulation/core/physiology/post_allocation_state.py (046P-G — unchanged; reserve rule preserved separately)
- simulation/core/carbon/pool.py (046G); source_sink_allocation.py (046I); all upstream contracts (020/021/046P-G)
No mutation of CarbonPool, allocation result, growth inputs, or previous biomass.

## 11. Exact assertions passed (20 assertions A-O, synthetic labeled)
A retention=1 structural/biomass; B retention=0.5 structural=0.5/residual=0.5; C retention=0 structural=0; D residual explicit; E no second respiration; F g_C/g_DM boundary; G biomass derivation; H immutability; I determinism; J provenance; K timestep; L surplus ≠ residual; M no reserve double; N no hidden sink; O PARTIAL conservation diagnosis.
Python direct execution: all pass (exit 0). PYTEST_UNAVAILABLE reported honestly.

## 12. pytest status
Direct python execution of assertions: pass. pytest binary unavailable in environment; not claimed.

## 13. Limitations / explicit non-goals
- No destination contract for (1−retention)×allocated yet (this is the PARTIAL reason, explicitly documented).
- Growth parameters synthetic/un calibrated (source_type=SYNTHETIC; provenance states this).
- No geometry update (geometry_updated=False in result; 046K future).
- No integration with actual plant architecture state (pure derivation; architecture_id passed through but not modified).
- No empirical validation of retention values (not required for audit; calibration future).
- 046J unit g_DM vs 046P-G/023 g_C boundary explicitly preserved (note in result and params).

## 14. Final scientific invariant preserved
structural_carbon = allocated × retention (g_C)
biomass = structural / carbon_fraction (g_DM)
conversion_residual = allocated × (1 − retention) — UNACCOUNTED until conversion-residual destination contract exists.
No reserve double; no respiration double; allocation surplus (unallocated) and conversion residual remain distinct; 046G/046I/046J unchanged.
