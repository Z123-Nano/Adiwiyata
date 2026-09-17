"""Water domain contracts — TASK 025. Simplified reservoir; liters; synthetic; no soil hydraulics."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class WaterInput(BaseModel):
    timestamp: Optional[datetime] = None
    amount_l: float  # liters; explicit unit
    source_type: Literal["irrigation","rainfall","other"] = "other"
    spatial_reference: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class RootZoneState(BaseModel):
    root_zone_id: Optional[str] = None
    plant_id: Optional[str] = None
    storage_l: float = 0.0  # liters; must be >=0 and <= capacity
    capacity_l: float = 10.0
    available_water_l: float = 0.0  # computed; not independently set
    unavailable_floor_l: float = 0.0  # synthetic parameter
    lower_bound_l: float = 0.0
    upper_bound_l: float = 0.0  # typically capacity
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class WaterBalanceInput(BaseModel):
    initial_state: RootZoneState
    inputs: List[WaterInput] = Field(default_factory=list)
    drainage_l: float = 0.0
    uptake_l: float = 0.0
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class WaterBalanceResult(BaseModel):
    initial_storage_l: float
    total_input_l: float
    uptake_l: float
    drainage_l: float
    final_storage_l: float
    balance_error_l: float  # should be ~0 within tolerance
    timestep_seconds: Optional[float] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class RootUptakeInput(BaseModel):
    plant_id: Optional[str] = None
    root_organ_id: Optional[str] = None
    available_water_l: float
    requested_uptake_l: float
    timestep_seconds: Optional[float] = None
    uptake_capacity_l: float = 5.0  # synthetic; per-timestep demand
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class RootUptakeResult(BaseModel):
    requested_uptake_l: float
    actual_uptake_l: float
    unmet_uptake_l: float
    water_status: Literal["adequate","limited","deficit"] = "adequate"
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class PlantWaterStatus(BaseModel):
    plant_id: Optional[str] = None
    status_indicator: Literal["adequate","limited","deficit"] = "adequate"
    relative_available: Optional[float] = None  # 0..1 model state, not real water potential
    uptake_reference_l: Optional[float] = None
    deficit_indicator: Optional[float] = None
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
