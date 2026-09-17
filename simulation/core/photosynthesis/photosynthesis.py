"""TASK 020 — Photosynthesis (rectangular hyperbola). Canonical; no replacement."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal

class PhotosynthesisParameters(BaseModel):
    alpha: float = Field(..., ge=0, description="Initial slope (g C / mmol PPFD / timestep baseline)")
    pmax: float = Field(..., ge=0, description="Maximum gross rate (g C per timestep)")
    version: Literal["v1"] = "v1"
    provenance: Optional[str] = None
    source: Literal["contract","fixture","calibrated","unknown"] = "contract"

class PhotosynthesisResult(BaseModel):
    gross_carbon_g: float
    ppfd_input: float
    unit: Literal["g_C_per_timestep"] = "g_C_per_timestep"
    timestep: float = 3600.0
    status: Literal["AVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    parameter_version: Optional[str] = "v1"

def photosynthesis_rectangular_hyperbola(ppfd: float, params: PhotosynthesisParameters, timestep: float = 3600.0) -> PhotosynthesisResult:
    """Rectangular hyperbola: gross = (alpha * PPFD * Pmax) / (alpha * PPFD + Pmax) scaled by timestep reference."""
    if ppfd < 0:
        return PhotosynthesisResult(gross_carbon_g=0.0, ppfd_input=ppfd, status="NOT_COMPUTABLE", note="Negative PPFD invalid", provenance=params.provenance)
    if params.alpha <= 0 or params.pmax <= 0:
        return PhotosynthesisResult(gross_carbon_g=0.0, ppfd_input=ppfd, status="NOT_COMPUTABLE", note="Parameters invalid", provenance=params.provenance)
    # Rectangular hyperbola (normalized per timestep context)
    gross = (params.alpha * ppfd * params.pmax) / (params.alpha * ppfd + params.pmax)
    # Scale to timestep if needed — preserve unit semantics; use baseline per-step for this contract
    gross = gross * (timestep / 3600.0)
    return PhotosynthesisResult(
        gross_carbon_g=gross,
        ppfd_input=ppfd,
        timestep=timestep,
        status="AVAILABLE",
        provenance=params.provenance or "TASK_020 photosynthesis v1",
        note="Rectangular hyperbola; PPFD input valid; no lux→PPFD conversion.",
        parameter_version=params.version,
    )
