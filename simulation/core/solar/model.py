"""SolarPosition domain model — TASK 008.
Method: pvlib.solarposition.get_solarposition (NREL SPA).
License: MIT (pvlib 0.15.2).
Expected accuracy: ~0.01° per SPA specification.
Refraction: included by SPA; not separately corrected.
Convention: azimuth clockwise from true North (0=N, 90=E, 180=S, 270=W).
Altitude positive = Sun above horizon."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class SolarPosition(BaseModel):
    timestamp: datetime
    latitude_deg: float = Field(..., description="degrees, positive = North")
    longitude_deg: float = Field(..., description="degrees, positive = East")
    azimuth_deg: float = Field(..., ge=0, lt=360, description="clockwise from true North")
    altitude_deg: float = Field(..., description="positive = above geometric horizon")
    zenith_deg: float = Field(..., ge=0, le=180, description="90° - altitude")
    above_horizon: bool = Field(...)
    method: str = "pvlib.solarposition.get_solarposition (NREL SPA)"

class SolarLocation(BaseModel):
    latitude_deg: float
    longitude_deg: float
    elevation_m: Optional[float] = 0.0
