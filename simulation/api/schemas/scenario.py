"""TASK 015 Scenario DTO — branch from Snapshot + overrides."""
from pydantic import BaseModel
from typing import Optional, Dict, List

class ScenarioResponse(BaseModel):
    scenario_id: str
    source_snapshot_id: Optional[str] = None
    status: str = "VALID"
    provenance: Optional[str] = None
    overrides: Optional[Dict] = None
    notes: Optional[str] = None
    is_derived: bool = True
