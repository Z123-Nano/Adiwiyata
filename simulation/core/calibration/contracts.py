"""Calibration contracts — TASK 028. Parameter-estimation framework; synthetic; no validation claim."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime

class CalibrationDataset(BaseModel):
    dataset_id: str
    observation_refs: List[str] = Field(default_factory=list)
    variable: str
    unit: str
    spatial_ref: Optional[str] = None
    temporal_ref: Optional[str] = None
    source_provenance: Optional[str] = None
    version: Literal["v1"] = "v1"
    inclusion_status: Literal["calibration","validation","excluded"] = "calibration"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class CalibrationRequest(BaseModel):
    calibration_id: str
    model_version_ref: str
    base_parameter_set_ref: str
    target_parameter_names: List[str] = Field(default_factory=list)
    observation_dataset_ref: str
    calibration_dataset_ref: Optional[str] = None
    objective: Literal["sum_sq_residuals","weighted_sum_sq","mae"] = "sum_sq_residuals"
    method: Literal["scipy_minimize_l_bfgs_b","bounded_grid","least_squares"] = "scipy_minimize_l_bfgs_b"
    bounds: Dict[str, Any] = Field(default_factory=dict)  # param -> [lower, upper]
    weighting: Optional[str] = None  # "equal","uncertainty"; documented
    seed: Optional[int] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class FittedParameter(BaseModel):
    parameter_name: str
    base_value: float
    fitted_value: float
    unit: str
    bounds: List[float] = Field(default_factory=list)
    method_ref: str
    objective_value: float
    status: Literal["VALID","CONVERGED","NOT_CONVERGED","NOT_IDENTIFIABLE","INCONCLUSIVE","INVALID_INPUT"] = "VALID"
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class CalibrationResult(BaseModel):
    calibration_id: str
    model_version_ref: str
    base_parameter_set_ref: str
    calibrated_parameter_set_ref: Optional[str] = None
    fitted_parameters: List[FittedParameter] = Field(default_factory=list)
    objective_value: float
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    observations_used: int
    exclusions: List[str] = Field(default_factory=list)
    status: Literal["VALID","CONVERGED","NOT_CONVERGED","NOT_IDENTIFIABLE","INSUFFICIENT_DATA","INCONCLUSIVE","INVALID_INPUT"] = "VALID"
    provenance: Optional[str] = None
    timestamp: Optional[datetime] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
