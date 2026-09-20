"""TASK 039 — temporal endpoint (read-only). No mutation endpoints."""
from fastapi import APIRouter
from simulation.api.schemas.clock import ClockResponse
from simulation.api.services.clock_service import clock_service

router = APIRouter()

@router.get("/simulation/clock", response_model=ClockResponse)
def get_clock():
    return clock_service()
