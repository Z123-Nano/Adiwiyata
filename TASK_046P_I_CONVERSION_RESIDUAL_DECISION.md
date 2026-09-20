# TASK 046P-I — Conversion Residual Destination Decision
Status: TASK_046P_I_C — EFFECTIVE_COEFFICIENT_ONLY (operational); contract ambiguity (D) acknowledged (destination undefined). No implementation of NSC/storage/loss; no mutation of existing contracts.
Date: 2026-09-18; Mode: LOCAL/OFFLINE; sources: 046P-H audit + provided research + executable repo.

## 1. Executive verdict
C — EFFECTIVE_COEFFICIENT_ONLY, with explicit acknowledgment that D (contract ambiguity) remains true: the executable 046J defines retention as a structural conversion fraction but provides no contract for conversion_residual when retention < 1. The residual is therefore DELIBERATELY UNMODELED — not reserve, not respiration, not NSC, not loss. Do NOT add to 046P-G reserve. Do NOT invent storage/NSC/loss mechanism. Document as unmodeled; require explicit destination contract (NSC or conversion-loss) before closing carbon accounting.

## 2. Research basis supplied (used as context; not runtime dependency)
FSPM framework distinguishes source acquisition / common-pool allocation / structural growth / reserve / NSC / respiration / other fluxes; residual assimilates can be stored in reserve when sink demand fully satisfied; structural biomass and NSC are distinct; residual must not automatically become respiration/heat/reserve/NSC/exudation/mortality without explicit contract. Used only for decision framing; no external claims made.

## 3. Actual 046J executable semantics (verified 046P-H)
structural = allocated × growth_retention_fraction (ge 0..1, synthetic SYNTHETIC, un calibrated)
biomass = structural / carbon_fraction_of_dry_biomass (gt 0..1, synthetic)
Result object: structural_carbon_increment_g_C, biomass_increment_g_DM, previous biomass preserved, geometry_updated=False, provenance "TASK 021 respiration handled upstream; no second respiration deduction."
No conversion_residual field; no NSC field; no storage field; no loss field.

## 4. Current carbon ledger (two distinct branches, not merged)
Branch A — allocation surplus (046P-G): available → allocatable → allocated + unallocated → reserve_next = unallocated (MODEL A passive residual). This applies to carbon NEVER assigned to an organ.
Branch B — conversion (046J): allocated → structural (retention) → biomass (g_DM). Residual = allocated − structural = allocated × (1 − retention). This applies to carbon ASSIGNED to organ but not converted structurally. Distinct physical meaning; must remain separate.
Merge forbidden by 046P-G contract and by 046J provenance.

## 5. Definition of conversion residual
conversion_residual_carbon_g = allocated_carbon_g × (1 − growth_retention_fraction)  [g_C]
For retention = 1: 0. For retention = 0.5, allocated = 1.0: 0.5 g_C.
Not structural. Not biomass. Not unallocated. Explicitly unaccounted until destination contract exists.

## 6. Distinction from allocation surplus (046P-G preserved)
unallocated_carbon_g = source_available − total_allocated (from 046I). Reserve_next = unallocated.
conversion_residual_carbon_g = allocated − structural (from 046J).
Different input quantities; different physical meaning; different rules; never summed; verified by construction (no adapter; test L asserts separation).

## 7. Candidate comparison
I-A NSC_STORAGE_REQUIRED: would require new NSC state, remobilization rules, capacity, calibration against storage observations. Not supported by executable; no calibration feasible with current measurements; not selected.
I-B EXPLICIT_LOSS_REQUIRED: would require explicit loss mechanism (respiration separate from 021? heat? exudation?) and calibrated coefficient. Not defined executable; not selected.
I-C EFFECTIVE_COEFFICIENT_ONLY: matches executable (retention is synthetic coefficient with no destination defined); requires explicit "NOT MODELED" documentation; selected.
I-D CONTRACT_AMBIGUITY: true — executable does not specify destination; acknowledged as companion to C.

