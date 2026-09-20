"""TASK 007 — SimulationClock / scheduler domain contract (instantiated)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Literal

class SchedulerState(BaseModel):
    status: Literal["READY","RUNNING","PAUSED","UNAVAILABLE"] = "READY"
    timestep_mode: Literal["fixed","adaptive","manual"] = "fixed"
    next_scheduled_time: Optional[str] = None
    provenance: Optional[str] = None

class SimulationClock(BaseModel):
    simulation_time: datetime = Field(default_factory=lambda: datetime(2026, 9, 17, 12, 0, 0, tzinfo=timezone.utc), description="Domain simulation time — deterministic, not browser time")
    world_time: datetime = Field(default_factory=lambda: datetime(2026, 9, 17, 12, 0, 0, tzinfo=timezone.utc), description="Observation/world reference time")
    observation_time: datetime = Field(default_factory=lambda: datetime(2026, 9, 17, 10, 0, 0, tzinfo=timezone.utc), description="Last observation timestamp")
    timestep: float = 3600.0  # 1 hour fixed step
    timestep_mode: Literal["fixed","adaptive","manual"] = "fixed"
    timezone: str = "UTC"
    scheduler: SchedulerState = Field(default_factory=lambda: SchedulerState(status="READY", timestep_mode="fixed", provenance="TASK_007 scheduler domain"))
    clock_status: Literal["READY","ERROR","UNAVAILABLE"] = "READY"
    provenance: str = "TASK_007 SimulationClock v1; deterministic; source of truth for temporal boundary"
    version: str = "v1"

    class Config:
        validate_assignment = True

# Module-level instance (deterministic; no hidden global mutation)
_simulation_clock = SimulationClock()

def get_simulation_clock() -> SimulationClock:
    return _simulation_clock

def reset_clock() -> SimulationClock:
    global _simulation_clock
    _simulation_clock = SimulationClock()
    return _simulation_clock
