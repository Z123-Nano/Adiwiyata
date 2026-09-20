"""TASK 046P-B — Integration context and result contracts (explicit, immutable)."""
from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field

class PhotosynthesisIntegrationContext(BaseModel):
    """Explicit inputs for rate → carbon mass conversion; no hidden area/time."""
    organ_id: str
    organ_photosynthetic_area_m2: float = Field(..., ge=0, description="Explicit organ photosynthetic area; must be > 0")
    elapsed_seconds: float = Field(..., gt=0, description="Explicit elapsed timestep in seconds")
    carbon_molar_mass_g_per_mol: float = Field(default=12.011, ge=0, description="IUPAC carbon atomic weight; documented")
    carbon_basis: Literal["ELEMENTAL_CARBON"] = "ELEMENTAL_CARBON"
    source: str = "TASK_046P-B synthetic"  # provenance
    provenance: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    is_synthetic_example: bool = False
    schema_version: Literal["046P-B-v1"] = "046P-B-v1"

class IntegratedPhotosyntheticCarbon(BaseModel):
    """Derived: rate × area × time → CO₂ amount → elemental carbon mass (g_C)."""
    result_id: str
    organ_id: str
    gross_assimilation_rate_umol_co2_m2_s: float = Field(..., description="Rate from TASK 020")
    organ_photosynthetic_area_m2: float
    elapsed_seconds: float
    gross_co2_amount_umol: float = Field(..., description="Rate × area × time")
    carbon_molar_mass_g_per_mol: float
    gross_carbon_g_C: float = Field(..., description="CO₂ amount × carbon molar mass × 1e-6")
    carbon_basis: Literal["ELEMENTAL_CARBON"] = "ELEMENTAL_CARBON"
    timestep: float
    status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["046P-B-v1"] = "046P-B-v1"
