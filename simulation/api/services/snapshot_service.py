"""Snapshot service — read-only checkpoint; immutable."""
from simulation.api.schemas.snapshot import SnapshotResponse

SYNTH_SNAPSHOT = SnapshotResponse(
    snapshot_id="snap-001",
    timestamp="2026-09-17T00:00:00Z",
    source_state_ref="garden-001",
    version="v1",
    schema_version="v1",
    provenance="TASK_040 synthetic fixture; immutable",
    status="VALID",
    notes="Checkpoint of current domain/application state.",
    is_immutable=True,
)

class SnapshotService:
    def __init__(self):
        self._store = [SYNTH_SNAPSHOT]
    def list_all(self):
        return list(self._store)
    def get_by_id(self, sid: str):
        for s in self._store:
            if s.snapshot_id == sid:
                return s
        return None

snapshot_service = SnapshotService()
