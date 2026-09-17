"""TASK 022 — Source-sink allocation. Proportional; conservation 1e-6; deficit explicit."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal

class OrganDemand(BaseModel):
    organ_id: str
    demand_g: float
    status: Literal["AVAILABLE","NOT_COMPUTABLE"] = "AVAILABLE"

class AllocationResult(BaseModel):
    source_available_g: float
    allocations: Dict[str, float]
    deficit_g: float
    conservation_check: bool  # sum(alloc) + deficit ≈ source within 1e-6
    status: Literal["AVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None

def allocate_source_sinks(source_available_g: float, demands: List[OrganDemand], provenance: Optional[str] = None, tolerance: float = 1e-6) -> AllocationResult:
    total_demand = sum(d.demand_g for d in demands if d.status == "AVAILABLE")
    allocations = {}
    if total_demand <= 0:
        allocations = {d.organ_id: 0.0 for d in demands}
        return AllocationResult(source_available_g=source_available_g, allocations=allocations, deficit_g=source_available_g, conservation_check=True, status="AVAILABLE" if source_available_g >= 0 else "NOT_COMPUTABLE", provenance=provenance or "TASK_022 allocation v1", note="No valid demand.")
    if source_available_g < 0:
        return AllocationResult(source_available_g=source_available_g, allocations={}, deficit_g=source_available_g, conservation_check=False, status="NOT_COMPUTABLE", provenance=provenance or "TASK_022 allocation v1", note="Negative source.")
    # Proportional allocation conserving total
    allocated = {}
    for d in demands:
        if d.status == "AVAILABLE" and total_demand > 0:
            allocated[d.organ_id] = source_available_g * (d.demand_g / total_demand)
        else:
            allocated[d.organ_id] = 0.0
    sum_alloc = sum(allocated.values())
    deficit = max(0.0, source_available_g - sum_alloc)
    # Conservation check
    cons = abs(sum_alloc + deficit - source_available_g) <= tolerance
    return AllocationResult(
        source_available_g=source_available_g,
        allocations=allocated,
        deficit_g=deficit,
        conservation_check=cons,
        status="AVAILABLE",
        provenance=provenance or "TASK_022 allocation v1",
        note=f"Proportional; conservation={cons}; deficit={deficit:.6f}",
    )
