from fastapi import APIRouter, HTTPException
from simulation.api.services.garden_service import get_plant
router = APIRouter()

@router.get("/plants")
def list_plants():
    return {"plants":[{"id":"plant-p1","status":"VALID","provenance":"TASK_034 domain source"}],"provenance":"TASK_034 domain source"}

@router.get("/plants/{plant_id}")
def get_plant_route(plant_id: str):
    result = get_plant(plant_id)
    if result is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Plant not found","plant_id":plant_id})
    return result
