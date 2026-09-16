"""Prediction contracts — TASK 016 (infrastructure; no biological forecasting; explicit NOT_COMPUTABLE)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, List

class PredictionRequest(BaseModel):
    request_id: str
    source_snapshot_ref: str
    scenario_ref: Optional[str] = None  # optional; must derive from same snapshot
    target_time: datetime  # timezone-aware
    model_version_ref: Optional[str] = None
    parameter_set_ref: Optional[str] = None
    deterministic_settings: Optional[dict] = None  # e.g. random_seed
    created_at: datetime
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class Prediction(BaseModel):
    prediction_id: str
    request_ref: str
    source_snapshot_ref: str
    scenario_ref: Optional[str] = None
    target_time: datetime
    created_at: datetime
    model_version_ref: Optional[str] = None
    parameter_set_ref: Optional[str] = None
    status: Literal["CREATED","READY","RUNNING","COMPLETED","FAILED","INCONCLUSIVE","NOT_COMPUTABLE"] = "CREATED"
    output_ref: Optional[str] = None  # future-state snapshot/checkpoint or projected state ref
    assumptions: List[str] = Field(default_factory=list)
    uncertainty_status: Literal["unknown","not_modelled","qualitative","quantified","not_applicable"] = "not_modelled"
    provenance: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
    notes: Optional[str] = None  # explicit: biological forecasting not available
    is_synthetic_example: bool = False
