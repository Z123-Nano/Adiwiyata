"""TASK 032 API DTOs — adapter boundary; not scientific source of truth."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    api_version: str
    app: str
    scientific_core: str
    note: Optional[str] = None

class PlantIdPath(BaseModel):
    plant_id: str

class GardenResponse(BaseModel):
    garden_id: str
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","INCONCLUSIVE","FAILED"]
    provenance: Optional[str] = None
    objects: List[Any] = Field(default_factory=list)
