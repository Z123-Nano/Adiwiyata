"""TASK 046H-E — Sink demand parameter contract (explicit; synthetic fixtures labeled)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class SinkParameterSet(BaseModel):
    """Explicit sink-demand parameters — no hidden constants; provenance required."""
    parameter_set_id: str = Field(..., description="Stable parameter-set identity")
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = Field(..., description="Organ type applicability")
    sink_coefficient_g_per_m_per_timestep: float = Field(..., gt=0, description="Sink strength per structural proxy unit (length_m) per timestep; g_C / m / timestep")
    structural_proxy_reference: Literal["length_m","radius_m","geometry_metadata","none"] = Field(default="length_m", description="Which domain quantity serves as proxy; must be explicit and documented")
    structural_proxy_unit: Literal["m","m2","dimensionless","none"] = Field(default="m", description="Unit of structural proxy")
    provenance: str = Field(..., description="Source / method / version / date / uncertainty if available")
    source_type: Literal["SYNTHETIC","LITERATURE","MEASURED","CALIBRATED","UNKNOWN"] = "SYNTHETIC"
    parameter_version: str = "v1"
    is_synthetic_example: bool = False
    note: Optional[str] = Field(None, description="Explicit limitations; synthetic label; no empirical claim")
    schema_version: Literal["v1"] = "v1"

    @model_validator(mode="after")
    def check_positive(self):
        if self.sink_coefficient_g_per_m_per_timestep <= 0:
            raise ValueError("sink_coefficient must be positive (potential demand non-negative)")
        return self

def sink_parameters(
    parameter_set_id: str,
    organ_type: str,
    sink_coefficient_g_per_m_per_timestep: float,
    structural_proxy_reference: str = "length_m",
    structural_proxy_unit: str = "m",
    provenance: str = "TASK_046H-E synthetic; minimal hybrid; coefficient not calibrated",
    source_type: str = "SYNTHETIC",
    is_synthetic_example: bool = True,
    note: Optional[str] = None,
) -> SinkParameterSet:
    return SinkParameterSet(
        parameter_set_id=parameter_set_id,
        organ_type=organ_type,
        sink_coefficient_g_per_m_per_timestep=sink_coefficient_g_per_m_per_timestep,
        structural_proxy_reference=structural_proxy_reference,
        structural_proxy_unit=structural_proxy_unit,
        provenance=provenance,
        source_type=source_type,
        is_synthetic_example=is_synthetic_example,
        note=note or "Synthetic parameter example: coefficient not empirically calibrated; structural proxy limited to length_m (no biomass/surface-area contract).",
    )
