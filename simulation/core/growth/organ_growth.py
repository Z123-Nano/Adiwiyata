"""TASK 046J — OrganGrowthResult (realized biomass increment; g_DM; not geometry)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class OrganGrowthResult(BaseModel):
    result_id: str = Field(..., description="Stable result identity")
    plant_id: str = Field(...)
    architecture_id: Optional[str] = None
    organ_id: str = Field(..., description="Organ identity")
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = "other"
    # Inputs preserved (not overwritten)
    allocated_carbon_g: float = Field(..., ge=0, description="Allocated carbon from 046I; g_C")
    previous_biomass_g_DM: float = Field(..., ge=0, description="Pre-step dry biomass; g_DM")
    # Conversion outputs — distinct
    structural_carbon_increment_g_C: float = Field(..., ge=0, description="Structural carbon retained after growth cost; g_C")
    biomass_increment_g_DM: float = Field(..., ge=0, description="Realized dry biomass increment; g_DM")
    new_biomass_g_DM: float = Field(..., ge=0, description="previous + increment; g_DM")
    growth_parameter_set_ref: str = Field(..., description="Reference to GrowthConversionParameters")
    timestep: float = Field(..., gt=0)
    simulation_time_ref: Optional[str] = None
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    source_reference: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False
    note: Optional[str] = Field(None, description="TASK 023 GrowthResult uses g_C (incompatible); 046J uses g_DM.")

    @model_validator(mode="after")
    def invariants(self):
        # Mass state consistency
        expected_new = self.previous_biomass_g_DM + self.biomass_increment_g_DM
        if abs(self.new_biomass_g_DM - expected_new) > 1e-6:
            raise ValueError("new_biomass != previous + increment")
        # Non-negative growth
        if self.biomass_increment_g_DM < -1e-6:
            raise ValueError("negative biomass increment")
        if self.previous_biomass_g_DM < -1e-6:
            raise ValueError("negative previous biomass")
        # Structural <= allocated when retention <=1
        # (parameter enforces; defensive here)
        if self.structural_carbon_increment_g_C > self.allocated_carbon_g + 1e-6:
            raise ValueError("structural carbon exceeds allocated carbon")
        return self
