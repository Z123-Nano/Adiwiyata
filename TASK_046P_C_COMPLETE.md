# TASK 046P-C — COMPLETE (2026-09-18)

Status: TASK_046P_C_COMPLETE

## STEP 0 — Executable Audit
- TASK 021 `carbon_respiration` (`simulation/core/carbon/carbon.py`): returns `CarbonResult(gross_carbon_g, respiration_g, net_carbon_g, timestep, status, provenance, note, parameter_version)`; `net = gross - respiration`; negative permitted.
- TASK 046G `CarbonPool` (`simulation/core/carbon/pool.py`): `reserve_carbon_g + current_net_carbon_g = available_carbon_g`; invariant checked; sign preserved; no clamping; `source_carbon_result_id`, `previous_pool_id`; no allocation/growth fields.

## STEP 1 — TASK 021 Semantics Verified
- Net = gross − respiration; identity preserved; units g_C/timestep.

## STEP 2 — CarbonPool Semantics Verified
- `available = reserve + current_net`; negative allowed; reserve is explicit carry-over; no automatic reserve-next.

## STEP 3 — Integration Input
- Adapter `carbon_pool_adapter.py`: takes `CarbonResult` + explicit `reserve_carbon_g` + identity + provenance.

## STEP 4 — No Invented Carryover
- Reserve explicitly passed; not derived from previous pool.

## STEP 5 — Build Function
- `build_carbon_pool_from_balance`: pure; validates `AVAILABLE`; takes `net`; calculates `available`; uses `carbon_pool_from_reserve_and_net`.

## STEP 6 — Numerical Semantics
- Positive/negative/zero net preserved; `available = reserve + net`; no clamp.

## STEP 7 — Zero Cases
- Valid; no substitution.

## STEP 8 — Negative Cases
- `reserve=1.0, net=-0.4 → available=0.6`; `reserve=0, net=-0.4 → available=-0.4`; preserved.

## STEP 9 — Source Lineage
- `source_carbon_result_id` passed (None when CarbonResult lacks result_id — no fabrication).
- `previous_pool_id` optional; never fabricated.

## STEP 10 — Identity
- `plant_id` required; `architecture_id` optional; consistent.

## STEP 11 — Timestep
- Preserved from TASK 021; no second integration.

## STEP 12 — No Allocation
- Adapter does not call 046I; no organ/sink calculations.

## STEP 13 — No g_C → g_DM
- Adapter outputs `g_C`; 046J unchanged.

## STEP 14 — Provenance
- Records TASK 021 source, reserve, net, available, timestep, simulation_time.

## STEP 15 — Fixture
- Synthetic: gross=1.20, resp=0.30, net=0.90, reserve=0.40, available=1.30; negative net case.

## STEP 16 — Tests (22 assertions)
- A–T pass; PYTEST_UNAVAILABLE reported.

## STEP 17 — Static Audit
- `available_carbon_g` / `current_net_carbon_g` / `gross_carbon_g` distinct; no unit change; adapter uses direct fields.

## STEP 18 — Execution
- `python3 tests/simulation/test_task046p_c_quick.py`: 22 PASS.

## STEP 19 — Report
- This file.

## Scope Restrictions Respected
- 020, 021, 046G, 046I, 046J, LightField, API, frontend unchanged.
- Only new adapter/fixture/test/report added.

## Limitations (explicit)
- No empirical biological calibration (synthetic fixtures).
- `CarbonResult` has no `result_id`; adapter passes `None` correctly; future contract may add id.
- No rate-integration (046P-B-FIX2 separate) applied here.

Co-Authored-By: Claude Code <noreply@anthropic.com>
