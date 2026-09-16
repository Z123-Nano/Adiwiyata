"""Validation contracts — TASK 013 (validation only; no calibration)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, List
from simulation.core.contracts.domain import Measurement, LightField
from simulation.core.light.field.contracts import LightSample

class ValidationCase(BaseModel):
    id: str
    model_ref: str  # LightField reference / timestamp
    measurement_ref: str  # Measurement id
    timestamp: datetime
    spatial_ref: Optional[dict] = None  # {x,y,z} or named reference
    comparison_method: Literal["exact_spatial","nearest_spatial","structural_spatial"] = "nearest_spatial"
    temporal_tolerance_sec: float = 300.0  # configurable; 0 = exact
    spatial_tolerance_m: float = 0.5  # max distance for nearest match
    result_status: Literal["PASS","FAIL","INCONCLUSIVE"] = "INCONCLUSIVE"
    metric_notes: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class ValidationMatch(BaseModel):
    case_id: str
    selected_sample: Optional[LightSample] = None  # domain-only; not converted
    spatial_distance_m: float = 0.0
    matching_rule: Literal["exact","nearest_within_threshold","nearest_beyond_threshold","unmatched"] = "unmatched"
    accepted: bool = False
    reason: Optional[str] = None  # explicit rejection cause

class ValidationResult(BaseModel):
    case_id: str
    status: Literal["PASS","FAIL","INCONCLUSIVE"]
    matched_count: int = 0
    unmatched_count: int = 0
    mean_spatial_distance_m: Optional[float] = None
    note: Optional[str] = None
    # No lux-vs-relative RMSE; structural/pattern metrics documented explicitly
