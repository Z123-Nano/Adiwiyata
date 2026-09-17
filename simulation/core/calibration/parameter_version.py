"""Parameter-set version — TASK 028. Original immutable; calibrated derived."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any

class ParameterValue(BaseModel):
    name: str
    value: float
    unit: str
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class ParameterSetVersion(BaseModel):
    parameter_set_id: str
    version: Literal["base","calibrated"] = "base"
    model_version_ref: Optional[str] = None
    parameters: List[ParameterValue] = Field(default_factory=list)
    source_parameters: Optional[str] = None  # base set ref for calibrated
    calibration_ref: Optional[str] = None
    provenance: Optional[str] = None
    timestamp: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
