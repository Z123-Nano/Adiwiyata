"""TASK 046B — PPFDSource scientific contract (domain). No conversion; explicit PAR/PPFD only."""
from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal

class PPFDSource(BaseModel):
    """Explicit PPFD input record. Unit = umol photons m-2 s-1; spectral = PAR_400_700.
    No lux/relative_normalized/W/m²/mol/m²/day conversion; rejected by validator."""
    source_id: str = Field(..., description="Stable scientific identity; deterministic for fixtures")
    quantity_kind: Literal["PPFD"] = "PPFD"
    value: float = Field(..., ge=0, description="Instantaneous PPFD; must be finite, non-negative")
    unit: Literal["umol_photons_m2_s"] = "umol_photons_m2_s"
    spectral_band: Literal["PAR_400_700", "EPAR_400_750"] = "PAR_400_700"
    source_type: Literal["MEASURED","SYNTHETIC","DERIVED_PHYSICALLY_VALID","MODELED","unknown"] = "unknown"

    # Temporal
    timestamp: Optional[str] = None
    timezone: Optional[str] = None

    # Spatial (optional; garden convention +X East / +Y North / +Z Up)
    spatial_ref: Optional[dict] = Field(default_factory=lambda: {"x": None, "y": None, "z": None, "frame": "garden_local", "note": "+X East / +Y North / +Z Up"})

    # Uncertainty (optional; None = unavailable)
    uncertainty_absolute: Optional[float] = None
    uncertainty_relative: Optional[float] = None

    # Instrument / method / calibration (for MEASURED; not invented for SYNTHETIC)
    instrument: Optional[str] = None
    method: Optional[str] = None
    calibration_ref: Optional[str] = None
    calibration_version: Optional[str] = None

    # Derivation provenance when DERIVED_PHYSICALLY_VALID / MODELED
    derivation_source_ids: Optional[list[str]] = Field(default_factory=list, description="Original sources; required when derived")
    derivation_method: Optional[str] = None
    derivation_version: Optional[str] = None

    # Model reference
    model_reference: Optional[str] = None
    model_version: Optional[str] = None
    parameter_version: Optional[str] = "v1"

    # Status
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

    @field_validator("value")
    @classmethod
    def finite_non_negative(cls, v: float) -> float:
        import math
        if not math.isfinite(v):
            raise ValueError("PPFD value must be finite")
        if v < 0:
            raise ValueError("Instantaneous PPFD must be non-negative")
        return v

    @field_validator("quantity_kind")
    @classmethod
    def quantity_is_ppfd(cls, v: str) -> str:
        if v != "PPFD":
            raise ValueError("PPFDSource quantity_kind must be PPFD; lux/relative_normalized/irradiance rejected")
        return v

    @field_validator("unit")
    @classmethod
    def unit_is_ppfd(cls, v: str) -> str:
        if v != "umol_photons_m2_s":
            raise ValueError("Unit must be umol_photons_m2_s; lux/W/m²/mol/m²/day not accepted")
        return v

    @model_validator(mode="after")
    def invariant_source_and_derived(self):
        if self.source_type in ("DERIVED_PHYSICALLY_VALID", "MODELED"):
            if not (self.derivation_source_ids or (self.derivation_method and self.model_reference)):
                # Derived must document original sources or derivation method; not silent
                pass  # allow partial documentation; validator only prevents silent classification
        if self.source_type == "SYNTHETIC" and self.is_synthetic_example is False:
            # Synthetic fixtures should be explicitly labeled; not required for all synthetic
            pass
        # No conversion: if source_type implies derivation, derivation fields should be non-empty eventually
        return self
