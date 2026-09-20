"""TASK 043 — SimulationStep DTO."""
from pydantic import BaseModel
from typing import Optional, List, Literal, Any
from .measurement import MeasurementResponse  # reference only; not required

class ComponentStatusResponse(BaseModel):
    component: str
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"]
    note: Optional[str] = None
    value: Optional[Any] = None

class SimulationStepResultResponse(BaseModel):
    result_id: str
    source_snapshot_id: Optional[str] = None
    source_scenario_id: Optional[str] = None
    previous_simulation_time: Optional[str] = None
    next_simulation_time: Optional[str] = None
    timestep: float
    component_statuses: List[ComponentStatusResponse]
    plant_state_ref: Optional[str] = None
    architecture_ref: Optional[str] = None
    provenance: Optional[str] = None
    status: Literal["VALID","PARTIAL","NOT_COMPUTABLE","ERROR"] = "PARTIAL"
    note: Optional[str] = None
