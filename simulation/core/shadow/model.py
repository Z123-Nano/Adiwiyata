"""Direct shadow domain contract — TASK 009. Independent of R3F/Three.js."""
from __future__ import annotations
from pydantic import BaseModel, Field
from simulation.core.solar.model import SolarPosition
from typing import Optional, Literal

class SunDirection(BaseModel):
    """Direction of incoming sunlight in garden coordinates (+X East, +Y North, +Z Up).
    Vector points from sun toward ground (downward with az/alt components)."""
    dx: float = Field(..., description="East component (positive = sun from east toward observer)")
    dy: float = Field(..., description="North component")
    dz: float = Field(..., description="Down component (negative = sun above horizon)")
    azimuth_deg: float = Field(..., ge=0, lt=360)
    altitude_deg: float = Field(..., description="positive = sun above horizon")

class ShadowResult(BaseModel):
    sun_above_horizon: bool = Field(...)
    occluder_id: Optional[str] = None
    receiver_id: Optional[str] = None
    shadowed: bool = False
    shadow_length_m: Optional[float] = None
    shadow_direction_deg: Optional[float] = None  # clockwise from true north, projection on horizontal plane
    notes: Optional[str] = None

class Occluder(BaseModel):
    id: str
    geometry: Literal["box","wall","cylinder","point","other"] = "box"
    position: tuple[float,float,float] = (0.0,0.0,0.0)
    dimensions: tuple[float,float,float] = (1.0,1.0,1.0)  # w,y,h or w,d,h per type
    height_m: float = 1.0  # vertical extent above ground for simple shadow
