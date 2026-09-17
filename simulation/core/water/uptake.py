"""Root uptake — TASK 025. First-order; available-water limited; synthetic capacity."""
from __future__ import annotations
from simulation.core.water.contracts import RootUptakeInput, RootUptakeResult

def root_uptake(inp: RootUptakeInput) -> RootUptakeResult:
    if inp.requested_uptake_l < 0:
        return RootUptakeResult(
            requested_uptake_l=inp.requested_uptake_l, actual_uptake_l=0.0,
            unmet_uptake_l=abs(inp.requested_uptake_l), water_status="deficit",
            status="INVALID_INPUT", provenance=inp.provenance or "TASK_025; negative request",
            notes="Negative requested uptake rejected.")
    if inp.available_water_l < 0:
        return RootUptakeResult(
            requested_uptake_l=inp.requested_uptake_l, actual_uptake_l=0.0,
            unmet_uptake_l=inp.requested_uptake_l, water_status="deficit",
            status="INVALID_INPUT", provenance=inp.provenance or "TASK_025; negative available",
            notes="Negative available water rejected.")
    if inp.uptake_capacity_l < 0:
        return RootUptakeResult(
            requested_uptake_l=inp.requested_uptake_l, actual_uptake_l=0.0,
            unmet_uptake_l=inp.requested_uptake_l, water_status="deficit",
            status="INVALID_INPUT", provenance=inp.provenance or "TASK_025; negative capacity",
            notes="Negative uptake capacity rejected.")
    # Without root reference: NOT_IMPLEMENTED if required
    if inp.root_organ_id is None and inp.plant_id is None:
        # Allow calculation if inputs explicitly provide available water; but document missing reference
        pass  # proceed; reference optional for model calculation but required for integration
    requested = min(inp.requested_uptake_l, inp.uptake_capacity_l)
    actual = min(requested, inp.available_water_l)
    unmet = max(0.0, requested - actual)
    # Status based on ratio
    ratio = actual / requested if requested > 0 else 1.0
    if ratio >= 0.95:
        status_ind = "adequate"
    elif ratio >= 0.5:
        status_ind = "limited"
    else:
        status_ind = "deficit"
    return RootUptakeResult(
        requested_uptake_l=round(requested, 6),
        actual_uptake_l=round(actual, 6),
        unmet_uptake_l=round(unmet, 6),
        water_status=status_ind,
        timestep_seconds=inp.timestep_seconds,
        status="VALID",
        provenance=inp.provenance or "TASK_025; uptake v1",
        notes="Actual = min(requested, available, capacity). Synthetic.",
        is_synthetic_example=inp.is_synthetic_example,
    )
