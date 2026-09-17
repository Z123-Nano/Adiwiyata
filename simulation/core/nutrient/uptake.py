"""Nutrient uptake — TASK 026. First-order; available-limited; synthetic capacity."""
from __future__ import annotations
from simulation.core.nutrient.contracts import NutrientUptakeInput, NutrientUptakeResult

def nutrient_uptake(inp: NutrientUptakeInput) -> NutrientUptakeResult:
    if inp.requested_uptake_mg < 0:
        return NutrientUptakeResult(nutrient=inp.nutrient, requested_uptake_mg=inp.requested_uptake_mg, actual_uptake_mg=0, unmet_uptake_mg=abs(inp.requested_uptake_mg), status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative request")
    if inp.available_amount_mg < 0:
        return NutrientUptakeResult(nutrient=inp.nutrient, requested_uptake_mg=inp.requested_uptake_mg, actual_uptake_mg=0, unmet_uptake_mg=inp.requested_uptake_mg, status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative available")
    if inp.uptake_capacity_mg < 0:
        return NutrientUptakeResult(nutrient=inp.nutrient, requested_uptake_mg=inp.requested_uptake_mg, actual_uptake_mg=0, unmet_uptake_mg=inp.requested_uptake_mg, status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative capacity")
    if inp.root_organ_id is None and inp.plant_id is None:
        # Reference missing; not blocking calculation but noted; stay VALID if inputs okay
        pass
    actual = min(inp.requested_uptake_mg, inp.available_amount_mg, inp.uptake_capacity_mg)
    unmet = max(0.0, inp.requested_uptake_mg - actual)
    # Status synthetic thresholds
    ratio = actual / inp.requested_uptake_mg if inp.requested_uptake_mg > 0 else 1.0
    if ratio >= 0.8:
        ind = "adequate"
    elif ratio >= 0.5:
        ind = "limited"
    else:
        ind = "deficient"
    return NutrientUptakeResult(
        nutrient=inp.nutrient,
        requested_uptake_mg=round(inp.requested_uptake_mg, 6),
        actual_uptake_mg=round(actual, 6),
        unmet_uptake_mg=round(unmet, 6),
        water_status_reference=None,
        timestep_seconds=inp.timestep_seconds,
        status="VALID",
        provenance=inp.provenance or "TASK_026; uptake v1 synthetic",
        notes="Independent N/P/K; no interaction; synthetic thresholds.",
        is_synthetic_example=inp.is_synthetic_example,
    )
