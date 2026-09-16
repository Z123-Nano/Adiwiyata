"""Light component contracts — TASK 010. Approximation only; no lux/PPFD/LightField."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal

class LightComponents(BaseModel):
    """Separate component identity preserved; no collapse to single scalar."""
    direct: float = Field(..., ge=0, description="Direct solar component (relative normalized 0-1)")
    diffuse: float = Field(..., ge=0, description="Diffuse sky component (relative normalized 0-1)")
    reflected: float = Field(..., ge=0, description="First-order reflected/environmental (relative normalized 0-1)")
    total: float = Field(..., ge=0, description="Direct + diffuse + reflected (not a sole source of truth)")
    unit: Literal["relative_normalized"] = "relative_normalized"
    normalization_note: str = "Relative intensity, NOT lux/PPFD; normalization = max expected direct + diffuse + reflected = 1.0 under clear daytime with full visibility"
    timestamp: Optional[str] = None

class DiffuseApproximation(BaseModel):
    """Simple daylight-sky approximation. Not full sky radiance."""
    sky_visibility_fraction: float = Field(..., ge=0, le=1, description="[0,1] sky visible (1 = full hemisphere visible)")
    daylight_factor: float = Field(..., ge=0, le=1, description="1 = clear daylight, 0 = night; based on solar altitude > 0")
    diffuse_output: float = Field(..., ge=0, le=1, description="daylight_factor * sky_visibility_fraction * clear_baseline(1.0)")
    daylight_baseline: float = 1.0  # normalized clear-day diffuse baseline

class ReflectedApproximation(BaseModel):
    """First-order bounded reflection — NOT radiosity/path-tracing."""
    surface_reflectance: float = Field(..., ge=0, le=1, description="Albedo-like [0,1]")
    visible_surface_fraction: float = Field(..., ge=0, le=1, description="[0,1] of surface visible to receiver")
    incident_environmental: float = Field(..., ge=0, le=1, description="Environmental light reaching surface (normalized)")
    reflection_coefficient: float = Field(default=0.3, ge=0, le=1, description="Bounded coefficient; prevents >100% amplification")
    reflected_output: float = Field(..., ge=0, description="reflectance * visible_frac * incident * coeff")
