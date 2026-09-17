"""Plant water status — TASK 025. Simplified model state; not real water potential."""
from __future__ import annotations
from simulation.core.water.contracts import PlantWaterStatus

def derive_water_status(
    plant_id: str,
    uptake_l: float,
    available_l: float,
    capacity_l: float,
    timestamp=None,
    provenance: str = None,
) -> PlantWaterStatus:
    if capacity_l <= 0:
        return PlantWaterStatus(
            plant_id=plant_id, status_indicator="deficit",
            relative_available=None, deficit_indicator=1.0,
            status="INVALID_INPUT",
            provenance=provenance or "TASK_025; non-positive capacity",
            notes="Capacity must be positive.")
    relative = min(1.0, available_l / capacity_l) if capacity_l > 0 else 0.0
    if relative >= 0.8:
        ind = "adequate"
    elif relative >= 0.4:
        ind = "limited"
    else:
        ind = "deficit"
    deficit = max(0.0, 1.0 - relative)
    return PlantWaterStatus(
        plant_id=plant_id, status_indicator=ind,
        relative_available=round(relative, 6),
        uptake_reference_l=round(uptake_l, 6),
        deficit_indicator=round(deficit, 6),
        timestamp=timestamp,
        status="VALID",
        provenance=provenance or "TASK_025; simplified model state (not measured potential)",
        notes="Normalized relative state; not true water potential.",
        is_synthetic_example=True,
    )
