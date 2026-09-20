"""Validation contracts — TASK 029. Independent dataset; fixed model; metrics; criteria; no calibration."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime

class MetricCriterion(BaseModel):
    metric_name: Literal["mae","rmse","bias","correlation","count"] = "mae"
    max_allowed_error: Optional[float] = None
    min_required_value: Optional[float] = None
    unit: Optional[str] = None
    interpretation: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ValidationDataset(BaseModel):
    dataset_id: str
    role: Literal["calibration","validation","excluded"] = "validation"
    observation_refs: List[str] = Field(default_factory=list)
    variable: str
    unit: str
    spatial_scope: Optional[str] = None
    temporal_scope: Optional[str] = None
    model_reference: Optional[str] = None
    parameter_set_reference: Optional[str] = None
    provenance: Optional[str] = None
    version: Literal["v1"] = "v1"
    independence_notes: Optional[str] = None
    inclusion_status: Literal["included","excluded"] = "included"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ValidationRequest(BaseModel):
    validation_id: str
    model_version_ref: str
    parameter_set_ref: str
    validation_dataset_ref: str
    target_quantity: str
    target_unit: str
    matching_rules: Optional[Dict[str, Any]] = None
    metric_config: List[MetricCriterion] = Field(default_factory=list)
    uncertainty_weighting: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ValidationResult(BaseModel):
    validation_id: str
    model_version_ref: str
    parameter_set_ref: str
    dataset_ref: str
    matched_count: int = 0
    unmatched_count: int = 0
    exclusions: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    criteria_met: Dict[str, Any] = Field(default_factory=dict)
    status: Literal["VALID","INVALID_INPUT","INSUFFICIENT_DATA","LEAKAGE_DETECTED","UNIT_MISMATCH","NOT_COMPUTABLE","INCONCLUSIVE"] = "VALID"
    provenance: Optional[str] = None
    timestamp: Optional[datetime] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ValidationMatch(BaseModel):
    case_id: str
    selected_sample: Optional[Any] = None
    spatial_distance_m: float = Field(default=float('inf'))
    matching_rule: Literal["nearest_within_threshold","nearest_beyond_threshold","unmatched","exact"] = "unmatched"
    accepted: bool = False
    reason: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
