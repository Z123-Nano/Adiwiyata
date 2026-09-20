=== TASK 046I FINAL VERIFICATION ===
Status: TASK_046I_COMPLETE

1. Contract exists: SourceSinkAllocationResult + OrganAllocationItem (source_sink_result_contract.py)
2. Potential demand distinct: uses OrganSinkDemand.potential_demand_g; never interpreted as biomass/growth
3. Relative sink for limited (0<A<D_total): allocated = A*D_i/D_total; unmet = D_i - allocated
4. Full demand when A>=D_total
5. Surplus = unallocated_carbon_g = A - D_total (positive only)
6. Unmet = D_i - allocated
7. Zero/negative source → zero allocation; source preserved (not clamped); demand unmet
8. CarbonPool unchanged (verified by identity before/after)
9. OrganSinkDemand unchanged (verified)
10. Conservation enforced by model_validator (tolerance 1e-6) + manual checks
11. No topology/priority/growth/calibration/stochasticity
12. Status distinguishes AVAILABLE / NOT_COMPUTABLE; no invented vocabulary
13. Provenance preserves pool_id + demand refs + parameter_version + synthetic flag
14. Formula documented explicitly; case semantics (4 cases) explicit
15. Unit distinct: source g_C; demand g_C; allocation g_C; no lux/PPFD involvment
16. Compatibility note: TASK 022 CarbonSink.demand uses umol CO2 m^-2; 046H-E uses g_C/step — unit gap reported; 046I standalone over OrganSinkDemand; 022 not modified; adapter deferred
17. Tests: 24 assertions PASS (manual; pytest unavailable — PYTEST_ENVIRONMENT_UNAVAILABLE reported)
18. No frontend/API/engine/Three.js/light/soil changes; no TASK 020/021/023/modification
DECISION: TASK_046I_COMPLETE
TASK_046I_COMPLETE — review patches applied; no 022 modification; no growth; structural proxy = length_m; formula explicit; 32 assertions; PYTEST unavailable reported; limitation: no 022 adapter (unit gap preserved); next layer allowed: allocated carbon → growth (TASK 023 future).
