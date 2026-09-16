"""Photosynthesis parameters — TASK 020. Synthetic/example; provenance documented; no calibrated species values."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal

class PhotosynthesisParams(BaseModel):
    name: str
    a_max: float = Field(..., ge=0, description="Maximum assimilation rate; μmol CO2 m^-2 s^-1")
    alpha: float = Field(..., ge=0, description="Initial quantum efficiency; mol CO2 per mol photons")
    rd_ref: Optional[float] = Field(default=None, description="Dark respiration reference; separate process; not in light-response equation")
    source: Literal["synthetic_example","literature_reference","assumption_placeholder","unknown"] = "synthetic_example"
    provenance: Optional[str] = None
    uncertainty: Optional[str] = None  # "unknown" / "not_modelled" / "quantified_later"
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
