"""TASK 046P-G — Passive Residual Reserve / Post-Allocation Carbon State Transition.
Pure state-transition contract; MODEL A baseline; no active storage physiology.
Synthetic fixtures labeled; no mutation of CarbonPool / SourceSinkAllocationResult.
Status determination handled by audit (046J retention boundary → PARTIAL)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class PostAllocationCarbonState(BaseModel):
    """Next reserve state after source-sink allocation (MODEL A — passive residual)."""
    schema_version: Literal["v1"] = "v1"
    parameter_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False

    plant_id: str = Field(...)
    architecture_id: Optional[str] = None
    previous_pool_id: Optional[str] = None
    previous_allocation_id: Optional[str] = None
    timestep: float = Field(..., gt=0)
    simulation_time: Optional[str] = None

    source_available_carbon_g: float = Field(..., description="CarbonPool.available_carbon_g at allocation (g_C); may be negative")
    total_allocated_carbon_g: float = Field(..., ge=0, description="From SourceSinkAllocationResult (g_C)")
    unallocated_carbon_g: float = Field(..., ge=0, description="Residual after allocation (g_C)")

    reserve_next_carbon_g: float = Field(..., ge=0, description="Passive reserve for next timestep = unallocated when source>0, else 0 (g_C)")
    carbon_deficit_g: float = Field(..., ge=0, description="Explicit deficit when source_available < 0; = max(-avail,0) (g_C)")

    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","PARTIAL","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def check_reserve_rule(self):
        # MODEL A baseline: reserve_next = unallocated for positive source; 0 for non-positive
        if self.source_available_carbon_g > 1e-9:
            if abs(self.reserve_next_carbon_g - self.unallocated_carbon_g) > 1e-6:
                raise ValueError(f"MODEL A violation: reserve_next={self.reserve_next_carbon_g} != unallocated={self.unallocated_carbon_g}")
        else:
            if self.reserve_next_carbon_g > 1e-9:
                raise ValueError(f"Negative/non-positive source must yield reserve_next=0; got {self.reserve_next_carbon_g}")
        # Deficit only when source < 0
        expected_deficit = max(-self.source_available_carbon_g, 0.0)
        if abs(self.carbon_deficit_g - expected_deficit) > 1e-6:
            raise ValueError(f"Deficit violation: deficit={self.carbon_deficit_g} vs expected={expected_deficit}")
        # Reserve never double-counted (not derived from current reserve + available)
        # Enforced structurally by contract definition (reserve_next from unallocated only)
        # Non-negative reserve and deficit
        if self.reserve_next_carbon_g < -1e-9 or self.carbon_deficit_g < -1e-9:
            raise ValueError("Negative reserve or deficit not permitted")
        return self

def compute_post_allocation_state(
    previous_pool_id: Optional[str],
    previous_allocation_id: Optional[str],
    source_available_carbon_g: float,
    unallocated_carbon_g: float,
    total_allocated_carbon_g: float,
    plant_id: str,
    architecture_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time: Optional[str] = None,
    provenance: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> PostAllocationCarbonState:
    """PURE: reserve_next = unallocated if source>0 else 0; deficit = max(-avail,0). No mutation of inputs."""
    if source_available_carbon_g > 1e-9:
        reserve_next = float(unallocated_carbon_g)
        deficit = 0.0
    else:
        reserve_next = 0.0
        deficit = float(max(-source_available_carbon_g, 0.0))
    return PostAllocationCarbonState(
        previous_pool_id=previous_pool_id,
        previous_allocation_id=previous_allocation_id,
        plant_id=plant_id,
        architecture_id=architecture_id,
        timestep=timestep,
        simulation_time=simulation_time,
        source_available_carbon_g=float(source_available_carbon_g),
        total_allocated_carbon_g=float(total_allocated_carbon_g),
        unallocated_carbon_g=float(unallocated_carbon_g),
        reserve_next_carbon_g=reserve_next,
        carbon_deficit_g=deficit,
        status="AVAILABLE" if source_available_carbon_g >= -1e-9 else "AVAILABLE",
        provenance=provenance,
        is_synthetic_example=is_synthetic_example,
        note="MODEL A passive residual reserve; 046J retention boundary requires retention==1.0 for full end-to-end conservation (PARTIAL if not satisfied)",
    )
