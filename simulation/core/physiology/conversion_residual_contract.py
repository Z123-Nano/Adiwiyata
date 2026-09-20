"""TASK 046P-J — ConversionResidualContract (explicit boundary, no physical destination implemented).
Pure; immutable inputs; UNMODELED baseline; STORAGE/LOSS gated (no implementation); g_C only.
Does NOT modify 046J/046G/046I/046P-G; no NSC/storage/loss/reserve/respiration mutation."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class ConversionResidualContract(BaseModel):
    """Explicit accounting at 046J growth boundary: allocated → structural + residual.
    Destination defaults to UNMODELED (current repository state). STORAGE/LOSS permitted
    only with explicit reference/state-transition evidence (gating enforced)."""
    schema_version: Literal["v1"] = "v1"
    parameter_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False

    result_id: str = Field(...)
    plant_id: str = Field(...)
    architecture_id: Optional[str] = None
    source_allocation_id: Optional[str] = None
    allocated_carbon_g: float = Field(..., ge=0, description="g_C from 046I allocation")
    retention: float = Field(..., ge=0, le=1, description="046J growth_retention_fraction")
    structural_carbon_g: float = Field(..., ge=0, description="g_C = allocated * retention")
    conversion_residual_carbon_g: float = Field(..., ge=0, description="g_C = allocated - structural")
    destination: Literal["UNMODELED","STORAGE","LOSS"] = "UNMODELED"
    storage_reference: Optional[str] = Field(None, description="Required if destination=STORAGE; must reference explicit storage-state/transition contract")
    loss_reference: Optional[str] = Field(None, description="Required if destination=LOSS; must reference explicit loss-process provenance")
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    timestep: float = Field(..., gt=0)
    simulation_time_ref: Optional[str] = None
    provenance: Optional[str] = None
    note: Optional[str] = Field(None, description="Explicit: UNMODELED = residual identified but destination not implemented. PARTIAL until destination contract exists.")

    @model_validator(mode="after")
    def check_equations(self):
        expected_struct = self.allocated_carbon_g * self.retention
        if abs(self.structural_carbon_g - expected_struct) > 1e-6:
            raise ValueError(f"Structural equation violated: {self.structural_carbon_g} vs {expected_struct}")
        expected_res = self.allocated_carbon_g - self.structural_carbon_g
        if abs(self.conversion_residual_carbon_g - expected_res) > 1e-6:
            raise ValueError(f"Residual equation violated: {self.conversion_residual_carbon_g} vs {expected_res}")
        # Conservation identity at boundary (accounting, not biological closure)
        if abs(self.allocated_carbon_g - (self.structural_carbon_g + self.conversion_residual_carbon_g)) > 1e-6:
            raise ValueError("Conservation identity violated")
        # Destination gating
        if self.destination == "STORAGE" and not self.storage_reference:
            raise ValueError("STORAGE requires explicit storage_reference (gating)")
        if self.destination == "LOSS" and not self.loss_reference:
            raise ValueError("LOSS requires explicit loss_reference (gating)")
        # Negative rejection
        if self.allocated_carbon_g < -1e-9:
            raise ValueError("Negative allocation rejected")
        if self.retention < -1e-9 or self.retention > 1 + 1e-9:
            raise ValueError("Retention must be in [0,1]")
        return self

def build_conversion_residual_contract(
    result_id: str,
    plant_id: str,
    allocated_carbon_g: float,
    retention: float,
    architecture_id: Optional[str] = None,
    source_allocation_id: Optional[str] = None,
    destination: Literal["UNMODELED","STORAGE","LOSS"] = "UNMODELED",
    storage_reference: Optional[str] = None,
    loss_reference: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time_ref: Optional[str] = None,
    provenance: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> ConversionResidualContract:
    """PURE: computes structural + residual from 046J inputs; destination UNMODELED by default.
    No mutation of 046J/046P-G/CarbonPool/SourceSinkAllocationResult."""
    structural = float(allocated_carbon_g) * float(retention)
    residual = float(allocated_carbon_g) - structural
    return ConversionResidualContract(
        result_id=result_id,
        plant_id=plant_id,
        architecture_id=architecture_id,
        source_allocation_id=source_allocation_id,
        allocated_carbon_g=float(allocated_carbon_g),
        retention=float(retention),
        structural_carbon_g=structural,
        conversion_residual_carbon_g=residual,
        destination=destination,
        storage_reference=storage_reference,
        loss_reference=loss_reference,
        timestep=timestep,
        simulation_time_ref=simulation_time_ref,
        provenance=provenance,
        is_synthetic_example=is_synthetic_example,
        note=f"TASK_046P-J: structural={structural}; residual={residual}; destination={destination}; UNMODELED unless STORAGE/LOSS contract provided; retention<1 => partial until destination defined; NO mutation of 046G/I/J/046P-G; g_C only.",
    )
