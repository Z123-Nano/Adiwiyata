"""Respiration model — TASK 021. Minimal maintenance form; synthetic params; biomass required or NOT_COMPUTABLE. Source: structural maintenance reference; not species-calibrated."""
from __future__ import annotations
from simulation.core.physiology.respiration_contracts import RespirationInput, RespirationResult, RespirationParams

def respiration_rate(input_data: RespirationInput, params: RespirationParams) -> RespirationResult:
    if input_data.biomass_g_m2 is None:
        return RespirationResult(
            status="NOT_COMPUTABLE",
            respiratory_loss_rate=None,
            maintenance_rate_ref=params.name,
            biomass_input_ref=None,
            input_ref=None,
            provenance=f"TASK_021; biomass unavailable => NOT_COMPUTABLE; params_source={params.source}",
            assumptions=["biomass required for maintenance respiration"],
            notes="Respiration requires biomass input. No biomass invented.",
            is_synthetic_example=input_data.is_synthetic_example or params.is_synthetic_example,
        )
    if input_data.biomass_g_m2 < 0:
        return RespirationResult(
            status="INVALID_INPUT",
            respiratory_loss_rate=None,
            provenance="TASK_021; negative biomass rejected",
            notes="Biomass must be non-negative.",
        )
    rate = params.maintenance_rate_per_biomass * input_data.biomass_g_m2
    return RespirationResult(
        status="VALID",
        respiratory_loss_rate=round(rate, 6),
        maintenance_rate_ref=params.name,
        biomass_input_ref=str(input_data.biomass_g_m2),
        input_ref=None,
        provenance=f"TASK_021; equation=maintenance_rate*biomass; params_source={params.source}; {params.provenance or ''}",
        assumptions=["maintenance respiration only; growth respiration deferred"],
        notes=f"Rate = {params.maintenance_rate_per_biomass} * {input_data.biomass_g_m2} = {rate} μmol CO2 m^-2 s^-1.",
        is_synthetic_example=input_data.is_synthetic_example or params.is_synthetic_example,
    )
