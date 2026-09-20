# TASK 046P-L — NSC / Carbon Storage Feasibility & Contract Decision
Status: TASK_046P_L_C — KEEP_PASSIVE_RESERVE (current maturity does not justify explicit NSC/storage model; conversion residual remains separate and unmodeled; future NSC contract possible when measurements + calibration support it).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; executable source = truth.

## 1. Executive verdict (C)
Keep passive reserve (MODEL L-D). Do NOT implement NSC/storage (L-A/L-B/L-C). Current repository lacks: measurement contracts for NSC/starch/sugar; calibrated storage parameters; validation dataset for storage; identifiable separation of storage synthesis/remobilization from sink demand/photosynthesis/retention; snapshot/state contracts include no NSC field; water/nutrient interfaces exist but have no storage coupling. Conversion residual (046P-J) remains separate from reserve (046P-G) and from NSC. Implementation policy: report only; no new storage pool, sink, capacity, remobilization, or conversion-residual→NSC mapping.

## 2. Research basis (supplied)
FSPM distinguishes source, allocation, structural, reserve/NSC, respiration, other fluxes; NSC/reserve may be explicit sink when relevant; storage parameters need calibration; high-resolution temporal data may be unavailable; structural biomass and NSC distinct; residual must not become NSC automatically. Used for framing only.

## 3. Current carbon architecture (verified, unchanged)
- 046G: CarbonPool (reserve + net = available; sign preserved; no automatic reserve-next)
- 046I: Source–Sink Allocation (allocatable = max(available,0); conservation 1e-6; pool immutable)
- 046P-G: reserve_next = unallocated_carbon_g (MODEL A; no conversion-residual added)
- 046J: structural = allocated × retention; biomass = structural / carbon_fraction
- 046P-J: ConversionResidualContract (UNMODELED; STORAGE/LOSS gated; RESPIRATION excluded)
- 021: respiration = gross × rate; upstream of pool
Two distinct branches preserved: allocation surplus → reserve (046P-G); growth conversion residual → unmodeled (046P-J).

## 4. Existing storage / reserve interfaces (audited, no inference)
Search results (real files): water/contracts.py, water/balance.py, water/fixtures.py, carbon_pool_adapter.py, fixtures_046p_d, fixtures_046g, fixtures_046j, post_allocation_state.py, conversion_residual_contract.py, scheduler, snapshot/fixtures, calibration/contracts, validation/contracts, scenario/contracts, water/uptake, root/nutrient contracts.
No file defines NSC/starch/sugar/storage_capacity/storage_sink/remobilization/state-transition for carbon. Only references are conceptual (conversion_residual_contract note mentions future STORAGE; 046P-H notes 046J retention gap; 046P-I notes contract ambiguity). No implementation.

## 5. Measurement / observation observability (explicit — none for NSC)
Directories `simulation/core/measurement/` and `simulation/core/observation/` do not exist.
Existing contracts (calibration, validation, scenario, snapshot, water) are synthetic/general; none define NSC/starch/sugar measurement protocol, sampling method, temporal resolution, or organ-level storage observation.
Digital-twin observations available conceptually (biomass, PPFD, light, water, geometry, destructive biomass) — none distinguish NSC from structural carbon.
Conclusion: observability INSUFFICIENT for explicit NSC model calibration.

## 6. Parameter identifiability (explicit — confounded)
Parameters that would need separate identification:
- storage synthesis rate (from what? allocation surplus? conversion residual? external input?)
- storage capacity / bound
- remobilization rate (to sinks? to structural growth?)
- retention (already synthetic/un calibrated; confounded with sink demand and photosynthetic source)
With current data (no NSC measurement, no labeled carbon tracing, no time-series storage), retention + sink demand + photosynthesis are confounded; storage parameters unidentifiable.
Consequence: L-A/L-B/L-C would add unidentifiable degrees of freedom.

## 7. Model L-A (Single passive NSC pool) analysis
Requires: NSC_t state; storage_input; remobilization_output; new contracts; calibration; validation dataset; snapshot/state persistence support.
Not supported: no NSC contracts; no calibration dataset; no observation protocol; conversion residual not mapped (and must remain separate per 046P-J/046P-G).
Verdict: NOT READY.

## 8. Model L-B (Active storage sink) analysis
Requires: storage sink demand competing with organ sinks; storage capacity; storage synthesis; remobilization; explicit coupling to sink allocation (046I). Would require modifying source–sink allocation to include storage as competitor — major contract change.
Not supported: no storage contract; no calibration; no measurement; reserve (046P-G) is separate and different mechanism (passive surplus, not active sink).
Verdict: NOT READY.

## 9. Model L-C (Two-state active/stored NSC) analysis
Requires: active/stored split; exchange dynamics; capacity; remobilization; calibration of both states.
Not supported: no contracts; highest complexity; lowest identifiability with current observations.
Verdict: NOT READY.

