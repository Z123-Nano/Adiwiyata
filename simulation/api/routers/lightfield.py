"""TASK 038 — LightField endpoint: delegates to domain service; no physics in router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from simulation.api.schemas.lightfield import LightFieldResponse, LightSampleResponse
from simulation.api.services.lightfield_service import compute_lightfield_service

router = APIRouter()

class LightFieldInput(BaseModel):
    solar_ref: str = "synthetic"
    extent: list = [0,0,5,5]

@router.post("/lightfield/compute", response_model=LightFieldResponse)
def compute_lightfield(inp: LightFieldInput):
    # Delegate to domain; adapter does not compute scientifically
    try:
        bounds = tuple(inp.extent) if len(inp.extent) >= 4 else (0,5,0,5)
        # Use fixed sensible resolution for visualization stability
        result = compute_lightfield_service(grid_bounds=bounds, grid_res=(8,8), z_height=0.0)
    except Exception as e:
        # Preserve explicit status semantics; do not invent values
        return LightFieldResponse(
            extent_min=[0,0,0], extent_max=[5,5,0], resolution=[8,8,1],
            sampling_strategy="regular_grid_horizontal",
            sample_count=0, samples=[], status="NOT_COMPUTABLE",
            provenance="TASK_038; computation failed", note=str(e),
        )
    samples = [
        LightSampleResponse(
            x=s.x, y=s.y, z=s.z,
            direct=s.direct, diffuse=s.diffuse,
            reflected=s.reflected, total=s.total,
            unit=s.unit,
        ) for s in result.samples
    ]
    return LightFieldResponse(
        extent_min=list(result.extent_min),
        extent_max=list(result.extent_max),
        resolution=list(result.resolution),
        sampling_strategy=result.sampling_strategy,
        solar_reference=result.solar_reference,
        sample_count=len(samples),
        samples=samples,
        status="VALID",
        provenance="TASK_011 domain compute via lightfield_service",
        note="Direct/diffuse/reflected/total separated; relative_normalized; lux/PPFD not implied.",
    )