## 8. Respiration double-count audit (clean)
TASK 021 respiration handled upstream (046J provenance). No second deduction at growth. Conversion residual is NOT respiration; must NOT be classified as respiratory loss unless separate respiration contract defines it explicitly (current: none). No path exists to deduct residual as respiration.

## 9. Observability / identifiability
Current observations: biomass time series, organ geometry, destructive biomass, PPFD/light, water, nutrient, environment. None distinguish NSC vs structural vs conversion efficiency. Retention is synthetic/un calibrated (source_type=SYNTHETIC). Separate identification of retention vs sink demand requires either: destructive NSC measurement, labeled carbon tracing, or controlled growth experiments — none currently available. Therefore A/B not identifiable; C is only defensible baseline.

## 10. Calibration implications
Retention calibration impossible without NSC/structural separation measurements. If future NSC measurements added, could calibrate retention + NSC destination together; currently retention is a synthetic placeholder. No validation of retention value against empirical data (explicit per fixtures provenance).

## 11. Final decision (exact)
C — EFFECTIVE_COEFFICIENT_ONLY, with D acknowledged.
Operational rules:
- retention = structural conversion fraction (executable contract preserved).
- conversion_residual = allocated × (1 − retention) [g_C] — explicitly UNMODELED.
- DO NOT add to reserve_next (046P-G unchanged; reserve = unallocated only).
- DO NOT label as respiration (021 handles upstream; no second deduction).
- DO NOT label as NSC/storage/loss/heat/exudation/mortality (no contracts exist).
- Document as unmodeled residual; require explicit ConversionResidualContract (NSC destination or conversion-loss mechanism) before closing carbon ledger at growth boundary.
- Conservation status: PARTIAL (not CLOSED) when retention < 1. Closed only when retention = 1.0 OR destination contract defines residual.

## 12. Required next contract (explicit, not invented)
Create `ConversionResidualContract` (or extend `PostGrowthCarbonState`) defining:
- conversion_residual_carbon_g (explicit output from 046J)
- allowed destinations: STORAGE/NSC (with NSC state + remobilization), LOSS (with explicit loss process/provenance + calibration), UNMODELED (current baseline)
- constraint: reserve_next (046P-G) must NOT include conversion_residual unless destination = STORAGE and explicit storage→reserve transition defined
- status: RESIDUAL_UNACCOUNTED / RESIDUAL_TO_STORAGE / RESIDUAL_TO_LOSS / NOT_COMPUTABLE
Until this contract exists: keep C baseline; report unaccounted; do not silently assign.

## 13. Files inspected (read, unchanged)
- simulation/core/growth/growth_derivation.py (046J executable — audited; NOT modified)
- simulation/core/growth/growth_conversion_params.py (param contract — unchanged)
- simulation/core/growth/fixtures_046j.py (synthetic)
- simulation/core/physiology/post_allocation_state.py (046P-G — unchanged; reserve rule preserved)
- simulation/core/carbon/pool.py; allocation contracts; upward contracts (020/021/046G/046I)
- TASK_046P_H_PARTIAL.md (preceding audit)

## 14. Files changed
Created:
- TASK_046P_I_CONVERSION_RESIDUAL_DECISION.md (this report)
No code/edit created; no contract implemented (per Step 9: decision audit only, no NSC/storage/loss/reserve mutation).

## 15. Tests / audits
Used 046P-H assertions (A-O pass) as verification that: retention equation correct, structural/biomass derivation correct, no reserve double, no second respiration, surplus ≠ residual, immutability/determinism/provenance preserved. No new assertions needed (decision task, not implementation).

## 16. Limitations
- No destination contract implemented (deliberate; C baseline requires documentation, not invention).
- No calibration of retention (explicit synthetic; unchanged).
- No empirical NSC validation available.
- Carbon conservation claimed only when retention = 1.0 or when destination contract exists; otherwise reported PARTIAL/unmodeled.
- 046P-G reserve equation unchanged; 046J executable unchanged; no cross-task mutation.