## 10. Model L-D (Keep passive reserve + unmodeled residual) analysis
Current: reserve_next = unallocated (046P-G); conversion_residual = unmodeled (046P-J); retention = structural conversion fraction (046J synthetic); respiration upstream (021); no storage.
Supported by: all existing contracts; all fixtures/tests; all validations; no new parameters; no calibration required; conversion residual explicit but unmodeled (correct per 046P-I/046P-K); reserve and residual distinct; g_C/g_DM boundary clean.
Verdict: CURRENT BASELINE; correct until measurement/calibration supports L-A/B/C.

## 11. Conversion residual relationship (preserved, not changed)
Per 046P-J/046P-H/046P-K: conversion_residual_g_C = allocated × (1 − retention) = UNMODELED. Must NOT become NSC automatically. No mapping from 046J residual to storage state without explicit future contract. Reserve (046P-G) remains unallocated-only. Scientific invariant preserved.

## 12. Passive reserve relationship (preserved)
046P-G: reserve_next = unallocated_carbon_g (MODEL A). NSC/storage is conceptually separate from passive reserve: reserve = allocation surplus (car never committed to organ); NSC = carbon committed to organ structure/store that did not become structural. Do NOT merge. If future L-A/B implemented, must define whether NSC is separate pool or replaces/extends reserve — not assumed now.

## 13. Water / nutrient coupling readiness (future, not now)
Water contracts (simulation/core/water/) and root/nutrient contracts exist. Storage could respond to drought/irrigation/nutrient limitation in future, but no storage-coupling equation exists. Mapping is possible conceptually (e.g., drought → reduced synthesis / increased remobilization) but requires explicit contract not present. Do not invent coupling.

## 14. Digital twin implications
Real garden measurements: biomass, geometry, light, water, possible destructive sampling. NSC would require destructive sampling or high-frequency non-destructive proxy (none defined). Scenario/branching (scenario/contracts) can branch predictions but lacks NSC state to branch from. Calibration framework (calibration/contracts) is scalar/synthetic; no storage parameter versioning. Validation (validation/contracts, evaluation.py) compares by metric — no NSC metric defined. Temporal resolution for storage dynamics unverified. Recommendation: digital twin should remain at current complexity (L-D) until measurement protocols and calibration datasets for storage exist.

## 15. Final decision (C)
C — KEEP_PASSIVE_RESERVE (MODEL L-D).
Explicit NSC/storage model (L-A/B/L-C) is scientifically plausible but not supported by executable contracts, measurements, identifiability, or calibration framework. Conversion residual remains separate and unmodeled. Passive reserve (036P-G) unchanged. No implementation.

## 16. Required future contract (explicit, not invented)
To move from L-D to L-A/B/C when measurements support:
1. Measurement protocol contract (NSC/starch/sugar observation method, temporal resolution, organ-level, destructive/non-destructive).
2. Calibration dataset contract (explicit storage measurements linked to simulation runs; not validation data; separate from calibration of retention/sink demand).
3. Storage-state contract (NSC_t / active_t / stored_t; synthesis; remobilization; capacity bounds; provenance).
4. Storage-transition / remobilization contract (when/where to synthesize, when to remobilize; coupling to sink demand, growth, water, nutrient — only where existing interfaces allow).
5. Conversion-residual→storage mapping contract (only if conversion residual is designed to enter storage — currently NOT; must be explicit; do NOT silently merge into reserve_next).
6. Validation metric contract (storage prediction vs observation; MAE/RMSE relative to storage measurements).
Not all required at once; start from measurement + calibration dataset before state model.

## 17. Files inspected (read, unchanged)
- simulation/core/carbon/pool.py, carbon/carbon.py
- simulation/core/allocation/source_sink_allocation.py, source_sink_result_contract.py
- simulation/core/growth/*.py (046J contracts/derivation/params/fixtures)
- simulation/core/physiology/post_allocation_state.py, conversion_residual_contract.py, fixtures_046p_j.py
- simulation/core/clock/clock.py, scheduler/scheduler.py (time separate from biology)
- simulation/core/calibration/*, validation/*, scenario/*, snapshot/*
- simulation/core/water/*, root/nutrient contracts
- tests/simulation/test_task046p_*.py (verified references intact)
No upstream modification.

## 18. Files changed
None. Only report created.

## 19. Tests / audits
Reused 046P-J assertions (A-T) to confirm: reserve unchanged, conversion residual separate, units g_C, no mutation, determinism, provenance, gating. No new tests needed for audit-only decision (decision validated by absence of contracts, not by new execution).

## 20. pytest status
PYTEST_UNAVAILABLE reported honestly; no false claims; audit verified by direct inspection of files and existing assertions.

## 21. Limitations
- Decision is based on repository contract absence, not on biological impossibility. NSC is real; model is not ready.
- Conversion residual remains unmodeled; not mapped to storage; reserve remains passive surplus.
- No calibration dataset exists for storage; identifiability not demonstrated; measurement protocols not defined.
- Digital twin requirements not fully satisfied for mechanistic storage; continue with L-D until evidence supports L-A/B/C.
