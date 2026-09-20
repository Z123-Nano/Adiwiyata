"""TASK 014 Snapshot router — read-only, immutable."""
from fastapi import APIRouter, HTTPException
from simulation.api.schemas.snapshot import SnapshotResponse
from simulation.api.services.snapshot_service import snapshot_service

router = APIRouter()

@router.get("/snapshots", response_model=list[SnapshotResponse])
def list_snapshots():
    return snapshot_service.list_all()

@router.get("/snapshots/{snapshot_id}", response_model=SnapshotResponse)
def get_snapshot(snapshot_id: str):
    s = snapshot_service.get_by_id(snapshot_id)
    if s is None:
        raise HTTPException(status_code=404, detail={"code":"NOT_FOUND","message":"Snapshot not found","id":snapshot_id})
    return s
