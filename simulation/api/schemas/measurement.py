"""Measurement / Observation schemas — TASK 037 DTO / response models."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MeasurementResponse(BaseModel):
    id: str
    timestamp: str  # ISO; preserved exactly
    variable: str
    value: float
    unit: str
    location_target_id: Optional[str] = None
    spatial_ref: Optional[dict] = None
    instrument: Optional[str] = None
    instrument_id: Optional[str] = None
    method: Optional[str] = None
    calibration_ref: Optional[str] = None
    observer_source: Optional[str] = None
    uncertainty: Optional[float] = None  # None preserved; never zero
    provenance: Optional[str] = None
    quality_flag: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    status: str = "VALID"

class MeasurementListResponse(BaseModel):
    measurements: List[MeasurementResponse]
    provenance: Optional[str] = None
    note: Optional[str] = None

class ObservationResponse(BaseModel):
    id: str
    timestamp: str
    target_id: Optional[str] = None
    observation_type: Optional[str] = None
    category: Optional[str] = None
    content: str
    structured_attributes: Optional[dict] = None
    value_numeric: Optional[float] = None
    unit: Optional[str] = None
    location_target_id: Optional[str] = None
    spatial_ref: Optional[dict] = None
    method: Optional[str] = None
    observer_source: Optional[str] = None
    uncertainty: Optional[float] = None
    notes: Optional[str] = None
    provenance: Optional[str] = None
    quality_flag: Optional[str] = None
    is_synthetic_example: bool = False
    status: str = "VALID"

class ObservationListResponse(BaseModel):
    observations: List[ObservationResponse]
    provenance: Optional[str] = None
    note: Optional[str] = None
