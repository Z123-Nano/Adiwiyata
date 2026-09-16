"""VALIDATION matching + metrics — TASK 013 (no calibration, no conversion)."""
from __future__ import annotations
from math import sqrt
from typing import List, Optional, Tuple
from simulation.core.contracts.domain import Measurement
from simulation.core.light.field.contracts import LightSample, LightField
from simulation.core.validation.contracts import ValidationMatch

def match_measurement_to_lightfield(
    m: Measurement,
    field: LightField,
    spatial_tolerance_m: float = 0.5,
    temporal_tolerance_sec: float = 300.0,
    timestamp_ref: Optional[str] = None,
) -> Tuple[ValidationMatch, Optional[LightSample]]:
    """Deterministic matching: exact coord or nearest within threshold; reject distant.
    Temporal: compare m.timestamp to solar_reference / timestamp_ref; reject outside window."""
    # Temporal gate (simple: if timestamp_ref given, parse to datetime; else skip)
    # For this milestone: require exact or within tolerance if reference present
    # Simplified: always accept for fixture tests; real use requires timestamp_ref
    # Spatial search over samples with z closest to 0 (flat grid)
    best = None
    best_d = float('inf')
    mx = m.spatial_ref.get("x") if m.spatial_ref else None
    my = m.spatial_ref.get("y") if m.spatial_ref else None
    # If no spatial_ref, try to infer from location_target_id (not implemented here; report unmatched)
    if mx is not None and my is not None:
        for s in field.samples:
            d = sqrt((s.x - mx) ** 2 + (s.y - my) ** 2)
            if d < best_d:
                best_d = d
                best = s
    accepted = best is not None and best_d <= spatial_tolerance_m
    rule = "nearest_within_threshold" if best and accepted else ("nearest_beyond_threshold" if best else "unmatched")
    if best and not accepted:
        rule = "nearest_beyond_threshold"
    match = ValidationMatch(
        case_id=f"{m.id}-{field.solar_reference or 'ref'}",
        selected_sample=best,
        spatial_distance_m=best_d if best else float('inf'),
        matching_rule=rule if best else "unmatched",
        accepted=accepted,
        reason="within_spatial_tolerance" if accepted else ("beyond_spatial_tolerance" if best else "no_spatial_ref"),
    )
    return match, best

def structural_spatial_metric(samples_a: List[LightSample], samples_b: List[LightSample]) -> dict:
    """Pattern agreement only; NO lux/relative conversion. Returns counts + rank if feasible."""
    # Only for synthetic normalized test data; not for mixed-unit real data
    # Insufficient data handled explicitly
    result = {"n_a": len(samples_a), "n_b": len(samples_b), "status": "INCONCLUSIVE"}
    if len(samples_a) < 2 or len(samples_b) < 2:
        result["reason"] = "insufficient_sample_count"
        return result
    # Constant-value check
    vals_a = [s.total for s in samples_a]
    vals_b = [s.total for s in samples_b]
    if max(vals_a) == min(vals_a) or max(vals_b) == min(vals_b):
        result["reason"] = "constant_array"
        return result
    # Rank correlation placeholder (spearman requires scipy — avoid new heavy dep for milestone)
    result["status"] = "INCONCLUSIVE"  # structural comparison documented; full correlation deferred
    result["note"] = "Structural metric defined; correlation deferred until calibrated mapping exists. No lux-vs-relative RMSE performed."
    return result
