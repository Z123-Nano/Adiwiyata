"""TASK 046N — Domain orchestration result contract.
Minimal; uses existing status vocabulary; no new physics.
"""
from __future__ import annotations
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class FSPMTimestepResult(BaseModel):
    step_id: str
    source_state_id: Optional[str] = None
    architecture_before_id: Optional[str] = None
    architecture_after_id: Optional[str] = None
    simulation_time_before: Optional[str] = None
    simulation_time_after: Optional[str] = None
    timestep: Optional[float] = None
    status: Literal["COMPLETE","PARTIAL","NOT_COMPUTABLE","INVALID_INPUT"] = "PARTIAL"
    lightfield_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "AVAILABLE"
    physiology_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "NOT_COMPUTABLE"
    carbon_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "NOT_COMPUTABLE"
    demand_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "NOT_COMPUTABLE"
    allocation_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "NOT_COMPUTABLE"
    growth_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT"] = "NOT_COMPUTABLE"
    architecture_status: Literal["AVAILABLE","NOT_COMPUTABLE","INVALID_INPUT","UNCHANGED"] = "UNCHANGED"
    lightfield_result_ref: Optional[str] = None
    carbon_result_ref: Optional[str] = None
    demand_result_refs: List[str] = Field(default_factory=list)
    allocation_result_ref: Optional[str] = None
    growth_result_refs: List[str] = Field(default_factory=list)
    architecture_delta_refs: List[str] = Field(default_factory=list)
    provenance: Optional[str] = None
    schema_version: Literal["046N-v1"] = "046N-v1"
    is_synthetic_example: bool = False
    orientation_aware: bool = False
    notes: Optional[str] = ("Coarse architecture-derived shadow approximation; "
                            "LightField relative_normalized ≠ PPFD; "
                            "downstream physiology unavailable due to missing PPFDSource; "
                            "no orientation-aware optics; architecture unchanged at step boundary.")
