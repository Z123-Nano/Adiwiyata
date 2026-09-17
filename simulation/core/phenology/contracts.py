"""Phenology contracts — TASK 024. State machine; explicit stages; no species timing."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

STAGE_VOCAB = ("seed","germination","seedling","vegetative","flowering","fruiting","senescence","dormant","completed")

class PhenologyTransitionEvent(BaseModel):
    event_id: str
    plant_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    from_stage: Literal[*STAGE_VOCAB] = "seed"
    to_stage: Literal[*STAGE_VOCAB] = "seed"
    trigger_type: Literal["manual_observation","explicit_stage_event","accumulated_time","parameter_threshold"] = "manual_observation"
    reason: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class PhenologyState(BaseModel):
    plant_id: Optional[str] = None
    current_stage: Literal[*STAGE_VOCAB] = "seed"
    previous_stage: Optional[Literal[*STAGE_VOCAB]] = None
    stage_start_time: Optional[datetime] = None
    stage_start_age_days: Optional[float] = None  # explicit age reference; not simulation time
    transition_count: int = 0
    transition_history: List[PhenologyTransitionEvent] = Field(default_factory=list)
    last_transition_reason: Optional[str] = None
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_COMPUTABLE","NOT_IMPLEMENTED","INCONCLUSIVE"] = "VALID"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class PhenologyTransitionResult(BaseModel):
    plant_id: Optional[str] = None
    previous_stage: Optional[str] = None
    current_stage: Literal[*STAGE_VOCAB] = "seed"
    event: Optional[PhenologyTransitionEvent] = None
    status: Literal["VALID","INVALID_INPUT","NOT_IMPLEMENTED","NOT_COMPUTABLE","INCONCLUSIVE"] = "VALID"
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    model_version: Literal["v1"] = "v1"
    schema_version: Literal["v1"] = "v1"
