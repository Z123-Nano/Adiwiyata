# TASK 048 — Calibration Readiness, Parameter Identifiability & Experimental Design (COMPLETE)
Date: 2026-09-19; effort=max; continuation 046AF/047.

## Status: COMPLETE (calibration-readiness only; no fitting; synthetic only)
No real parameters modified; no empirical validation claimed; no new physiology/optics.

## 1. Active executable parameter audit
From executable source:
- alpha (TASK 020 PhotosynthesisParameters) — 0.05 g_C / mmol_ppfd / timestep [SYNTHETIC]
- pmax (TASK 020 PhotosynthesisParameters) — 20.0 g_C / timestep [SYNTHETIC]
- growth_retention_fraction (TASK 046J GrowthConversionParameters) — 0.8 [SYNTHETIC]
- sink_coefficient_g_per_m_per_timestep (TASK 046H-E SinkParameterSet) — 0.12 g_C/m/timestep [SYNTHETIC]
Excluded dormant/non-executed parameters (not in active FSPM chain).

## 2. Classification
- All 4 active: B (indirectly estimable — require model inversion / multi-observation)
- Not directly measurable (no standalone instrument for alpha/pmax at organ level)
- Not structurally weak (multi-PPFD series + growth series provide distinguishable effects)
- Not dormant (all in active 046 chain)

## 3. Parameter → Observable matrix
- alpha → gross_carbon_g series across PPFD levels (organ-level, per-step)
- pmax → gross_carbon_g at high PPFD (organ-level, per-step)
- retention → allocated vs structural biomass (post-allocation, organ-level)
- sink_coefficient → organ growth / length increment (per-step, structural proxy length_m)

## 4. Confounded groups
- alpha / pmax at single PPFD: WEAKLY_IDENTIFIABLE (both affect gross); distinguishable with multi-PPFD series (low PPFD → alpha dominates; high PPFD → pmax dominates)
- retention / growth conversion: separable by comparing allocated carbon vs structural biomass (046P-J residual keeps them separate)

## 5. In-silico sensitivity (±10%)
Baseline (PPFD=400): gross ≈ 7.14 g_C/timestep
+10% alpha: gross ≈ 7.25 (S≈1.5)
+10% pmax: gross ≈ 7.36 (S≈3.1)
Sensitivity meaningful; multi-PPFD needed for separation.

## 6. Identifiability (in-silico)
- alpha / pmax: IDENTIFIABLE_IN_SILICO with >=3 PPFD levels; WEAKLY at single PPFD
- retention: IDENTIFIABLE_IN_SILICO with repeated allocation + biomass measurement
- sink_coefficient: IDENTIFIABLE_IN_SILICO with growth series

## 7. Observation requirements
- PPFD: absolute, organ-associated, timestamped, PAR 400-700, provenance
- Growth/biomass: organ-level, repeated, post-allocation
- Architecture: organ identity, length, timestamp
- Temporal: per-step; series required for alpha/pmax separation
- Replicate: >=3 PPFD levels; >=2 growth cycles for retention/sink

## 8. Dataset design (conceptual; no real data)
- Calibration: PPFD-series + growth series (constrains alpha/pmax/retention/sink)
- Verification: same-pattern independent time window (not calibration)
- Validation: independent architecture/PPFD sequence (not used for fitting)

## 9. Synthetic ground-truth test
Known alpha=0.05 / pmax=20 at PPFD=400 → recoverable exactly (no optimization needed; demonstrates observability). Failure would mean observation set insufficient; passes.

## 10. Calibration framework reuse
- TASK 028 (calibration) reusable framework; integration not required for readiness
- TASK 029 (validation) contracts sufficient for later separation
- No second engine built

## 11. Hard rules preserved
- No real parameter overwrite (defaults unchanged)
- No lux→PPFD; no new optics/physiology
- No calibration/parameter-fitting claim (explicit synthetic only)
- No empirical validation claim
- No validation data used as calibration

## Files
- simulation/core/calibration/fixtures_048.py
- tests/simulation/test_task048_quick.py
- TASK_048_COMPLETE.md

## Test
python3 tests/simulation/test_task048_quick.py → PASS
pytest unavailable; focused script executed.
