TASK 049 — Synthetic acquisition / measurement protocol — COMPLETE (design + audit; execution limited to fixtures/test)
Status: COMPLETE (design verified; full production-observation end-to-end deferred to future session with live protocol execution beyond quick audit; no data lost; fixtures/protocol preserved)
Evidence: tests/simulation/test_task049_quick.py PASS A-O; fixtures_049 + protocol_049 present; fixtures_047 sync contracts verified (SYNC_PPFD_0 / LUX_0 / ARCH_OBS_0); 046AB orchestrator used as reference boundary.
Contracts preserved: Measurement / Observation (047); PPFDSource (046O); LightField ≠ PPFD (046AB); no lux→PPFD; no calibration/fit/validation claim; synthetic label explicit; units explicit; spatial frame garden_local (+X East / +Y North / +Z Up, G0); multi-PPFD plan (low/mid/high) for 048 identifiability (alpha / pmax); raw→processed→derived→TASK_047_sync pipeline; dataset roles (calibration/verification/validation); immutability verified; determinism verified.
Scientific notes: protocol is synthetic-design only — no empirical garden measurements used; no parameter overwritten; 048 sensitivity / identifiability / dataset split preserved; observation sync (match_measurement_to_lightfield) verified conceptually via fixtures, not executed with live measurement ingestion (interrupted by audit request / quick-check request, not by defect).
No new science invented; no upstream mutation beyond minimal fixtures/protocol/test; no forbidden terms introduced (lux / relative_normalized / interpolation / nearest / average / broadcast) in production contracts.
Co-Authored-By: Claude Code <noreply@anthropic.com>

=== TASK 049-FIX ADDENDUM (2026-09-19) ===
Production APIs invoked (verified by test):
- simulation/core/validation/matching.py::match_measurement_to_lightfield (returns ValidationMatch + optional LightSample)
- simulation/core/validation/evaluation.py::validate_model (returns ValidationResult; leakage / empty / count-check / metrics)
- simulation/core/validation/contracts.py::ValidationMatch / ValidationResult / ValidationRequest / MetricCriterion (used directly)
SESSION_049 input path: fixtures_049.py (GARDEN_PROBE / PLANT_REGISTRY / SENSOR_REGISTRY / SESSION_049 / MULTI_PFD_PLAN / PIPELINE_STEPS) + fixtures_047.py (SYNC_PPFD_0 / SYNC_LUX_0 / ARCH_OBS_0 / BAD_ORGAN / BAD_TIME)
Valid PPFD sync result: accepted=True; selected_sample present; rule=nearest_within_threshold; case_id links to observation id; provenance/intact.
Wrong-organ: accepted=False; no nearest-organ fallback (production rule unmatched/beyond_threshold).
Wrong-time: observation timestamp preserved (10:00 vs 12:00); not silently replaced.
Lux/PPFD: SYNC_LUX_0.unit=="lux" preserved; no conversion; comparison requires same-unit paired lists.
Architecture discrepancy: validate_model(req, [0.20], [0.23]) → ValidationResult; no leakage; no calibration.
Missing-observation: unmatched result verified.
Uncertainty preservation: 30.0 / 0.02 preserved; not rewritten.
Provenance preservation: observation provenance strings intact; match case_id links to observation id.
Raw immutability: fixtures unchanged after all production calls (verified by assertions on ids/values/timestamps/quality).
Model/snapshot immutability: no architecture update; no parameter fit; no data assimilation; no state mutation.
Determinism: second call with identical inputs yields identical ValidationMatch (accepted, rule, case_id, selected_sample.x).
Production-boundary dependency (P): assert isinstance(match_ppfd, ValidationMatch) — fails if bypassed.
Static audit (changed test/fixture/report only; production matching/evaluation unedited): no lux→PPFD term in test or fixtures; no nearest fallback; no interpolation; no broadcast; no silent averaging; no mutation; no calibration; no parameter overwrite; no fabricated measurement.
Test command/result: python tests/simulation/test_task049_quick.py — PASS (33 PASS lines: original A-O + P + A-O production cases); exit 0.
Pytest availability: pytest module not installed; direct python execution used (identical assertions).
Explicit statements: not calibrated; not empirically validated; not biologically validated; no predictive validation; no real-garden calibration; synthetic protocol only; no new science; existing contracts reused only.
Changed files: tests/simulation/test_task049_quick.py (extended with production sync cases); TASK_049_COMPLETE.md (updated); fixtures_049/protocol_049 and fixtures_047 unchanged (used only).
Co-Authored-By: Claude Code <noreply@anthropic.com>
