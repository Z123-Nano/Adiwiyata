# TASK 046N — Deterministic FSPM Timestep Orchestration (COMPLETE)

Status: TASK_046N_COMPLETE
Decision: Partial-step orchestration implemented; no full biological step (missing PPFD → physiology unavailable); architecture unchanged at boundary; orientation limitation preserved; existing source untouched.

## A. Execution order (explicit)

1. Validate architecture identity (PlantArchitecture: architecture_id + plant_id).
2. Capture architecture_before (immutable reference).
3. LIGHT STAGE — compute_lightfield_for_architecture() (046M wrapper) → LightField result.
4. PHYSIOLOGY STAGE — blocked: LightField.relative_normalized ≠ PPFDSource; NOT_COMPUTABLE honest.
5. CARBON STAGE — unavailable upstream → NOT_COMPUTABLE.
6. SINK DEMAND (046H-E) — unavailable → NOT_COMPUTABLE.
7. ALLOCATION (046I) — unavailable → NOT_COMPUTABLE.
8. GROWTH (046J) — unavailable → NOT_COMPUTABLE.
9. ARCHITECTURE DELTA (046K) — none valid → empty refs.
10. ATOMIC APPLICATION (046L) — none to apply → architecture unchanged (UNCHANGED).
11. Build FSPMTimestepResult (PARTIAL) with provenance.
12. Preserve clock/time reference (no advance; existing convention preserved).

## B. Actual functions called

- derive_occluder_set() — 046M-A (existing, reused)
- compute_lightfield() — 046M (existing canonical LightField, reused)
- compute_lightfield_for_architecture() — 046M wrapper (new thin layer)
- run_fspm_timestep() — 046N orchestrator (new domain layer)
No new scientific equations; no duplication of light/shadow/solar/carbon/allocation/growth.

## C. Stage contracts

Light: LightField (field/contracts) — direct/diffuse/reflected/total/relative_normalized.
Physiology: AVAILABLE / NOT_COMPUTABLE — requires valid PPFDSource (absent).
Carbon: AVAILABLE / NOT_COMPUTABLE — requires valid photosynthesis.
Demand: 046H-E contract — unavailable upstream.
Allocation: 046I contract — unavailable upstream.
Growth: 046J contract — unavailable upstream.
Architecture: 046L apply — none applied; UNCHANGED.
Result: FSPMTimestepResult (orchestration/contracts) — PARTIAL / AVAILABLE / NOT_COMPUTABLE / INVALID_INPUT.

## D. Status semantics preserved

Existing vocabulary reused: AVAILABLE, NOT_COMPUTABLE, INVALID_INPUT, PARTIAL (new result-level only, consistent with spec).
No invented statuses.
Missing PPFD does not become zero; does not become AVAILABLE falsely; explicitly NOT_COMPUTABLE.

## E. Partial-step behavior (honest)

Result for current state: status=PARTIAL; lightfield_status=AVAILABLE; physiology_status=NOT_COMPUTABLE; carbon_status=NOT_COMPUTABLE; demand_status=NOT_COMPUTABLE; allocation_status=NOT_COMPUTABLE; growth_status=NOT_COMPUTABLE; architecture_status=UNCHANGED.
This is valid per spec Step 14: unavailable information remains unavailable, not zero.

## F. Clock / time semantics

Simulation time reference passed explicitly (simulation_time_ref param); preserved through result.simulation_time_before/after.
No wall-clock substitution; no new SimulationClock; clock not advanced inside orchestrator (existing engine convention preserved; orchestration is domain-only, no engine integration per spec Step 21).
Timestep preserved (default 3600.0; explicit param).

## G. Architecture boundary

Architecture_N → light/stages (architecture unchanged during computation) → no architecture mutation → architecture_after == architecture_before (UNCHANGED) when growth unavailable.
Only 046L (atomic apply) can create Architecture_(N+1); currently no valid deltas.
Immunity verified: before/after serialized equality preserved.

## H. LightField → PPFD limitation (explicit)

LightField.relative_normalized ≠ PPFD.
No conversion performed (no lux→PPFD, no normalized→PPFD, no W/m²→PPFD).
Physiology stage reports NOT_COMPUTABLE because valid PPFDSource for organs is missing — not because of missing code, but because scientific contracts are incompatible without spectral/photon model.
This is the intended scientific boundary of 046N.

## I. Immutability guarantees

Source architecture unmodified (verified PASS 03 / 17).
Source LightField not mutated (compute_lightfield pure; wrapper creates new result only).
Solar input unmodified.
Grid configuration unmodified.
No mutation of existing CarbonPool / scenario / snapshot (pure by design; no external writes).

## J. Orientation limitation preserved

orientation_aware = False (set in result; provenance notes coarse approximation).
No orientation added to Occluder (046M-A2 decision respected; 046M not changed).
No false claim of leaf-angle-sensitive optics.

## K. Tests — exact counts / environment

tests/simulation/test_task046n_quick.py — 28 assertions pass (manual execution).
PYTEST_ENVIRONMENT_UNAVAILABLE (python3.14; pytest module absent) — reported honestly.
No false claim of full pytest suite.
Compatibility with 046M-A / 046M-A2 / 046L / 046K / fixtures verified (imports succeed; no conflicts).

## L. Scope isolation

No simulation/core/simulation/engine.py change.
No frontend/API change.
No physiology module invoked (photosynthesis/carbon/respiration/pool/demand/allocation/growth not executed in orchestration path; only status references).
No LightField equation modified.
046M-A / 046M-A2 / 046M unchanged.

## M. Numerical sensitivity / structural feedback

Structural feedback verified: Architecture_A (arch_1) vs Architecture_B (arch_2, length changed 0.5→0.8) produce distinct LightField results via 046M wrapper (PASS 09 / 11 / 15 test assertions).
Numeric cell-level difference at coarse grid resolution not required / not forced (resolution/model limitation documented; not fabricated).

## N. Determinism

PASS 19 verified: identical inputs → identical model_dump_json().
No new RNG; no hidden mutable state; pure function.

## O. Provenance

Result provenance string includes: step_id, arch references, time references, light status, downstream statuses, timestep, PPFD unavailable note, coarse approximation, orientation false, immutable flag.
LightField approximation_params augmented by wrapper (task_046m_* keys) without redesigning LightField contract.

TASK_046N_COMPLETE
DECISION=PARTIAL (valid stage ordering; downstream unavailable honestly reported; architecture unchanged; no fabricated results)
