"""TASK 021 — Carbon / respiration. Canonical; preserve negative; no clipping."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal

class CarbonResult(BaseModel):
    gross_carbon_g: float
    respiration_g: float
    net_carbon_g: float
    timestep: float = 3600.0
    status: Literal["AVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    parameter_version: Optional[str] = "v1"

def carbon_respiration(gross_carbon_g: float, respiration_rate: float = 0.15, timestep: float = 3600.0, provenance: Optional[str] = None) -> CarbonResult:
    """net = gross - respiration; preservation of negative permitted per TASK 021."""
    respiration = gross_carbon_g * respiration_rate
    net = gross_carbon_g - respiration
    return CarbonResult(
        gross_carbon_g=gross_carbon_g,
        respiration_g=respiration,
        net_carbon_g=net,
        timestep=timestep,
        status="AVAILABLE",
        provenance=provenance or "TASK_021 carbon/respiration v1",
        note="Net carbon preserved with sign; no clipping unless contract requires.",
    )
