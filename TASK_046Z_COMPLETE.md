# TASK 046Z — Carbon Ledger State Transition (COMPLETE — Decision B)
Status: COMPLETE (new pure NextCarbonState contract; existing 046P-G + 046P-J sufficient; no upstream edits).

## Decision
B — NEW PURE NEXT-STATE CONTRACT (`simulation/core/carbon/next_state.py`) required because `PostAllocationCarbonState` carries reserve but no explicit combined next-state with external current_net. Contract defines only state transition; no storage/NSC physics invented.

## Boundary / equations
- `reserved_next = unallocated_t` (positive source; MODEL A from 046P-G)
- `reserve_next = 0` (non-positive source); `deficit = max(-available, 0)`
- `available_(t+1) = reserve_(t+1) + current_net_(t+1)` — current_net external, not fabricated
- `conversion_residual` remains `UNMODELED`; NOT added to reserve (G verified)
- Units: `g_C`; timestep explicit; identity preserved

## Critical distinctions preserved
- Reserve from surplus ONLY; residual UNMODELED (E, G verified)
- No fabrication of next-timestep photosynthesis / respiration / net carbon
- No NSC / starch / remobilization / transport / maintenance respiration changes
- Pure / immutable / deterministic (J, K verified)
- Provenance / source_ids / identity preserved (H, I)

## Tests
A-L pass (surplus/exact/limited/zero/negative/residual/not-reserve/identity/provenance/immutability/deterministic/no-hidden-storage).
PYTEST_UNAVAILABLE (direct python3 assertions).

## Files
New: `simulation/core/carbon/next_state.py`, `simulation/core/carbon/fixtures_046z.py`, `tests/simulation/test_task046z_quick.py`, `TASK_046Z_COMPLETE.md`.
Upstream untouched: 046G pool, 046I allocation, 046J growth, 046P-G reserve, 046P-J residual.
