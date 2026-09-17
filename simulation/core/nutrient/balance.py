"""Nutrient balance — TASK 026. Independent N/P/K; synthetic fraction; no chemistry."""
from __future__ import annotations
from simulation.core.nutrient.contracts import NutrientBalanceInput, NutrientBalanceResult, NutrientPoolState
from simulation.core.nutrient.pool import compute_available

def balance_nutrient(inp: NutrientBalanceInput) -> NutrientBalanceResult:
    # Validation
    p = inp.initial_pool
    if p.total_amount_mg < 0:
        return NutrientBalanceResult(nutrient=p.nutrient, initial_total_mg=p.total_amount_mg, input_mg=0, uptake_mg=0, loss_mg=0, final_total_mg=p.total_amount_mg, final_available_mg=0, balance_error_mg=p.total_amount_mg, status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative initial total")
    if inp.uptake_mg < 0:
        return NutrientBalanceResult(nutrient=p.nutrient, initial_total_mg=p.total_amount_mg, input_mg=0, uptake_mg=0, loss_mg=0, final_total_mg=p.total_amount_mg, final_available_mg=0, balance_error_mg=0, status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative uptake")
    if inp.loss_mg < 0:
        return NutrientBalanceResult(nutrient=p.nutrient, initial_total_mg=p.total_amount_mg, input_mg=0, uptake_mg=0, loss_mg=0, final_total_mg=p.total_amount_mg, final_available_mg=0, balance_error_mg=0, status="INVALID_INPUT", provenance=inp.provenance or "TASK_026; negative loss")
    for w in inp.inputs:
        if w.amount_mg < 0:
            return NutrientBalanceResult(nutrient=p.nutrient, initial_total_mg=p.total_amount_mg, input_mg=0, uptake_mg=0, loss_mg=0, final_total_mg=p.total_amount_mg, final_available_mg=0, balance_error_mg=0, status="INVALID_INPUT", provenance=inp.provenance or f"TASK_026; negative nutrient input for {w.nutrient}")
    total_input = sum(w.amount_mg for w in inp.inputs if w.nutrient == p.nutrient)
    final_total = p.total_amount_mg + total_input - inp.uptake_mg - inp.loss_mg
    if final_total < 0:
        final_total = 0.0  # should not happen with valid inputs; preserve explicitly
    avail_pool = NutrientPoolState(root_zone_id=p.root_zone_id, plant_id=p.plant_id, nutrient=p.nutrient, total_amount_mg=final_total, availability_fraction=p.availability_fraction)
    avail_state = compute_available(avail_pool)
    balance_error = p.total_amount_mg + total_input - inp.uptake_mg - inp.loss_mg - final_total
    return NutrientBalanceResult(
        nutrient=p.nutrient,
        initial_total_mg=round(p.total_amount_mg, 6),
        input_mg=round(total_input, 6),
        uptake_mg=round(inp.uptake_mg, 6),
        loss_mg=round(inp.loss_mg, 6),
        final_total_mg=round(final_total, 6),
        final_available_mg=round(avail_state.available_amount_mg, 6),
        balance_error_mg=round(balance_error, 6),
        timestep_seconds=inp.timestep_seconds,
        status="VALID",
        provenance=inp.provenance or "TASK_026; balance v1 synthetic",
        notes="Pool independent; availability synthetic fraction; no chemical kinetics.",
        is_synthetic_example=inp.is_synthetic_example or p.is_synthetic_example,
    )
