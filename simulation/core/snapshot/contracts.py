"""Snapshot / Checkpoint contracts — TASK 014 (immobile, serializable, no science added)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, List, Any

class ClockState(BaseModel):
    start: Optional[str] = None  # isoformat
    current: Optional[str] = None
    end: Optional[str] = None
    paused: bool = False

class ScheduledProcessState(BaseModel):
    id: str
    timestep_minutes: float
    priority: int
    enabled: bool
    next_run: Optional[str] = None

class SchedulerState(BaseModel):
    processes: List[ScheduledProcessState] = Field(default_factory=list)

class Snapshot(BaseModel):
    snapshot_id: str
    created_at: datetime
    simulation_time: float  # matches SimulationState.simulation_time
    world_time: Optional[str] = None  # clock.current isoformat
    world_time_tz: Optional[str] = None
    model_version_ref: Optional[str] = None
    parameter_set_ref: Optional[str] = None
    garden_ref: Optional[str] = None  # Garden id or serialized
    plant_states_refs: List[str] = Field(default_factory=list)
    environment_state_ref: Optional[str] = None
    clock_state: Optional[ClockState] = None
    scheduler_state: Optional[SchedulerState] = None
    random_seed: Optional[int] = None  # None = absent/not applicable
    provenance: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
    is_checkpoint: bool = False  # True = persisted artifact
    notes: Optional[str] = None

class Checkpoint(Snapshot):
    """Persisted snapshot — semantic distinction, same fields."""
    pass
