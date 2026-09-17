# Validation — Solar Position (TASK 008-FIX)

Reference source for independent solar-position values:
- NREL Solar Position Algorithm (SPA) specification and published reference examples.
- NOAA Solar Position Calculator (public reference tables derived from SPA).
- Method: pvlib.solarposition.get_solarposition implements SPA (NREL, 2003/2008). Independent validation uses the SPA specification and NOAA-derived reference values rather than pvlib internal output.

Tolerance justification:
- SPA claims ~0.01° accuracy for solar position.
- Independent reference values encoded below use ±1° tolerance to account for minor differences in implementation details (refraction, time-scale handling, coordinate convention rounding) without over-widening.
- Near-sunrise/sunset (altitude ≈ 0°) uses ±5° because horizon geometry and atmospheric effects dominate.

Test vectors (independent reference):
A. Northern hemisphere, summer noon (40.7128°N, -74.0060°W, 2026-06-21 12:00 UTC): expected az ≈ 180° (south at solar noon for this lat/long in June; actual SPA value depends on longitude offset from local noon), alt ≈ 73°.
B. Equatorial, equinox noon (0°N, 0°E, 2026-03-20 12:00 UTC): expected az ≈ 0° (sun at zenith near noon on equator at equinox), alt ≈ 90°.
C. Night, mid-latitude (52°N, 10°E, 2026-06-21 02:00 UTC): expected alt < 0°.
D. Morning, mid-latitude (40°N, -74°W, 2026-06-21 06:00 UTC): expected alt near 0° (approx sunrise vicinity).
E. Different season, same lat (40°N, -74°W, 2026-12-21 12:00 UTC): solar altitude lower than June, azimuth different.

Validation method:
- Compare pvlib output against these reference expectations (not against pvlib itself).
- Sanity invariants (zenith = 90 - alt, az in [0,360), altitude sign) remain separate.
- If discrepancy > tolerance, document rather than silently adjust.

## TASK 012 — Measurement / Observation (ingestion, not calibration/validation)
- Measurement contract extended: id, timestamp, variable (extensible), value, unit (required), location_target_id / spatial_ref, instrument/instrument_id/method/calibration_ref, observer_source, uncertainty (optional, None=unknown), provenance/quality_flag/notes, is_synthetic_example.
- Observation contract extended: observation_type, category, content, structured_attributes, value_numeric/unit only when appropriate, method/observer_source/uncertainty/notes/provenance/quality_flag, is_synthetic_example.
- Raw preservation enforced: serialization round-trip preserves exact value, unit, uncertainty=None, synthetic label.
- Lux semantics preserved: unit="lux"; no automatic PPFD conversion; no equating lux with photosynthesis.
- Spatial association: named object (location_target_id) or local coordinates (spatial_ref); coordinate convention +X East, +Y North, +Z Up remains.
- Uncertainty semantics: known = float; unknown/absent = None (explicit); never silently zero.
- Persistence: JSON (Pydantic); no database introduced; DuckDB remains optional for later analytical workload.
- Validation / calibration / regression / LightField comparison / photosynthesis inference deliberately deferred to TASK 013+.
- All fixtures synthetic; labeled; no invented survey values.

## TASK 013 — Light Validation (validation only; no calibration)
- Validation case contract: id, model_ref, measurement_ref, timestamp, spatial_ref, comparison_method, temporal_tolerance_sec, spatial_tolerance_m, result_status (PASS/FAIL/INCONCLUSIVE), metric_notes, provenance, is_synthetic_example.
- Matching: exact / nearest-within-threshold / nearest-beyond-threshold / unmatched; distance recorded; rejected explicitly; temporal gate (exact + configurable τ) documented.
- Metrics: structural only (matched/unmatched counts, spatial distance, match rate); rank correlation only on same-unit normalized data; NO RMSE lux-vs-relative_normalized; constant/insufficient arrays → INCONCLUSIVE.
- Unit distinction preserved: lux (Measurement.unit) vs relative_normalized (LightSample.unit); never directly compared numerically.
- PASS/FAIL/INCONCLUSIVE: PASS = comparison complete; FAIL = forbidden metric / impossible; INCONCLUSIVE = missing/unmatched/temporal out/unit mismatch/insufficient.
- Synthetic fixtures A-M labeled is_synthetic_example=True; no real measurements; no LightField edits.
- No calibration, no regression, no parameter fitting, no lux→PPFD.

## TASK 022 validation notes
- Allocation is deterministic (sorted sink_id order; no set/dict dependence).
- Synthetic fixtures: full demand (10 -> 10), limiting (5 -> 2.5/1.5/1.0), deficit (-3 -> deficit 3, allocated 0), zero demand, zero carbon.
- Conservation verified by test H (tolerance 1e-3); floating point described in result.conservation_check.
- No empirical calibration or independent observation comparison performed (not in scope).
- Allocation does not modify PlantArchitecture or PlantState (test R).

## TASK 023 — Growth validation notes
- Analytical reference: efficiency 0.5, carbon 10 => biomass 5 g_m2; carbon 4 * 0.25 => 1.
- No biological calibration or empirical comparison performed.
- Geometry derivation is simplified cylindrical approximation (fixed radius); not architectural.
- Source architecture isolation verified (test N/I).
