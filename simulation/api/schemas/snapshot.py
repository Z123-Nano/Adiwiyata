"""TASK 014 Snapshot DTO — immutable checkpoint."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SnapshotResponse(BaseModel):
    snapshot_id: str
    timestamp: Optional[str] = None
    source_state_ref: Optional[str] = None
    version: str = "v1"
    schema_version: Optional[str] = "v1"
    provenance: Optional[str] = None
    status: str = "VALID"
    notes: Optional[str] = None
    is_immutable: bool = True
