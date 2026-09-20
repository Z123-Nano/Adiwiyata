"""TASK 046T — AbsolutePPFDReference contract (physical boundary input).
Pure immutable; extends PPFDSource conventions; explicit geometry; no hidden conversion.
Baseline: UNMODELED until paired with SpatialPPFDTransferFactor and validated."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class AbsolutePPFDReference(BaseModel):
    """Explicit physical PPFD boundary for hybrid light architecture.
    Must be paired with SpatialPPFDTransferFactor before any organ PPFD computation."""
    schema_version: Literal["v1"] = "v1"
    parameter_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False

    ref_id: str = Field(..., description="Stable physical reference identity")
    ppfd_value: float = Field(..., ge=0, description="Instantaneous incident PPFD; µmol photons m^-2 s^-1; PAR 400-700")
    unit: Literal["umol_photons_m2_s"] = "umol_photons_m2_s"
    spectral_domain: Literal["PAR_400_700", "EPAR_400_750"] = "PAR_400_700"
    reference_geometry: Literal["ABOVE_CANOPY", "OPEN_SKY", "GARDEN_REFERENCE_PLANE", "LOCAL_REFERENCE_SENSOR", "OTHER_EXPLICIT"] = "GARDEN_REFERENCE_PLANE"
    reference_geometry_note: Optional[str] = Field(None, description="Explicit description of plane/context (e.g., horizontal plane at z=0, open-sky above canopy)")
    reference_position: Optional[dict] = Field(default_factory=lambda: {"x": None, "y": None, "z": None, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"}, description="Spatial location of reference measurement/context")
    timestamp: Optional[str] = None
    timezone: Optional[str] = None
    simulation_time_ref: Optional[str] = None
    source_type: Literal["MEASURED", "SYNTHETIC", "DERIVED_PHYSICALLY_VALID", "MODELED", "unknown"] = "unknown"
    instrument: Optional[str] = Field(None, description="Measurement instrument / method if measured")
    provenance: Optional[str] = None
    uncertainty: Optional[float] = Field(None, ge=0, description="Standard uncertainty of ppfd_value (µmol photons m^-2 s^-1) if available")
    status: Literal["AVAILABLE", "NOT_COMPUTABLE", "UNAVAILABLE", "ERROR"] = "AVAILABLE"

    @model_validator(mode="after")
    def check_reference(self):
        if self.ppfd_value < 0:
            raise ValueError("Absolute reference PPFD must be non-negative")
        if self.unit != "umol_photons_m2_s":
            raise ValueError("Unit must be umol_photons_m2_s")
        if self.spectral_domain not in ("PAR_400_700", "EPAR_400_750"):
            raise ValueError("Spectral domain must be PAR 400-700 (or EPAR)")
        if self.reference_geometry == "OTHER_EXPLICIT" and not self.reference_geometry_note:
            raise ValueError("OTHER_EXPLICIT requires reference_geometry_note")
        # Reference is valid boundary; does NOT claim full biological closure
        return self

def build_absolute_ppfd_reference(
    ref_id: str,
    ppfd_value: float,
    reference_geometry: Literal["ABOVE_CANOPY", "OPEN_SKY", "GARDEN_REFERENCE_PLANE", "LOCAL_REFERENCE_SENSOR", "OTHER_EXPLICIT"] = "GARDEN_REFERENCE_PLANE",
    reference_geometry_note: Optional[str] = None,
    reference_position: Optional[dict] = None,
    timestamp: Optional[str] = None,
    simulation_time_ref: Optional[str] = None,
    source_type: Literal["MEASURED", "SYNTHETIC", "DERIVED_PHYSICALLY_VALID", "MODELED", "unknown"] = "unknown",
    provenance: Optional[str] = None,
    uncertainty: Optional[float] = None,
    instrument: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> AbsolutePPFDReference:
    return AbsolutePPFDReference(
        ref_id=ref_id,
        ppfd_value=float(ppfd_value),
        reference_geometry=reference_geometry,
        reference_geometry_note=reference_geometry_note,
        reference_position=reference_position or {"x": None, "y": None, "z": None, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"},
        timestamp=timestamp,
        simulation_time_ref=simulation_time_ref,
        source_type=source_type,
        provenance=provenance,
        uncertainty=uncertainty,
        instrument=instrument,
        is_synthetic_example=is_synthetic_example,
    )
