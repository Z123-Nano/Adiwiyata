"""Carbon balance contracts — TASK 021. Net carbon bookkeeping; no growth."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class CarbonBalanceInput(BaseModel):
    photosynthesis_result_ref: str
    respiration_result_ref: Optional[str] = None
    timestep_seconds: float = Field(..., ge=0, description="Duration over which rates apply")
    organ_id: Optional[str] = None
    plant_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class CarbonBalanceResult(BaseModel):
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    gross_assimilation_rate: Optional[float] = None  # μmol CO2 m^-2 s^-1
    respiratory_loss_rate: Optional[float] = None    # μmol CO2 m^-2 s^-1
    net_carbon_rate: Optional[float] = None          # μmol CO2 m^-2 s^-1
    timestep_seconds: Optional[float] = None
    integrated_net_carbon: Optional[float] = None     # μmol CO2 m^-2 (rate * time)
    unit_rate: Literal["umol_CO2_m2_s"] = "umol_CO2_m2_s"
    unit_amount: Literal["umol_CO2_m2"] = "umol_CO2_m2"
    organ_id: Optional[str] = None
    plant_id: Optional[str] = None
    input_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
