"""Organ growth contracts — TASK 023. Mass-first; optional geometry; synthetic params; no growth claims."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List

class GrowthParam(BaseModel):
    name: str
    value: float
    unit: str
    provenance: Optional[str] = None
    is_synthetic_example: bool = True
    uncertainty_note: Optional[str] = None
    schema_version: Literal["v1"] = "v1"

class OrganGrowthInput(BaseModel):
    plant_id: Optional[str] = None
    organ_id: str
    organ_type: Literal["stem","branch","leaf","root","flower","other"] = "other"
    allocated_carbon: float  # umol CO2 m^-2 (from TASK 022)
    carbon_unit: Literal["umol_CO2_m2"] = "umol_CO2_m2"
    timestep_seconds: Optional[float] = None
    current_organ_state: dict = Field(default_factory=dict)  # snapshot of existing fields (length_m, radius_m, etc)
    growth_params: List[GrowthParam] = Field(default_factory=list)
    provenance: Optional[str] = None
    status: Literal["VALID","NOT_IMPLEMENTED","NOT_COMPUTABLE","INVALID_INPUT"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class OrganGrowthResult(BaseModel):
    plant_id: Optional[str] = None
    organ_id: str
    timestep_seconds: Optional[float] = None
    carbon_used: float  # <= allocated_carbon
    carbon_remaining: float
    biomass_change: float = 0.0  # g m^-2 (explicit synthetic conversion; not species-calibrated)
    biomass_unit: Literal["g_m2"] = "g_m2"
    length_change_m: Optional[float] = None  # only when geometry explicitly derived
    radius_change_m: Optional[float] = None
    geometry_status: Literal["COMPUTED","NOT_COMPUTABLE","NOT_IMPLEMENTED"] = "NOT_COMPUTABLE"
    updated_state_reference: Optional[dict] = None  # new state fields (not mutation of input)
    status: Literal["VALID","NOT_IMPLEMENTED","NOT_COMPUTABLE","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    model_version: Literal["v1"] = "v1"
    schema_version: Literal["v1"] = "v1"
