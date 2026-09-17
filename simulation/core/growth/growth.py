"""TASK 023 — Organ growth (mass-first). Geometry only if architecture contract supports."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal

class GrowthResult(BaseModel):
    organ_id: str
    architecture_id: Optional[str] = None
    biomass_increment_g: float
    efficiency: float = 0.5  # from parameter contract if available
    unit: Literal["g_C"] = "g_C"
    geometry_updated: bool = False  # true only if explicit geometry/density contract exists
    status: Literal["AVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None

def organ_growth(organ_id: str, allocated_carbon_g: float, architecture_id: Optional[str] = None, efficiency: float = 0.5, provenance: Optional[str] = None) -> GrowthResult:
    biomass = allocated_carbon_g * efficiency
    return GrowthResult(
        organ_id=organ_id,
        architecture_id=architecture_id,
        biomass_increment_g=biomass,
        efficiency=efficiency,
        status="AVAILABLE" if allocated_carbon_g >= 0 else "NOT_COMPUTABLE",
        provenance=provenance or "TASK_023 organ growth v1",
        note="Mass-first growth; geometry not fabricated unless architecture contract supports.",
        geometry_updated=False,
    )
