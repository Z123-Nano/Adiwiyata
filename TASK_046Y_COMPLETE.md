# TASK 046Y — Photosynthesis Carbon Quantity & Temporal Integration Audit (COMPLETE — Decision A)
Status: COMPLETE (audit only; no code changes required; upstream untouched; all assertions A-L pass; PYTEST_UNAVAILABLE honest).
Decision: A — GROSS_CARBON_ALREADY_INTEGRATED.

## Executive verdict
Executable evidence from `simulation/core/photosynthesis/photosynthesis.py` (TASK 020 canonical), `simulation/core/physiology/photosynthesis_input_adapter.py` (046D), `simulation/core/physiology/carbon_input_adapter.py` (046F), and `simulation/core/physiology/photosynthesis_integration.py` (046P-B-FIX2) proves `PhotosynthesisResult.gross_carbon_g` is already `g_C_per_timestep` (unit literal, timestep-scaled by `t/3600`). The 046D adapter passes it directly; 046F passes it directly to TASK 021 (`carbon_respiration`); 046P-B-FIX2 explicitly rejects rate-integration when `gross_carbon_g` is present. No additional `area × dt` integration is permitted or needed at this boundary.

## Source-of-truth executable evidence
- 020 (`photosynthesis.py`): `PhotosynthesisResult.unit = "g_C_per_timestep"`; `timestep=3600.0`; equation `gross = (alpha * ppfd * pmax) / (alpha * ppfd + pmax) * (timestep/3600.0)`. Parameters `alpha` (g C / mmol PPFD / timestep baseline), `pmax` (g C / timestep). Rate is NOT produced; integrated carbon is.
- 046D adapter: passes `exposure.ppfd_value` → `photosynthesis_rectangular_hyperbola` → copies `gross_carbon_g`; contains no `area`, `elapsed_seconds`, or `timestep` multiplication for carbon.
- 046P-B-FIX2 (`photosynthesis_integration.py`): first guard rejects if `unit == "g_C_per_timestep"` or `gross_carbon_g > 0` with `ppfd_input` missing → `NOT_COMPUTABLE` with note "already integrated".
- 046F adapter (`carbon_input_adapter.py`): "PASS-THROUGH ... no area/time integration"; passes `gross_carbon_g` to `carbon_respiration`.
- 021 (`carbon/carbon.py` `carbon_respiration`): receives `gross_carbon_g` as `g_C` per timestep; applies respiration once (`respiration_rate`); net = gross - respiration.

## Equation / unit table
| Quantity | Executable source | Unit | Time basis | Notes |
|---|---|---|---|---|
| PPFD input | `PPFDInput.ppfd` (046D) | µmol photons m⁻² s⁻¹ | instantaneous | Incident only |
| Photosynthesis rate (conceptual) | 020 hyperbola | µmol CO₂ m⁻² s⁻¹ | instantaneous | Not produced by 020; 020 produces integrated carbon |
| `gross_carbon_g` (020 output) | `PhotosynthesisResult.gross_carbon_g` | g_C_per_timestep | timestep (default 3600 s) | Already scaled by `t/3600`; synthetic params |
| 046P-B integration (when rate) | `integrate_photosynthesis_rate_to_carbon` | g_C | `elapsed_seconds` × area | Blocked when input already integrated |
| 046F → 021 | `carbon_from_photosynthesis` | g_C_per_timestep | `timestep` preserved | Pass-through; respiration subtracted once |
| Net carbon | `CarbonResult.net_carbon_g` | g_C_per_timestep | same timestep | Gross - respiration; no second subtraction |

## Dimensional audit (key)
- If `gross_carbon_g = 12.5` (g_C/3600s) were mistakenly treated as rate: `12.5 × 0.05 m² × 3600 s = 2250` (wrong by factor ~180). Executable output stays 12.5; 046P-B-FIX2 blocks the error.
- Carbon molar mass `12.011` used only in 046P-B rate-integration path (not here because already integrated).
- No `g_C` → `µmol CO₂` conversion needed at boundary because 020 output is already carbon mass.

## Boundary correctness
- `gross_carbon_g` → 021: direct; no `area`; no `dt` reintegration; respiration exactly once.
- Organ identity preserved through 046D/046F via `exposure_ref`.
- Source type preserved (`DERIVED_PHYSICALLY_VALID` / `MEASURED` / `SYNTHETIC`).
- Synthetic fixtures labeled; not empirical calibration.

## Zero / invalid
- Zero `gross_carbon_g` valid → `net_carbon_g = 0 - respiration`; executable handles.
- Negative/non-finite blocked upstream (PPFDSource validators + 020 input guard).

## Static audit (step 17 equivalent)
- No `getattr`/`hasattr` fallback; no `LightField`; no `interpolation`; no `nearest`; no `average`; no `broadcast`; no `area` inference in 046D/046F; no `lux`; no `W/m²`; no `µmol/J`; no `g_DM`; no `absorbed`/`APAR`; no double respiration (021 applies once; 020 has none).

## Test results
- Fixtures: `fixtures_046y.py` (synthetic integrated results A/B/C with known values and timesteps)
- Assertions: `test_task046y_quick.py` — A-L pass (unit, adapter pass-through, 046P-B-FIX2 block, 021 direct receipt, dimensional proof F, determinism I, exact value J, provenance H, zero C, identity preserved)
- PYTEST_UNAVAILABLE honest (direct `python3` assertions)

## Files changed
New audit-only: `fixtures_046y.py`, `test_task046y_quick.py`, `TASK_046Y_COMPLETE.md`. Zero upstream modifications (020/021/046D/046E/046F/046G untouched).

## Limitations / next
- 020 params synthetic / uncalibrated (`PARAM_PROVENANCE` explicit); not species-specific.
- `gross_carbon_g` is per-timestep; multi-timestep aggregation (e.g., daily carbon) requires explicit temporal summation outside this boundary.
- No optical/absorption model needed (incident PPFD boundary verified by 046X).
