"""TASK 046I — Source-Sink Allocation result contract (potential → allocated, not growth)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List

class OrganAllocationItem(BaseModel):
    organ_id: str
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = "other"
    potential_demand_g: float = Field(..., ge=0)
    allocated_carbon_g: float = Field(..., ge=0)
    unmet_demand_g: float = Field(..., ge=0)
    allocation_fraction: float = Field(..., ge=0, le=1)
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None

class SourceSinkAllocationResult(BaseModel):
    result_id: str = Field(..., description="Stable allocation result identity")
    plant_id: str = Field(...)
    architecture_id: Optional[str] = None
    carbon_pool_id: Optional[str] = None
    timestep: float = Field(..., gt=0)
    simulation_time_ref: Optional[str] = None
    source_available_carbon_g: float = Field(..., description="Exact CarbonPool.available_carbon_g (may be negative)")
    allocatable_carbon_g: float = Field(..., ge=0, description="max(source_available,0) used for allocation")
    total_potential_demand_g: float = Field(..., ge=0)
    total_allocated_carbon_g: float = Field(..., ge=0)
    total_unmet_demand_g: float = Field(..., ge=0)
    unallocated_carbon_g: float = Field(..., ge=0)
    allocations: List[OrganAllocationItem] = Field(default_factory=list)
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    source_reference: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False
    note: Optional[str] = Field(None, description="Limited to proportional source-sink; no topology/priority/growth.")
    conservation_tolerance: float = 1e-6

    @model_validator(mode="after")
    def check_conservation(self):
        total_all = sum(a.allocated_carbon_g for a in self.allocations)
        total_unmet = sum(a.unmet_demand_g for a in self.allocations)
        source_pos = max(self.source_available_carbon_g, 0.0)
        # When source positive: sum allocated + unallocated ≈ source_pos
        if source_pos > 1e-9:
            if abs(total_all + self.unallocated_carbon_g - source_pos) > self.conservation_tolerance:
                raise ValueError(f"Conservation violated: allocated+unallocated={total_all+self.unallocated_carbon_g} vs source_pos={source_pos}")
        # Demand conservation: sum allocated + sum unmet ≈ total demand
        if abs(total_all + total_unmet - self.total_potential_demand_g) > self.conservation_tolerance:
            raise ValueError(f"Demand conservation violated: allocated+unmet={total_all+total_unmet} vs demand={self.total_potential_demand_g}")
        # Each allocated <= demand
        for a in self.allocations:
            if a.allocated_carbon_g > a.potential_demand_g + self.conservation_tolerance:
                raise ValueError(f"Allocated exceeds demand for {a.organ_id}")
        return self
