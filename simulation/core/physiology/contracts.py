"""Plant Physiology contracts — TASK 019. Contracts only; no equations; placeholders explicit."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, List, Dict

# --- Input contracts ---
class LightInput(BaseModel):
    """Light reference for physiological process; unit preserved; not converted to PPFD unless contract exists."""
    source: Literal["LightField","LightSample","measurement","unknown"] = "unknown"
    sample_ref: Optional[str] = None
    variable: Literal["illuminance","relative_normalized","ppfd","unknown"] = "unknown"
    value: Optional[float] = None
    unit: Optional[str] = None  # e.g. lux, relative_normalized; must match variable
    timestamp: Optional[datetime] = None
    spatial_ref: Optional[dict] = None  # organ/plant/local
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class EnvironmentInput(BaseModel):
    temperature_c: Optional[float] = None  # explicitly unknown if missing
    co2_ppm: Optional[float] = None
    humidity_pct: Optional[float] = None
    water_availability: Optional[str] = None  # status/qualitative; not simulated value
    nutrient_state_ref: Optional[str] = None
    provenance: Optional[str] = None
    timestamp: Optional[datetime] = None

class PlantPhysiolInput(BaseModel):
    plant_id: str
    architecture_ref: Optional[str] = None
    state_ref: Optional[str] = None  # PlantState reference
    light_input: Optional[LightInput] = None
    environment_input: Optional[EnvironmentInput] = None
    timestamp: datetime
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

# --- State ---
class PlantPhysiologyState(BaseModel):
    plant_id: str
    timestamp: datetime
    # Carbon placeholders — unknown/not_modelled, not zero
    gross_carbon_assimilation: Optional[float] = None  # unit reserved; not filled
    respiration_carbon_loss: Optional[float] = None
    net_carbon: Optional[float] = None
    carbon_pool_g: Optional[float] = None  # available carbon; unknown = None
    carbon_allocation_state: Optional[str] = None  # qualitative/status
    # Water placeholders
    plant_water_status: Optional[str] = None  # qualitative
    root_zone_water_ref: Optional[str] = None
    transpiration_rate_ref: Optional[str] = None
    # Nutrient placeholders
    nitrogen_status: Optional[str] = None
    phosphorus_status: Optional[str] = None
    potassium_status: Optional[str] = None
    nutrient_limitation: Optional[str] = None
    # Gas exchange placeholders
    stomatal_conductance_ref: Optional[str] = None
    co2_reference_ppm: Optional[float] = None
    # Temperature / thermal
    plant_temperature_c: Optional[float] = None
    thermal_state: Optional[str] = None
    # Status / provenance
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    uncertainty_status: Literal["unknown","not_modelled","qualitative","quantified_later"] = "not_modelled"
    model_ref: Optional[str] = None
    provenance: Optional[str] = None
    notes: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False

# --- Process outputs ---
class PhotosynthesisResult(BaseModel):
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    gross_assimilation: Optional[float] = None  # placeholder; unit reserved
    limiting_factors: List[str] = Field(default_factory=list)
    input_ref: Optional[str] = None
    provenance: Optional[str] = None
    assumptions: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    is_synthetic_example: bool = False

class RespirationResult(BaseModel):
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    carbon_loss: Optional[float] = None
    maintenance_respiration_ref: Optional[str] = None
    growth_respiration_ref: Optional[str] = None
    input_ref: Optional[str] = None
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False

class CarbonBalanceResult(BaseModel):
    status: Literal["NOT_IMPLEMENTED","NOT_COMPUTABLE","VALID","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    gross_assimilation_ref: Optional[str] = None
    respiration_ref: Optional[str] = None
    net_carbon: Optional[float] = None
    source_sink_ref: Optional[str] = None
    input_ref: Optional[str] = None
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
