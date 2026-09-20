"""TASK 043 — single-step endpoint (read-only execution, no mutation, no loop)."""
from fastapi import APIRouter
from pydantic import BaseModel
from simulation.api.schemas.simulation_step import SimulationStepResultResponse
from simulation.api.services.snapshot_service import snapshot_service
from simulation.api.services.scenario_service import scenario_service
from simulation.core.simulation.engine import simulation_engine

router = APIRouter()

class StepIn(BaseModel):
    source_ref: str  # snapshot_id or scenario_id
    source_type: str = "snapshot"  # "snapshot" | "scenario"

@router.post("/simulation/step", response_model=SimulationStepResultResponse)
def execute_step(inp: StepIn):
    src = None
    if inp.source_type == "snapshot":
        src = snapshot_service.get_by_id(inp.source_ref)
    elif inp.source_type == "scenario":
        src = scenario_service.get_by_id(inp.source_ref)
    # Engine produces new result; source never mutated
    result = simulation_engine.step(inp.source_ref, snapshot=src if inp.source_type == "snapshot" else None, scenario=src if inp.source_type == "scenario" else None)
    return SimulationStepResultResponse(
        result_id=result.result_id,
        source_snapshot_id=result.source_snapshot_id,
        source_scenario_id=result.source_scenario_id,
        previous_simulation_time=result.previous_simulation_time,
        next_simulation_time=result.next_simulation_time,
        timestep=result.timestep,
        component_statuses=[
            {"component": cs.component, "status": cs.status, "note": cs.note, "value": cs.value}
            for cs in result.component_statuses
        ],
        plant_state_ref=result.plant_state_ref,
        architecture_ref=result.architecture_ref,
        provenance=result.provenance,
        status=result.status,
        note=result.note,
    )
