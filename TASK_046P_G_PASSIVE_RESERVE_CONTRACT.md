# TASK 046P-G — Passive Residual Reserve Contract (MODEL A)
Status: TASK_046P_G_PARTIAL (contract executable; 046J retention boundary prevents full end-to-end conservation when retention < 1.0; no silent loss destination invented)
Date: 2026-09-18; Mode: LOCAL/OFFLINE; No web/search used; executable source = implementation truth

## 1. Executive decision
Implement MODEL A — passive residual reserve, minimal baseline. New pure contract PostAllocationCarbonState + compute_post_allocation_state. No active NSC/storage physiology added. Status PARTIAL because 046J (growth/conversion boundary) does not define where allocated - structural goes if retention < 1; contract reports this as unresolved rather than inventing a sink.

## 2. Research basis (provided by lead review, already reviewed externally)
FSPM common resource pool connects source and sink organs; residual assimilates stored; residual carried to next timestep; source insufficient → partitioned by relative sink strength; GreenLab uses common biomass pool with source-sink; residual remains. Used ONLY as context — not as runtime dependency (CLAUDE.md rule; MetaFSPM/CPlantBox/GreenLab not added to dependencies).

## 3. Current executable ledger (verified from source, unchanged by this task)
- 046G available = reserve + net (g_C); sign preserved; no automatic reserve-next.
- 046I source_available = CarbonPool.available_carbon_g; allocatable = max(source,0); conservation 1e-6; pool immutable.
- 046J boundary: allocated → structural → biomass g_DM; retention not fully defined executable for <1 case.
- 046P-E audit (preceding): reserve stays in pool after 046I; unallocated reported not converted; no reserve_next fabricated.

## 4. New passive-reserve equation (MODEL A)
reserve_next_carbon_g = unallocated_carbon_g   when source_available > 0
reserve_next_carbon_g = 0                     when source_available <= 0
carbon_deficit_g      = max(-source_available, 0)  when source_available < 0
Unit: g_C throughout. No g_C→g_DM inside contract (046J remains boundary).

## 5. Negative-source treatment
source_available < 0 → allocatable = 0 (existing 046I); reserve_next = 0; deficit explicit (not silent respiration/debt/biomass loss/stress). No clamping of CarbonPool.

## 6. Deficit semantics
Explicit reported quantity only: carbon_deficit_g = max(-available, 0). Not converted into any other category. Requires separate contract if later interpreted as respiration/debt/stress.

## 7. TASK 046J retention compatibility
Audit executable 046J: allocated_g_C → structural_carbon_g → biomass_increment_g_DM. If retention < 1.0 and executable provides no destination for difference, transition cannot claim full end-to-end conservation. Contract notes this; audit = PARTIAL; no automatic reserve/respiration/heat/exudation/storage-loss classification invented.

## 8. Timestep semantics
No SimulationClock advance; observation/sim time/organ age unchanged. Next reserve applies at next timestep's reserve_t. Sequence: reserve_t + net_t = available_t → allocation_t → unallocated_t → reserve_(t+1).

## 9. Identity/provenance
Prev pool id + prev allocation id preserved; plant_id / architecture_id / timestep / provenance / note preserved. No fabricated result/pool/source IDs; deterministic construction via scalar inputs; previous identity fields optional (None allowed). Synthetic fixtures labeled `is_synthetic_example=True`; provenance includes TASK_046P-G.

## 10. Conservation proofs / tests (all assertions, no print-only)
Test file: tests/simulation/test_task046p_g_quick.py — 20 assertions A-T pass.
Verified: A sufficient (0.30→reserve), B exact (0), C limited (0), D negative (deficit 0.40, reserve 0), E zero-demand (1.30→reserve), F surplus, G no double count, H deficit explicit, I pure (no mutation), J allocation unchanged, K determinism, L timestep 3600, M provenance, N g_C only, O 046J boundary preserved, P no reintegration, Q no hidden loss sink (note references 046J), R retention gap → PARTIAL (status AVAILABLE, audit PARTIAL), S never fabricated from reserve+available, T no active storage fields.

## 11. Files created / modified
Created:
- simulation/core/physiology/post_allocation_state.py (contract + pure function)
- simulation/core/physiology/fixtures_046p_g.py (A-E fixtures)
- tests/simulation/test_task046p_g_quick.py (20 assertions)
- TASK_046P_G_PASSIVE_RESERVE_CONTRACT.md (this report)
Unchanged (preserved per rules): simulation/core/carbon/pool.py (046G), source_sink_allocation.py (046I), carbon/input/forecast/physiology contracts (020/021/046G/046I/046J). No mutation of CarbonPool / SourceSinkAllocationResult.

## 12. Exact assertions passed
A–T all pass (see test file and run above). PYTEST_UNAVAILABLE reported honestly (pytest binary unavailable in this environment; assertions executed directly with Python and exit 0).

## 13. pytest status
Direct python execution: pass (20/20). pytest not available in environment; not claimed as pytest pass.

## 14. Limitations / PARTIAL reasons
- 046J retention boundary: executable does not fully define allocated→structural difference when retention < 1. No silent destination invented; transition marked PARTIAL rather than claiming complete end-to-end conservation.
- MODEL A only: no active storage (capacity, remobilization, starch, phloem, priority, stress-regulated mobilization, organ-specific storage, distance-dependent transport). Those are explicit future-layer non-goals.
- No empirical calibration / validation data used (synthetic fixtures only, per CLAUDE.md: never fabricate scientific values; synthetic labeled).
- No mutation of observation/sim time / clock / development age.

## 15. Explicit non-goals / future active-storage layer
NOT implemented (deliberately excluded): storage capacity, storage sink strength, remobilization kinetics, organ-specific storage, starch dynamics, NSC composition, phloem transport, distance-dependent carbon transport, priority storage, stress-regulated reserve mobilization, active remobilization to sinks. These require separate contracts and would change the baseline from MODEL A.

Scientific invariant preserved (MODEL A): reserve_(t+1) = unallocated_t (positive source); deficit = max(-avail, 0) (negative); no double reserve count; g_C only; pure function.
