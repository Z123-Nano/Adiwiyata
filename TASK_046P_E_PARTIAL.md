# TASK 046P-E — PARTIAL (2026-09-18)

Status: TASK_046P_E_PARTIAL — reserve carryover / post-allocation state-transition contract missing in executable repository.

## STEP 0 — Executable Audit
- 046G pool.py: reserve/current_net/available invariant; pool unchanged by 046I.
- 046I allocation.py (allocate_carbon_to_sinks): uses available_carbon_g directly; allocatable=max(source_available,0); negative -> status AVAILABLE (note negative_or_zero_source); allocations empty; unallocated computed; pool unchanged.
- 046J spec: g_C -> g_DM; no reserve/state update defined.

## STEP 1 — Ledger (verified)
reserve_carbon_g + current_net_carbon_g = available_carbon_g (046G)
After 046I: allocated + unallocated = allocatable (conservation, 1e-6)
After 046J: allocated -> structural biomass (no executable reserve update)

## STEP 2 / 3 — Conservation
- 046G invariant verified.
- 046I conservation verified at boundary.
- No second balance exists.

## STEP 4 — 046J Boundary
- allocated_g_C -> realized structural carbon / g_DM.
- No executable contract for retention loss, remobilization, or reserve update.

## STEP 5 — Reserve Carryover (critical finding — BLOCKED)
- Executable repo has NO contract defining reserve_next = f(unallocated, growth_loss, remobilization).
- 046G defines reserve_carbon_g as INPUT (prior timestep carry-over), not computed output.
- 046I reports unallocated_carbon_g but does not transition pool state.
- 046J does not specify reserve update.
- Options compared (A passive, B storage sink, C current transient / executable-supported); only C matches repo.
- Decision: do NOT invent reserve_next; no adapter mutation; mark PARTIAL.

## STEP 6 — Timing
- No clock change; same-step (net -> allocation -> growth) per existing design; observation/time/development distinct.

## STEP 7 — Models Compared (documented only)
- A/B require new contracts; C matches executable.

## STEP 8 — No Implementation
- Only audit/verification tests performed (tests/test_task046p_e_quick.py).
- No reserve_next adapter, no pool mutation, no storage contract.

## STEP 9 — Tests (20 assertions; exit 0; PYTEST_UNAVAILABLE)
- A–D: sufficient / limited / negative / not clamped
- E: zero demand
- F: full allocation
- G: surplus preserved (not reserve)
- H: reserve not double-counted
- I: pool unchanged
- J: determinism
- K: timestep identity
- L: 046J unchanged
- M: g_C/g_DM boundary preserved
- N: no fabricated reserve_next
- O: conservation at boundary
- P: source identity
- Q: provenance
- R: negative source -> no positive allocation (executable)
- S: unallocated stays in pool (no mutation)
- T: no second balance

## STEP 10 — Scientific Invariants
- g_C preserved; no g_DM conversion; no hidden sink/source; no silent mutation; no fabricated IDs; deterministic; immutable.

## STEP 11 — Report
- This file: TASK_046P_E_PARTIAL.md.

## Limitations / Gap
- Reserve carryover contract missing. Implementation blocked until explicit storage/state-transition contract is defined (Model A/B) or repository accepts transient-pool semantics (Model C) with documented next-step rules.
- No empirical calibration (synthetic fixtures only).
- PYTEST_UNAVAILABLE.

## Confirmed Unchanged
- TASK_046G (pool.py) unchanged.
- TASK_046I (allocation.py) unchanged.
- TASK_046J (growth conversion boundary) unchanged.
- No upstream/downstream scientific contracts modified.

Co-Authored-By: Claude Code <noreply@anthropic.com>

## FIX2 — Audit verification repaired (post-step-1 failure on identity assertion)
- Actual failure reproduced: identity assertion referenced wrong literal ("pool_A" vs fixture "pool_E_A"); corrected to `assert res_A.carbon_pool_id == pool_A.pool_id` (fixture source, no literal duplication, no getattr).
- Adapter audit: removed `getattr`/`hasattr` fallback from `carbon_pool_allocation_adapter.py`; direct `float(carbon_pool.available_carbon_g)`; explicit `ValueError` on None/invalid pool.
- Fixtures `fixtures_046p_d.py` validated with required `OrganSinkDemand` fields (`sink_parameter_set_ref`, `sink_coefficient_ref`, `structural_proxy_value`).
- Test exits 0; 20 assertions pass; `PYTEST_UNAVAILABLE`; static audit clean (no alias, no g_DM/umol/PPFD/area*time, no reserve double-count).
- Status remains `TASK_046P_E_PARTIAL`: reserve carryover contract still missing; no storage/reserve transition implemented; 046G/046I/046J unchanged.
