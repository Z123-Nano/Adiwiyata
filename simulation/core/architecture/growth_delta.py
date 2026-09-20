"""TASK 046K — ArchitectureGrowthDelta result (proposal only; no mutation)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class ArchitectureGrowthDelta(BaseModel):
    result_id: str = Field(...)
    plant_id: str = Field(...)
    architecture_id: Optional[str] = None
    organ_id: str = Field(...)
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = "other"
    previous_biomass_g_DM: float = Field(..., ge=0)
    biomass_increment_g_DM: float = Field(..., ge=0)
    new_biomass_g_DM: float = Field(..., ge=0)
    geometry_dimension: Literal["length_m","radius_m","area_m2","volume_m3","none"] = "length_m"
    previous_length_m: float = Field(..., ge=0)
    delta_length_m: float = Field(..., ge=0, description="Non-negative for positive growth")
    proposed_length_m: float = Field(..., ge=0)
    relation_type: Literal["specific_length_linear","allometric_power","none"] = "specific_length_linear"
    parameter_set_ref: str = Field(...)
    timestep: float = Field(..., gt=0)
    simulation_time_ref: Optional[str] = None
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    source_reference: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False
    note: Optional[str] = Field(None, description="Delta proposal only; PlantOrgan not mutated; 023 unit=g_C noted.")

    @model_validator(mode="after")
    def invariants(self):
        if self.biomass_increment_g_DM < -1e-6:
            raise ValueError("negative biomass increment")
        if abs(self.new_biomass_g_DM - (self.previous_biomass_g_DM + self.biomass_increment_g_DM)) > 1e-6:
            raise ValueError("new biomass must equal previous + increment")
        if self.previous_length_m < -1e-6:
            raise ValueError("negative previous length")
        if self.delta_length_m < -1e-6:
            raise ValueError("negative delta length")
        if abs(self.proposed_length_m - (self.previous_length_m + self.delta_length_m)) > 1e-6:
            raise ValueError("proposed length = previous + delta")
        return self
