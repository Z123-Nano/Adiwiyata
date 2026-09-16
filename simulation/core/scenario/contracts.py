"""Scenario branch contracts — TASK 015 (hypothetical branch; source snapshot immutable)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal, Any
from simulation.core.contracts.domain import InterventionEvent

class ScenarioModification(BaseModel):
    id: str
    target_id: Optional[str] = None
    modification_type: Literal["environment_override","spatial_metadata","intervention_record","parameter_override","other"]
    payload: Optional[dict] = None  # structured; not interpreted biologically
    timestamp: Optional[datetime] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class Scenario(BaseModel):
    scenario_id: str
    name: str
    description: Optional[str] = None
    source_snapshot_ref: str  # must reference existing snapshot
    created_at: datetime
    schema_version: Literal["v1"] = "v1"
    modifications: List[ScenarioModification] = Field(default_factory=list)
    parameter_overrides: Optional[dict] = None  # explicit; source parameter set not mutated
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    notes: Optional[str] = None

class BranchedState(BaseModel):
    """Independent state derived from snapshot + scenario modifications."""
    source_snapshot_ref: str
    scenario_ref: str
    simulation_time: float  # copied from snapshot; may be overridden explicitly
    garden_ref: Optional[str] = None
    modifications_applied: List[str] = Field(default_factory=list)  # modification ids
    provenance: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
