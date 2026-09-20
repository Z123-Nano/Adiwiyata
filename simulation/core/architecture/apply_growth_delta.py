"""TASK 046L — Pure application: ArchitectureGrowthDelta → new PlantArchitecture (proposal applied)."""
from __future__ import annotations
from typing import Optional, List
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.architecture.growth_delta import ArchitectureGrowthDelta

TOLERANCE = 1e-3

def apply_architecture_growth_delta(
    architecture: PlantArchitecture,
    delta: ArchitectureGrowthDelta,
) -> PlantArchitecture:
    """Pure: new architecture with updated organ length; source unchanged; only length changed."""
    # Identity validation
    if not architecture or not delta:
        raise ValueError("TASK_046L: architecture and delta required")
    if architecture.plant_id != delta.plant_id:
        raise ValueError("TASK_046L: plant_id mismatch")
    if architecture.architecture_id != delta.architecture_id:
        raise ValueError("TASK_046L: architecture_id mismatch")
    # Find target organ exactly once
    target_organ_id = delta.organ_id
    match = [o for o in (architecture.organs or []) if getattr(o, "id", None) == target_organ_id]
    if len(match) != 1:
        raise ValueError(f"TASK_046L: organ_id {target_organ_id} must exist exactly once; found {len(match)}")
    target = match[0]
    # Base geometry consistency
    current_length = float(getattr(target, "length_m", None) or 0.0)
    if abs(current_length - delta.previous_length_m) > TOLERANCE:
        raise ValueError(
            f"TASK_046L: stale delta — current length {current_length} unlike delta.base {delta.previous_length_m} (tolerance {TOLERANCE})"
        )
    # Double-application guard: if delta > 0 and current length already at result, reject
    # After first apply new_length = base + delta > base; second apply base check fails because current != delta.previous
    # Zero delta is allowed (idempotent by design; still new state)
    # Apply only length change; preserve all else
    new_organ = target.model_copy(deep=True)
    # Update length with delta (delta >= 0 per contract; negative rejected by delta contract)
    new_length = current_length + delta.delta_length_m
    new_organ.length_m = new_length
    # Build new architecture with copied organs list
    new_organs = [new_organ if getattr(o, "id", None) == target_organ_id else o.model_copy(deep=True) for o in (architecture.organs or [])]
    # Create new architecture preserving identity and all non-target organs
    new_arch = architecture.model_copy(deep=True)
    new_arch.organs = new_organs  # type: ignore
    # Preserve provenance / note
    new_notes = (new_arch.notes or "") + f"; TASK_046L delta={delta.delta_length_m} organ={target_organ_id}; source_delta={delta.result_id}"
    new_arch.notes = new_notes
    # Explicit: source architecture unchanged (verified by caller)
    return new_arch
