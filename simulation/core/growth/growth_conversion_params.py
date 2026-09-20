"""TASK 046J — Growth conversion parameters (explicit; synthetic fixtures labeled)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class GrowthConversionParameters(BaseModel):
    """Explicit carbon-to-biomass conversion — not universal 1:1."""
    parameter_set_id: str = Field(..., description="Stable parameter set identity")
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = "other"
    growth_retention_fraction: float = Field(..., ge=0.0, le=1.0, description="Fraction of allocated carbon retained for structural biomass; [0,1]")
    carbon_fraction_of_dry_biomass: float = Field(..., gt=0.0, le=1.0, description="g_C per g_DM; >0 and <=1")
    provenance: str = Field(..., description="Source / method / version; synthetic if uncalibrated")
    source_type: Literal["SYNTHETIC","LITERATURE","MEASURED","CALIBRATED","UNKNOWN"] = "SYNTHETIC"
    parameter_version: str = "v1"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
    note: Optional[str] = Field(None, description="Explicit limitation: synthetic; not calibrated; TASK 023 unit=g_C incompatible with g_DM.")

    @model_validator(mode="after")
    def check_bounds(self):
        if self.growth_retention_fraction < 0 or self.growth_retention_fraction > 1:
            raise ValueError("growth_retention_fraction must be in [0,1]")
        if self.carbon_fraction_of_dry_biomass <= 0 or self.carbon_fraction_of_dry_biomass > 1:
            raise ValueError("carbon_fraction_of_dry_biomass must be in (0,1]")
        return self

def growth_params(
    parameter_set_id: str,
    organ_type: str,
    growth_retention_fraction: float = 1.0,
    carbon_fraction_of_dry_biomass: float = 0.5,
    provenance: str = "TASK_046J synthetic; not calibrated; TASK 023 uses g_C not g_DM",
    source_type: str = "SYNTHETIC",
    is_synthetic_example: bool = True,
    note: Optional[str] = None,
) -> GrowthConversionParameters:
    return GrowthConversionParameters(
        parameter_set_id=parameter_set_id,
        organ_type=organ_type,
        growth_retention_fraction=growth_retention_fraction,
        carbon_fraction_of_dry_biomass=carbon_fraction_of_dry_biomass,
        provenance=provenance,
        source_type=source_type,
        is_synthetic_example=is_synthetic_example,
        note=note or "Synthetic conversion; structural_carbon = allocated * retention; biomass = structural / carbon_fraction.",
    )
