"""Forecast contracts — TASK 030. Fixed model; snapshot/scenario; deterministic; no ranking."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime

class ForecastTarget(BaseModel):
    variable: str
    unit: str
    spatial_level: Optional[str] = None
    temporal_basis: Optional[str] = None

class ForecastRequest(BaseModel):
    forecast_id: str
    source_snapshot_ref: str
    scenario_ref: Optional[str] = None
    model_version_ref: str
    parameter_set_ref: str
    target_times: List[float] = Field(default_factory=list)
    targets: List[ForecastTarget] = Field(default_factory=list)
    initial_conditions_ref: Optional[str] = None
    deterministic: bool = True
    uncertainty_mode: Literal["NOT_MODELED","QUALITATIVE","QUANTIFIED"] = "NOT_MODELED"
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ForecastResult(BaseModel):
    forecast_id: str
    source_snapshot_ref: str
    scenario_ref: Optional[str] = None
    model_version_ref: str
    parameter_set_ref: str
    target_outputs: Dict[str, Any] = Field(default_factory=dict)
    target_times: List[float] = Field(default_factory=list)
    execution_status: Literal["COMPLETED","PARTIALLY_COMPUTABLE","NOT_COMPUTABLE","FAILED"] = "COMPLETED"
    computability_status: Literal["COMPUTABLE","PARTIALLY_COMPUTABLE","NOT_COMPUTABLE","INCONCLUSIVE"] = "COMPUTABLE"
    assumptions: List[str] = Field(default_factory=list)
    uncertainty_metadata: Optional[str] = None
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ModelCandidate(BaseModel):
    candidate_id: str
    model_version_ref: str
    parameter_set_ref: str
    description: Optional[str] = None
    provenance: Optional[str] = None
    calibration_reference: Optional[str] = None
    validation_reference: Optional[str] = None
    is_synthetic_example: bool = False

class ModelComparisonRequest(BaseModel):
    comparison_id: str
    candidates: List[ModelCandidate] = Field(default_factory=list)
    source_snapshot_ref: str
    scenario_ref: Optional[str] = None
    forecast_horizon_target_time: Optional[float] = None
    targets: List[ForecastTarget] = Field(default_factory=list)
    metric_config: List[Any] = Field(default_factory=list)
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class ModelComparisonResult(BaseModel):
    comparison_id: str
    candidate_results: List[Dict[str, Any]] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    comparability_status: Literal["COMPARABLE","INCOMPATIBLE","PARTIAL"] = "COMPARABLE"
    provenance: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","INCONCLUSIVE"] = "VALID"
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
