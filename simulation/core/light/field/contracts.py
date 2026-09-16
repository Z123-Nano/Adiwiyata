"""LightField contracts — TASK 011. Domain-only; no lux/PPFD/LightField aggregation."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class LightSample(BaseModel):
    """Single spatial sample; components separate, not collapsed."""
    x: float = Field(..., description="East coordinate in garden local system (m)")
    y: float = Field(..., description="North coordinate")
    z: float = Field(default=0.0, description="Up/receiver height (m)")
    direct: float = Field(..., ge=0, le=1, description="Direct solar component relative normalized")
    diffuse: float = Field(..., ge=0, le=1, description="Diffuse sky component")
    reflected: float = Field(..., ge=0, le=1, description="First-order reflected")
    total: float = Field(..., ge=0, description="Sum direct+diffuse+reflected")
    unit: Literal["relative_normalized"] = "relative_normalized"

class LightField(BaseModel):
    """Spatial light field; sampling strategy documented; not a render output."""
    extent_min: tuple[float,float,float] = (0.0,0.0,0.0)
    extent_max: tuple[float,float,float] = (10.0,10.0,0.0)
    resolution: tuple[int,int,int] = (10,10,1)  # grid steps per axis; first implementation flat z
    samples: List[LightSample] = Field(default_factory=list)
    sampling_strategy: Literal["regular_grid_horizontal"] = "regular_grid_horizontal"
    model_version: Optional[str] = None
    solar_reference: Optional[str] = None  # timestamp reference
    approximation_params: Optional[dict] = None  # sky_vis, diffuse_baseline, reflectance, coeff
