"""Respiration contracts — TASK 021. Minimal; explicit; no invented biomass unless synthetic fixture provides."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class RespirationParams(BaseModel):
    name: str
    maintenance_rate_per_biomass: float = Field(..., ge=0, description="Maintenance respiration rate per biomass; μmol CO2 g^-1 s^-1")
    source: Literal["synthetic_example","assumption_placeholder","unknown"] = "synthetic_example"
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    notes: Optional[str] = None
    schema_version: Literal["v1"] = "v1"

class RespirationInput(BaseModel):
    biomass_g_m2: Optional[float] = None  # synthetic/test only; None => NOT_COMPUTABLE
    temperature_c: Optional[float] = None
    organ_id: Optional[str] = None
    plant_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class RespirationResult(BaseModel):
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    respiratory_loss_rate: Optional[float] = None  # μmol CO2 m^-2 s^-1
    maintenance_rate_ref: Optional[str] = None
    biomass_input_ref: Optional[str] = None
    input_ref: Optional[str] = None
    provenance: Optional[str] = None
    assumptions: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
