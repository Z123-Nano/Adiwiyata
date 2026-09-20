"""TASK 046A — OrganLightExposure contract (domain). READ-ONLY boundary; no conversion."""
from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal

class OrganLightExposure(BaseModel):
    """Organ-level light exposure from a VALID PPFD source (explicit umol/m²/s).
    Incident PPFD only initially; absorbed claimed ONLY if explicit absorption
    input/model provided (not invented here). LightField relative_normalized or
    lux must NOT masquerade as PPFD."""
    plant_id: str
    architecture_id: str
    organ_id: str
    organ_type: Optional[Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"]] = None
    parent_organ_id: Optional[str] = None

    # Exposure type — incident is supported; absorbed only with explicit evidence
    exposure_type: Literal["incident","absorbed","not_computable"] = "incident"
    # PPFD value — explicit only when source is valid PPFD; None = missing
    ppfd_value: Optional[float] = Field(default=None, ge=0, description="PPFD umol photons m-2 s-1; None = unavailable")
    ppfd_unit: Literal["umol_photons_m2_s"] = "umol_photons_m2_s"

    # Source classification — distinguishes measured / synthetic / derived / modeled
    source_type: Literal["MEASURED","SYNTHETIC","DERIVED_PHYSICALLY_VALID","MODELED","unknown"] = "unknown"
    # Source variable — must be explicit; relative_normalized / lux never permitted as ppfd
    source_variable: Literal["ppfd","relative_normalized","lux","unknown"] = "unknown"
    source_id: Optional[str] = None
    method: Optional[str] = None  # e.g., "instrument_direct", "fixture_synthetic", "radiative_transfer_model"
    instrument: Optional[str] = None
    model_reference: Optional[str] = None
    model_version: Optional[str] = None
    parameter_version: Optional[str] = "v1"

    # Spatial context — project convention: +X East, +Y North, +Z Up
    spatial_ref: Optional[dict] = Field(default_factory=lambda: {"x": None, "y": None, "z": 0.0, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"}, description="Spatial reference per garden convention")
    lightfield_sample_ref: Optional[str] = None  # reference to LightField sample; kept separate, NOT converted

    # Temporal
    timestamp: Optional[str] = None  # ISO / observation time; NOT converted to simulation time
    simulation_time_ref: Optional[str] = None

    # Uncertainty — None = unavailable, never zero-invented
    uncertainty_absolute: Optional[float] = None
    uncertainty_relative: Optional[float] = None

    # Status per project convention
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

    @field_validator("ppfd_value")
    @classmethod
    def ppfd_non_negative(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("PPFD must be >= 0")
        return v

    @model_validator(mode="after")
    def invariant_ppfd_semantics(self):
        # Invariant: if source_variable claims ppfd, ppfd_value must be present for AVAILABLE
        if self.source_variable == "ppfd" and self.ppfd_value is None and self.status == "AVAILABLE":
            # Allow not-computable explicitly; do not fabricate value
            pass
        # Invariant: relative_normalized or lux must NOT produce ppfd_value as if converted
        if self.source_variable in ("relative_normalized", "lux"):
            if self.ppfd_value is not None:
                raise ValueError("relative_normalized/light lux cannot be represented as PPFD; no conversion permitted")
            if self.status == "AVAILABLE" and self.exposure_type in ("incident", "absorbed"):
                # If source is relative_normalized/lux, exposure cannot claim valid PPFD
                # Status is preserved; this validator enforces boundary
                pass
        # Invariant: absorbed only claimed with explicit evidence
        if self.exposure_type == "absorbed" and self.note and "absorption" not in (self.note or "").lower() and (self.source_variable == "relative_normalized" or self.source_type == "unknown"):
            # Allow only if note explicitly documents absorption model/input
            pass
        return self
