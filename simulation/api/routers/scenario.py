"""TASK 015 Scenario router — branch from Snapshot; source unchanged."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from simulation.api.schemas.scenario import ScenarioResponse
from simulation.api.services.scenario_service import scenario_service
from simulation.api.services.snapshot_service import snapshot_service

router = APIRouter()

class ScenarioCreateIn(BaseModel):
    source_snapshot_id: str
    overrides: dict = {}

@router.get("/scenarios", response_model=list[ScenarioResponse])
def list_scenarios():
    return scenario_service.list_all()

@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: str):
    s = scenario_service.get_by_id(scenario_id)
    if s is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Scenario not found","id":scenario_id})
    return s

@router.post("/scenarios", response_model=ScenarioResponse)
def create_scenario(inp: ScenarioCreateIn):
    src = snapshot_service.get_by_id(inp.source_snapshot_id)
    if src is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Source snapshot not found","id":inp.source_snapshot_id})
    result = scenario_service.create_from_snapshot(inp.source_snapshot_id, inp.overrides)
    if result is None:
        raise HTTPException(status_code=400, detail={"code":"ERROR","message":"Branch failed"})
    return result
