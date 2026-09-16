"""Photosynthesis input extension — TASK 020. PPFD/PAR direct; no lux conversion."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class PPFDInput(BaseModel):
    """Direct PPFD/PAR input for photosynthesis — μmol photons m^-2 s^-1."""
    ppfd: float = Field(..., ge=0, description="Photosynthetic photon flux density; μmol photons m^-2 s^-1")
    unit: Literal["umol_photons_m2_s"] = "umol_photons_m2_s"
    timestamp: Optional[datetime] = None
    organ_id: Optional[str] = None
    plant_id: Optional[str] = None
    source: Literal["synthetic","measurement","modeled","unknown"] = "unknown"
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
