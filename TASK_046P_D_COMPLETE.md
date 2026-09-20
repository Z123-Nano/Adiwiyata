# TASK 046P-D — COMPLETE (2026-09-18)

Status: TASK_046P_D_COMPLETE

## STEP 0 — Executable Audit
- 046G CarbonPool (`pool.py`): `available_carbon_g = reserve + current_net`; sign preserved; no clamp; `source_carbon_result_id`, `previous_pool_id`, identity fields; invariant checked; no allocation/growth fields.
- 046I `allocate_carbon_to_sinks` (`allocation.py`): takes `CarbonPool` + `List[OrganSinkDemand]`; uses `available_carbon_g` directly (`line 53`); `allocatable = max(source_available, 0.0)` (`line 54`); negative source → `NOT_COMPUTABLE`? Actually status AVAILABLE with note negative_or_zero_source (line 149); allocations empty; no mutation (`line 194` note).
- 046I demand: uses `potential_demand_g`; rejects negative; distinguishes None vs [].

## STEP 1 — Field feeding allocation
- `CarbonPool.available_carbon_g` is the exact resource field (already integrated reserve+net per 046G contract).

## STEP 2 — 046I Semantics
- Expects `source_available_g = float(available_carbon_g)`; proportional; conservation 1e-6; deficit explicit; negative source preserved as non-positive allocatable.

## STEP 3 — Reserve semantics
- Adapter uses `available_carbon_g` directly; does NOT recompute `reserve + net`; does NOT add reserve twice; reserve is embedded in available by 046G design.

## STEP 4 — Negative carbon
- 046G allows negative `available_carbon_g`; 046I handles via `max(...,0.0)` for allocatable; adapter passes through unchanged.

## STEP 5 — Unit
- g_C throughout; `available_carbon_g`, `allocated_carbon_g`, `deficit_g` all g_C; no g_DM; 046J separate.

## STEP 6 — Identity
- Pool `plant_id`, `architecture_id`, `pool_id` preserved by 046I; adapter passes through; no fabricated IDs.

## Implementation
- Adapter: `simulation/core/physiology/carbon_pool_allocation_adapter.py` — thin wrapper around `allocate_carbon_to_sinks`; pure; no mutation; provenance preserved.
- Fixtures: `fixtures_046p_d.py` (A–E cases: sufficient/limited/zero/negative/zero-demand).
- Tests: `test_task046p_d_quick.py` — 19 assertions (A–S) pass; PYTEST_UNAVAILABLE.

## No changes to upstream/downstream contracts
- 020, 021, 046G, 046J, LightField, API, frontend unchanged.
- 046I unchanged (used directly).

## Limitations (explicit)
- No empirical calibration (synthetic fixtures only).
- No stochasticity / optimization / engine integration.
- Adapter is verification wrapper; future extensions (priority policy, custom) remain in 046I contract.

Co-Authored-By: Claude Code <noreply@anthropic.com>


## FIX2 updates (post-audit)
- Adapter cleaned: removed provenance_suffix dead API; explicit ValueError on None/invalid pool (no getattr/hasattr); direct float(carbon_pool.available_carbon_g).
- Fixtures verified with sink_parameter_set_ref / sink_coefficient_ref.
- Static audit: zero getattr/hasattr in code; zero unrelated scientific conversions.
- Re-verified: 19 assertions pass; PYTEST_UNAVAILABLE; exit 0.
- Canonical 046I = simulation/core/allocation/source_sink_allocation.py (allocate_carbon_to_sinks).
