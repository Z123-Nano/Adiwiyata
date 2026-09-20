"""TASK 037 — measurement endpoint backed by service + fixtures (not hardcoded dict)."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from simulation.api.schemas.measurement import MeasurementResponse, MeasurementListResponse
from simulation.api.services.measurement_service import measurement_service
from simulation.core.contracts.domain import Measurement

router = APIRouter()

@router.get("/measurements", response_model=MeasurementListResponse)
def list_measurements():
    fixtures = measurement_service.list_all()
    items = []
    for f in fixtures:
        items.append(MeasurementResponse(
            id=f.id,
            timestamp=f.timestamp.isoformat() if hasattr(f.timestamp, "isoformat") else str(f.timestamp),
            variable=f.variable,
            value=f.value,
            unit=f.unit,
            location_target_id=f.location_target_id,
            spatial_ref=f.spatial_ref,
            instrument=f.instrument,
            instrument_id=f.instrument_id,
            method=f.method,
            calibration_ref=f.calibration_ref,
            observer_source=f.observer_source,
            uncertainty=f.uncertainty,
            provenance=f.provenance,
            quality_flag=f.quality_flag,
            notes=f.notes,
            is_synthetic_example=f.is_synthetic_example,
            status="VALID",
        ))
    return MeasurementListResponse(
        measurements=items,
        provenance="TASK_037 domain fixtures via measurement_service",
        note="Lux preserved; uncertainty=None preserved; synthetic fixtures labeled.",
    )

@router.get("/measurements/{measurement_id}", response_model=MeasurementResponse)
def get_measurement(measurement_id: str):
    m = measurement_service.get_by_id(measurement_id)
    if m is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Measurement not found","id":measurement_id})
    return MeasurementResponse(
        id=m.id,
        timestamp=m.timestamp.isoformat() if hasattr(m.timestamp, "isoformat") else str(m.timestamp),
        variable=m.variable,
        value=m.value,
        unit=m.unit,
        location_target_id=m.location_target_id,
        spatial_ref=m.spatial_ref,
        instrument=m.instrument,
        instrument_id=m.instrument_id,
        method=m.method,
        calibration_ref=m.calibration_ref,
        observer_source=m.observer_source,
        uncertainty=m.uncertainty,
        provenance=m.provenance,
        quality_flag=m.quality_flag,
        notes=m.notes,
        is_synthetic_example=m.is_synthetic_example,
        status="VALID",
    )

class MeasurementCreateIn(BaseModel):
    variable: str
    value: float
    unit: str
    location_target_id: str | None = None
    spatial_ref: dict | None = None
    instrument: str | None = None
    method: str | None = None
    observer_source: str | None = None
    uncertainty: float | None = None
    provenance: str | None = None
    notes: str | None = None
    is_synthetic_example: bool = False

@router.post("/measurements", response_model=MeasurementResponse)
def create_measurement(m_in: MeasurementCreateIn):
    # Service-backed creation with deterministic identity (not constant "m_new")
    m = Measurement(
        id="",  # service assigns
        timestamp=datetime.now(timezone.utc),
        variable=m_in.variable,
        value=m_in.value,
        unit=m_in.unit,
        location_target_id=m_in.location_target_id,
        spatial_ref=m_in.spatial_ref,
        instrument=m_in.instrument,
        method=m_in.method,
        observer_source=m_in.observer_source,
        uncertainty=m_in.uncertainty,
        provenance=m_in.provenance or "TASK_037 service",
        notes=m_in.notes,
        is_synthetic_example=m_in.is_synthetic_example,
    )
    created = measurement_service.create(m)
    return MeasurementResponse(
        id=created.id,
        timestamp=created.timestamp.isoformat() if hasattr(created.timestamp, "isoformat") else str(created.timestamp),
        variable=created.variable,
        value=created.value,
        unit=created.unit,
        location_target_id=created.location_target_id,
        spatial_ref=created.spatial_ref,
        instrument=created.instrument,
        instrument_id=created.instrument_id,
        method=created.method,
        calibration_ref=created.calibration_ref,
        observer_source=created.observer_source,
        uncertainty=created.uncertainty,
        provenance=created.provenance,
        quality_flag=created.quality_flag,
        notes=created.notes,
        is_synthetic_example=created.is_synthetic_example,
        status="VALID",
    )
