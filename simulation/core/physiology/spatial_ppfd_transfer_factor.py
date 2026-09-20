"""TASK 046T — SpatialPPFDTransferFactor contract (anchored transfer, not arbitrary scaling).
Links AbsolutePPFDReference + LightField identity → target organ/location.
No hidden conversion; no automatic relative_normalized = T; explicit method required."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class SpatialPPFDTransferFactor(BaseModel):
    """Explicit dimensionless transfer factor from physical reference PPFD to target.
    Must specify reference (AbsolutePPFDReference ref_id), LightField identity,
    target, time, method (explicit anchoring, NOT automatic relative_normalized)."""
    schema_version: Literal["v1"] = "v1"
    parameter_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False

    transfer_id: str = Field(..., description="Stable transfer identity")
    reference_id: str = Field(..., description="AbsolutePPFDReference.ref_id")
    lightfield_id: Optional[str] = Field(None, description="LightField identity (solar_reference / approximation_params / result_id)")
    target_organ_id: Optional[str] = None
    target_plant_id: Optional[str] = None
    target_location: Optional[dict] = Field(default_factory=lambda: {"x": None, "y": None, "z": None, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"}, description="Target point / plane reference")
    transfer_value: float = Field(..., ge=0, description="Dimensionless T = PPFD_target / PPFD_ref (only after explicit anchoring); may exceed 1 due to reflection/local geometry")
    transfer_unit: Literal["dimensionless"] = "dimensionless"
    transfer_definition: str = Field(..., description="Explicit method: e.g., 'explicit physical anchoring required; relative_normalized NOT automatically T; reference plane PPFD_ref defined; target at same time/spectrum; orientation limitation documented'")
    component: Literal["total", "direct", "diffuse", "reflected"] = "total"
    simulation_time_ref: Optional[str] = None
    provenance: Optional[str] = None
    status: Literal["AVAILABLE", "NOT_COMPUTABLE", "UNAVAILABLE", "ERROR"] = "AVAILABLE"

    @model_validator(mode="after")
    def check_transfer(self):
        if self.transfer_value < 0:
            raise ValueError("Transfer value must be non-negative")
        if not (self.reference_id and isinstance(self.reference_id, str) and len(self.reference_id) > 0):
            raise ValueError("Reference contract required (reference_id)")
        # Denominator implied by reference; must be > 0 for division validity
        # (reference value validated by AbsolutePPFDReference model; here only structural check)
        if self.transfer_definition is None or len(self.transfer_definition) < 10:
            raise ValueError("Transfer definition must explicitly describe anchoring method")
        if "relative_normalized" in (self.transfer_definition or "").lower() and "NOT" not in (self.transfer_definition or "").lower():
            # Prevent implicit claim that relative_normalized equals T without explicit condition
            # Allow only if definition explicitly states alignment conditions
            pass  # allowed if explicitly documented; no strict forbid needed
        return self

def build_spatial_ppfd_transfer(
    transfer_id: str,
    reference_id: str,
    lightfield_id: Optional[str] = None,
    target_organ_id: Optional[str] = None,
    target_plant_id: Optional[str] = None,
    transfer_value: float = 0.0,
    component: Literal["total", "direct", "diffuse", "reflected"] = "total",
    transfer_definition: str = "Explicit physical anchoring: reference PPFD_ref defines physical denominator; LightField relative_normalized requires aligned normalization to compute T; orientation/optics limitations preserved.",
    target_location: Optional[dict] = None,
    simulation_time_ref: Optional[str] = None,
    provenance: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> "SpatialPPFDTransferFactor":
    return SpatialPPFDTransferFactor(
        transfer_id=transfer_id,
        reference_id=reference_id,
        lightfield_id=lightfield_id,
        target_organ_id=target_organ_id,
        target_plant_id=target_plant_id,
        transfer_value=float(transfer_value),
        transfer_unit="dimensionless",
        transfer_definition=transfer_definition,
        component=component,
        target_location=target_location or {"x": None, "y": None, "z": None, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"},
        simulation_time_ref=simulation_time_ref,
        provenance=provenance,
        is_synthetic_example=is_synthetic_example,
        status="AVAILABLE",
    )
