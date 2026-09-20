=== PATCH / FINAL ===
Patches (per review):
- Negative allocated carbon: rejected (not clamped); provenance preserves original.
- Negative previous biomass: rejected (not clamped); provenance preserves original.
- Missing identity: rejected (no fabricated id); provenance notes.
- Zero allocation: valid (increment 0, new = previous).
- Structural <= allocated verified (retention <=1 enforced by param).
- Units: g_C (allocated/structural) vs g_DM (biomass increment/new biomass) distinct.
- TASK 023 compatibility: GrowthResult.unit='g_C' (carbon-based biomass); 046J uses g_DM; documented in note; 023 NOT modified.
- Growth cost: handled by retention parameter (explicit); TASK 021 respiration handled upstream; no second deduction.
- No geometry mutation; no photosynthesis/respiration in derivation; pure.
Tests: 12/12 PASS; PYTEST unavailable reported honestly.
DECISION: TASK_046J_COMPLETE
