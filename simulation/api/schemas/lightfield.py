"""LightField schema DTO — TASK 038. Preserves direct/diffuse/reflected/total separation."""
from pydantic import BaseModel
from typing import List, Optional, Literal

class LightSampleResponse(BaseModel):
    x: float
    y: float
    z: float
    direct: float
    diffuse: float
    reflected: float
    total: float
    unit: Literal["relative_normalized"] = "relative_normalized"

class LightFieldResponse(BaseModel):
    extent_min: List[float]
    extent_max: List[float]
    resolution: List[int]
    sampling_strategy: Literal["regular_grid_horizontal"] = "regular_grid_horizontal"
    solar_reference: Optional[str] = None
    sample_count: int
    samples: List[LightSampleResponse]
    status: str = "VALID"
    provenance: Optional[str] = None
    note: Optional[str] = None
