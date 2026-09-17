"""Nutrient contracts — TASK 026. N/P/K only; mg; synthetic; no chemistry."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

NUTRIENT = Literal["N","P","K"]

class NutrientInput(BaseModel):
    nutrient: NUTRIENT
    amount_mg: float
    timestamp: Optional[datetime] = None
    source_type: Literal["fertilizer","organic","amendment","other"] = "fertilizer"
    target_root_zone_id: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class NutrientPoolState(BaseModel):
    root_zone_id: Optional[str] = None
    plant_id: Optional[str] = None
    nutrient: NUTRIENT
    total_amount_mg: float = 0.0
    available_amount_mg: float = 0.0
    unavailable_amount_mg: float = 0.0
    capacity_mg: Optional[float] = None
    availability_fraction: float = 0.5  # synthetic parameter
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class NutrientBalanceInput(BaseModel):
    initial_pool: NutrientPoolState
    inputs: List[NutrientInput] = Field(default_factory=list)
    uptake_mg: float = 0.0
    loss_mg: float = 0.0
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class NutrientBalanceResult(BaseModel):
    nutrient: NUTRIENT
    initial_total_mg: float
    input_mg: float
    uptake_mg: float
    loss_mg: float
    final_total_mg: float
    final_available_mg: float
    balance_error_mg: float
    timestep_seconds: Optional[float] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class NutrientUptakeInput(BaseModel):
    plant_id: Optional[str] = None
    root_organ_id: Optional[str] = None
    nutrient: NUTRIENT
    requested_uptake_mg: float
    available_amount_mg: float
    uptake_capacity_mg: float = 10.0
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class NutrientUptakeResult(BaseModel):
    nutrient: NUTRIENT
    requested_uptake_mg: float
    actual_uptake_mg: float
    unmet_uptake_mg: float
    water_status_reference: Optional[str] = None
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class PlantNutrientStatus(BaseModel):
    plant_id: Optional[str] = None
    N_status: Literal["adequate","limited","deficient"] = "adequate"
    P_status: Literal["adequate","limited","deficient"] = "adequate"
    K_status: Literal["adequate","limited","deficient"] = "adequate"
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
