# TASK 046P-B-FIX2 — COMPLETE (2026-09-18)

Status: TASK_046P_B_FIX2_COMPLETE

## STEP 1 — Executable Audit
- `simulation/core/photosynthesis/photosynthesis.py`: `PhotosynthesisResult` fields = `gross_carbon_g,ppfd_input,unit,timestep,status,provenance,note,parameter_version`.
- `unit = Literal["g_C_per_timestep"]`; `gross_carbon_g: float`; method `photosynthesis_rectangular_hyperbola` computes `gross_carbon_g` directly (scaled by timestep).
- `simulation/core/physiology/contracts.py`: `gross_assimilation` = `Optional[float]=None` placeholder only.

## STEP 2 — Dimensional Decision
- Executable quantity = `gross_carbon_g [g_C / timestep]` — already integrated elemental carbon.
- Invalid operation confirmed: `g_C/timestep × area[m²] × time[s]` is wrong.
- Correct chain: TASK 020 integrated carbon → validated boundary → TASK 021.

## STEP 3 — Fix 046P-B
- Adapter (`carbon_input_adapter.py`): direct `photo.gross_carbon_g → float(rate) → carbon_respiration`; no integration call; no area/time reference.
- Integration (`photosynthesis_integration.py`): preserved as future rate-contract; guard rejects input with `unit="g_C_per_timestep"` or `gross_carbon_g>0` + no `ppfd_input`; does not apply to current path.
- No `getattr` alias; no fallback; direct access only.

## STEP 4 — Current Path
- Pass-through: `photo.gross_carbon_g` (verified 0.00432396 g_C) → `CarbonResult.gross_carbon_g` → `carbon_respiration`.
- Area (`organ_photosynthetic_area_m2`) and time (`elapsed_seconds`) NOT required or used.

## STEP 5 — No Fabricated Rate
- No `gross_assimilation` value created from `gross_carbon_g`.
- `PHOTOSYNTHETIC_RATE_EXECUTABLE=UNAVAILABLE` for current executable; documented.
- Future rate-integration contract kept separate, typed, and gated.

## STEP 6 — Separate Future Rate Integration
- `integrate_photosynthesis_rate_to_carbon` exists but rejects `g_C_per_timestep`; only applies to actual rate inputs; not merged.

## STEP 7 — Area Semantics
- Area NOT required for current pass-through.
- No geometry inference (mesh/Three.js/bounding-box) used.
- Domain geometry independent of visualization per CLAUDE.md.

## STEP 8 — Carbon Semantics
- `carbon_basis = ELEMENTAL_CARBON`; `unit = g_C_per_timestep`; output `gross_carbon_g_C` distinct from input.
- No `g_CO2`; no `g_DM` conversion (046J unchanged).

## STEP 9 — TASK 021
- Unchanged; receives `gross_carbon_g` (g_C/timestep) directly; compatible.

## STEP 10 — Respiration
- Single `carbon_respiration` call; no double subtraction/integration.

## STEP 11 — Fixture
- `gross_carbon_g = 0.00432396`; verified from executable semantics; no multiplication.

## STEP 12 — Tests (18 assertions)
- A canonical executable field; B unit; C pass-through; D no alias; E rejects g_C; F preserved; G separate contract; H provenance; I immutability; J determinism; K 020 unchanged; L 021 unchanged; M 046J unchanged; N area not required; O timestep from executable; P single respiration; Q synthetic verified; R output distinct.
- `PYTEST_UNAVAILABLE`; manual assertions.

## STEP 13 — Static Audit
- `gross_carbon_g_C` vs `gross_carbon_g` distinct; zero alias `getattr`; integration multiplies area only when rate input passes guard; adapter never multiplies.

## STEP 14 — Execution
- `python3 tests/simulation/test_task046p_quick.py`: 18 PASS.

## STEP 15 — Report
- `TASK_046P_B_FIX2_COMPLETE.md` documents all limitations honestly.

## Limitations (explicit)
- No executable `µmol CO₂ m⁻² s⁻¹` rate exists currently; only integrated `g_C_per_timestep` output.
- No empirical biological calibration performed (synthetic fixtures only).
- No area/time required on current path; future rate integration not activated.

Co-Authored-By: Claude Code <noreply@anthropic.com>
