"""Source-sink carbon allocation contracts — TASK 022. Allocation only; no growth; same unit as TASK 021."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class CarbonSource(BaseModel):
    source_id: str
    plant_id: Optional[str] = None
    available_carbon: float  # umol CO2 m^-2 (integrated over timestep)
    unit: Literal["umol_CO2_m2"] = "umol_CO2_m2"
    timestep_seconds: Optional[float] = None
    provenance: Optional[str] = None
    status: Literal["VALID","NOT_COMPUTABLE","NOT_IMPLEMENTED","INVALID_INPUT"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class CarbonSink(BaseModel):
    sink_id: str
    plant_id: Optional[str] = None
    organ_id: Optional[str] = None
    sink_type: Literal["stem","root","leaf","reproductive","other","maintenance"] = "other"
    demand: Optional[float] = None  # umol CO2 m^-2; None => NOT_COMPUTABLE
    priority: Optional[int] = None   # extensible; unenforced in v1
    capacity: Optional[float] = None  # extensible; unenforced in v1
    provenance: Optional[str] = None
    status: Literal["VALID","NOT_COMPUTABLE","NOT_IMPLEMENTED","INVALID_INPUT"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class SourceSinkAllocationRequest(BaseModel):
    source: CarbonSource
    sinks: List[CarbonSink]
    allocation_policy: Literal["proportional_demand","priority","stage_dependent","custom"] = "proportional_demand"
    timestep_seconds: Optional[float] = None
    model_version: Literal["v1"] = "v1"
    parameter_set_ref: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class SinkAllocation(BaseModel):
    sink_id: str
    allocated_carbon: float  # umol CO2 m^-2
    demand: Optional[float]
    unmet_demand: float
    status: Literal["VALID","NOT_COMPUTABLE","INVALID_INPUT"] = "VALID"

class SourceSinkAllocationResult(BaseModel):
    status: Literal["VALID","NOT_COMPUTABLE","NOT_IMPLEMENTED","INVALID_INPUT","INCONCLUSIVE"] = "NOT_IMPLEMENTED"
    source_carbon: float  # from source (original available; preserved separately)
    total_allocated: float
    unallocated_carbon: float
    carbon_deficit: float  # = max(0, -net_available_effective); 0 when source >=0
    sink_allocations: List[SinkAllocation]
    unmet_demand_total: float
    conservation_check: str  # descriptive; real check via values + tolerance
    conservation_tolerance: float = 1e-6
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
