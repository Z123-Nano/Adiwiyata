"""TASK 037 — observation endpoint backed by service + fixtures (no hardcoded constant)."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from simulation.api.schemas.measurement import ObservationResponse, ObservationListResponse
from simulation.api.services.observation_service import observation_service
from simulation.core.contracts.domain import Observation

router = APIRouter()

@router.get("/observations", response_model=ObservationListResponse)
def list_observations():
    fixtures = observation_service.list_all()
    items = []
    for f in fixtures:
        items.append(ObservationResponse(
            id=f.id,
            timestamp=f.timestamp.isoformat() if hasattr(f.timestamp, "isoformat") else str(f.timestamp),
            target_id=f.target_id,
            observation_type=f.observation_type,
            category=f.category,
            content=f.content,
            structured_attributes=f.structured_attributes,
            value_numeric=f.value_numeric,
            unit=f.unit,
            location_target_id=f.location_target_id,
            spatial_ref=f.spatial_ref,
            method=f.method,
            observer_source=f.observer_source,
            uncertainty=f.uncertainty,
            notes=f.notes,
            provenance=f.provenance,
            quality_flag=f.quality_flag,
            is_synthetic_example=f.is_synthetic_example,
            status="VALID",
        ))
    return ObservationListResponse(
        observations=items,
        provenance="TASK_037 domain fixtures via observation_service",
        note="Observation preserved separately from measurement; no inference to biology.",
    )

@router.get("/observations/{observation_id}", response_model=ObservationResponse)
def get_observation(observation_id: str):
    o = observation_service.get_by_id(observation_id)
    if o is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Observation not found","id":observation_id})
    return ObservationResponse(
        id=o.id,
        timestamp=o.timestamp.isoformat() if hasattr(o.timestamp, "isoformat") else str(o.timestamp),
        target_id=o.target_id,
        observation_type=o.observation_type,
        category=o.category,
        content=o.content,
        structured_attributes=o.structured_attributes,
        value_numeric=o.value_numeric,
        unit=o.unit,
        location_target_id=o.location_target_id,
        spatial_ref=o.spatial_ref,
        method=o.method,
        observer_source=o.observer_source,
        uncertainty=o.uncertainty,
        notes=o.notes,
        provenance=o.provenance,
        quality_flag=o.quality_flag,
        is_synthetic_example=o.is_synthetic_example,
        status="VALID",
    )

class ObservationCreateIn(BaseModel):
    content: str
    target_id: str | None = None
    observation_type: str | None = None
    category: str | None = None
    structured_attributes: dict | None = None
    value_numeric: float | None = None
    unit: str | None = None
    location_target_id: str | None = None
    spatial_ref: dict | None = None
    method: str | None = None
    observer_source: str | None = None
    uncertainty: float | None = None
    notes: str | None = None
    provenance: str | None = None
    is_synthetic_example: bool = False

@router.post("/observations", response_model=ObservationResponse)
def create_observation(o_in: ObservationCreateIn):
    # Service-backed identity (not hardcoded "o_new")
    o = Observation(
        id="",
        timestamp=datetime.now(timezone.utc),
        target_id=o_in.target_id,
        observation_type=o_in.observation_type,
        category=o_in.category,
        content=o_in.content,
        structured_attributes=o_in.structured_attributes,
        value_numeric=o_in.value_numeric,
        unit=o_in.unit,
        location_target_id=o_in.location_target_id,
        spatial_ref=o_in.spatial_ref,
        method=o_in.method,
        observer_source=o_in.observer_source,
        uncertainty=o_in.uncertainty,
        notes=o_in.notes,
        provenance=o_in.provenance or "TASK_037 service",
        is_synthetic_example=o_in.is_synthetic_example,
    )
    created = observation_service.create(o)
    return ObservationResponse(
        id=created.id,
        timestamp=created.timestamp.isoformat() if hasattr(created.timestamp, "isoformat") else str(created.timestamp),
        target_id=created.target_id,
        observation_type=created.observation_type,
        category=created.category,
        content=created.content,
        structured_attributes=created.structured_attributes,
        value_numeric=created.value_numeric,
        unit=created.unit,
        location_target_id=created.location_target_id,
        spatial_ref=created.spatial_ref,
        method=created.method,
        observer_source=created.observer_source,
        uncertainty=created.uncertainty,
        notes=created.notes,
        provenance=created.provenance,
        quality_flag=created.quality_flag,
        is_synthetic_example=created.is_synthetic_example,
        status="VALID",
    )
