"""TASK 046K — Architecture growth parameter contract (explicit synthetic)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class ArchitectureGrowthParameters(BaseModel):
    """Explicit geometry relation parameter — minimal specific-length only."""
    parameter_set_id: str = Field(...)
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = "other"
    relation_type: Literal["specific_length_linear", "allometric_power", "none"] = "specific_length_linear"
    specific_length_m_per_g_DM: float = Field(..., gt=0, description="m per g_DM; explicit; synthetic")
    provenance: str = Field(...)
    source_type: Literal["SYNTHETIC","LITERATURE","MEASURED","CALIBRATED","UNKNOWN"] = "SYNTHETIC"
    parameter_version: str = "v1"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
    note: Optional[str] = Field(None, description="Not calibrated; minimal bridge only; 023 growth uses g_C.")
    @model_validator(mode="after")
    def check_pos(self):
        if self.specific_length_m_per_g_DM <= 0:
            raise ValueError("specific_length_m_per_g_DM must be >0")
        return self

def architecture_growth_params(
    parameter_set_id: str,
    organ_type: str,
    specific_length_m_per_g_DM: float = 0.01,
    provenance: str = "TASK_046K synthetic; not calibrated; minimal specific-length bridge",
    source_type: str = "SYNTHETIC",
    is_synthetic_example: bool = True,
    note: Optional[str] = None,
) -> ArchitectureGrowthParameters:
    return ArchitectureGrowthParameters(
        parameter_set_id=parameter_set_id, organ_type=organ_type,
        relation_type="specific_length_linear",
        specific_length_m_per_g_DM=specific_length_m_per_g_DM,
        provenance=provenance, source_type=source_type,
        is_synthetic_example=is_synthetic_example,
        note=note or "Synthetic minimum; no empirical allometry; length_m only.",
    )
