"""Carbon balance — TASK 021. Net = gross - respiration; same time basis; explicit timestep; no growth."""
from __future__ import annotations
from typing import Optional
from simulation.core.physiology.carbon_contracts import CarbonBalanceInput, CarbonBalanceResult
from simulation.core.physiology.photosynthesis import photosynthesis_rate
from simulation.core.physiology.photosynthesis_fixtures import SYNTH_PARAMS

def carbon_balance(
    photosynthesis_result_ref: str,
    respiration_result_ref: Optional[str],
    gross_rate: float,
    respiration_rate: Optional[float],
    timestep_seconds: float,
    input_ref: Optional[str] = None,
    provenance: Optional[str] = None,
) -> CarbonBalanceResult:
    if timestep_seconds < 0:
        return CarbonBalanceResult(
            status="INVALID_INPUT",
            notes="Negative timestep rejected.",
            provenance="TASK_021; invalid timestep",
        )
    if gross_rate < 0:
        return CarbonBalanceResult(
            status="INVALID_INPUT",
            notes="Negative gross assimilation rejected.",
            provenance="TASK_021; invalid gross rate",
        )
    if respiration_rate is not None and respiration_rate < 0:
        return CarbonBalanceResult(
            status="INVALID_INPUT",
            notes="Negative respiration rejected.",
            provenance="TASK_021; invalid respiration",
        )
    resp = respiration_rate if respiration_rate is not None else 0.0
    net_rate = gross_rate - resp
    integrated = net_rate * timestep_seconds  # μmol CO2 m^-2 over interval
    return CarbonBalanceResult(
        status="VALID",
        gross_assimilation_rate=round(gross_rate, 6),
        respiratory_loss_rate=round(resp, 6) if respiration_rate is not None else None,
        net_carbon_rate=round(net_rate, 6),
        timestep_seconds=timestep_seconds,
        integrated_net_carbon=round(integrated, 6),
        unit_rate="umol_CO2_m2_s",
        unit_amount="umol_CO2_m2",
        provenance=provenance or "TASK_021; net=gen-res; synthetic",
        notes="Net carbon = gross assimilation - respiratory loss. Not biomass growth.",
        is_synthetic_example=True,
    )
