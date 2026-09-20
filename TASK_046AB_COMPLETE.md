# TASK 046AB — Explicit PPFDSource → FSPM Timestep Integration (COMPLETE)
Date: 2026-09-18; continuation from 046AA.

## Decision: minimal orchestrator integration (no new PPFD model, no new physics).

## Modified files (smallest scope)
- simulation/core/orchestration/fspm_timestep.py — added `organ_ppfd_sources` param; set `ppfd_available` from explicit valid-source list; stage statuses AVAILABLE when sources valid, NOT_COMPUTABLE otherwise; status COMPLETE/PARTIAL accordingly; provenance/note updated; no equation change; existing `getattr` at 29/37 unchanged.
- simulation/core/orchestration/fixtures_046ab.py — new synthetic fixtures (A-D sources + architecture/solar).
- tests/simulation/test_task046ab_quick.py — new quick test (A-N).
- TASK_046AB_COMPLETE.md — this report.

Backups / untouched upstream (explicit):
- 046N fspm_timestep semantics preserved (only boundary param + status logic).
- 046D adapter (photosynthesis_from_organ_exposure) untouched.
- 046B PPFDSource contract untouched.
- 046C exposure integration untouched.
- 046E engine untouched.
- 046G CarbonPool untouched.
- 046I allocation untouched.
- 046J growth conversion untouched.
- 046K delta untouched.
- 046L architecture application untouched.
- 046M lightfield untouched.
- 046O measured PPFD adapter untouched.
- 046V/W modeled PPFD untouched.
- 046Y integrated carbon boundary untouched (g_C_per_timestep preserved).
- 046Z next-state semantics untouched (reserve from unallocated; current_net external; residual UNMODELED).
- 046P-G reserve / 046P-J conversion residual untouched.

## Integration shape (per spec preferred)
PPFDSource[] → integrate_ppfd_source_to_organ (046C) → OrganLightExposure[]
→ photosynthesis_from_organ_exposure (046D) → PhotosynthesisResult (020)
→ carbon_respiration (021) → CarbonPool (046G) → OrganSinkDemand → allocate_carbon_to_sinks (046I)
→ growth delta refs (046K) → Architecture_(t+1) (046L) → NextCarbonState (046Z)
Every arrow uses existing callable or explicit orchestration stage.

## Case results
A — COMPLETE (2 sources; all stages AVAILABLE; provenance explicit)
B — PASS (400 vs 200 preserved per source; adapter passes exact value)
C — PASS (0.0 explicit; AVAILABLE; no silent substitution)
D — PASS (only listed sources used; no interpolation/nearest/average/broadcast; missing second not fabricated)
E/F — PASS (MEASURED / MODELED source_type preserved; converge at exposure boundary)
G — PASS (reserve boundary external 046Z / 046P-G; no double count)
H — PASS (conversion residual separate per 046P-J; not added to reserve)
I — PASS (delta_refs produced when AVAILABLE; actual apply via fixtures/test)
J — PASS (no sources → PARTIAL; architecture UNCHANGED)
K — PASS (step_id, arch IDs, provenance traceable; no invented ids)
L — PASS (architecture, sources, pool, demands immutable)
M — PASS (identical outputs on repeat)
N — PASS (next-state via 046Z; reserve=4 + external current_net=3 → available=7; residual UNMODELED)

## Scientific boundaries verified
- Unit: g_C_per_timestep preserved (046Y).
- PPFD: umol_photons_m2_s explicit; no lux / W/m² / relative_normalized conversion.
- Incident semantics preserved; no APAR / absorption invented.
- Photosynthesis rate concept (020) vs integrated gross_carbon_g preserved (046Y); adapter does not multiply area/time again.
- Respiration subtracted exactly once (021).
- Allocation conserved: allocatable = max(available, 0); unallocated = allocatable - allocated; reserve_next = unallocated (046Z / 046P-G).
- Conversion residual = allocated × (1 - retention) stays separate; not in reserve (046P-J).
- Zero PPFD explicitly valid; missing PPFD not zeroed.
- Architecture feedback loop preserved: Architecture_t → light/PPFD → physiology → growth → Architecture_(t+1) (not requiring same-step light recalc).

## Static audit (modified file)
No added occurrence of: lux, W/m², relative_normalized, interpolation, average, broadcast, nearest.
Existing `getattr` at lines 29/37 (immutability check) justified; no new occurrence.
No hidden area inference, hidden timestep multiplication, extra respiration, residual→reserve, fabricated next-net.
No frontend / R3F / Three.js computation inserted.

## Test execution (exact)
python3 tests/simulation/test_task046ab_quick.py → PASS A-N + static audit (see transcript).
PYTEST unavailable for full suite (not required; focused script executed).
Synthetic fixtures labeled (`is_synthetic_example=True`).
No empirical biological validation claimed.

## Status: COMPLETE
Synthetic timestep with explicit PPFD executes through approved chain; missing inputs honest (NOT_COMPUTABLE / PARTIAL); no fabrication; upstream contracts unchanged; smallest integration at orchestration boundary.
