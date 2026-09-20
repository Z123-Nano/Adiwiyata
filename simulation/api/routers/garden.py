from fastapi import APIRouter
from simulation.api.services.garden_service import get_garden, get_garden_objects
router = APIRouter()

@router.get("/garden")
def read_garden():
    return get_garden()

@router.get("/garden/objects")
def read_objects():
    return get_garden_objects()
