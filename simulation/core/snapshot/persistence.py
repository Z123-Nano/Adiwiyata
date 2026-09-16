"""Snapshot / Checkpoint persistence — JSON, deterministic, deep-boundary."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from simulation.core.snapshot.contracts import Snapshot, Checkpoint, ClockState, SchedulerState

class SnapshotRecord:
    def __init__(self, snapshots: Optional[List[Snapshot]] = None):
        self.snapshots = snapshots or []
    def add(self, s: Snapshot) -> None:
        # Deep boundary: serialize then parse to break mutable refs
        s = Snapshot.model_validate(s.model_dump())
        self.snapshots.append(s)
    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps([s.model_dump(mode="json") for s in self.snapshots], indent=2, default=str))
    @classmethod
    def from_json(cls, path: str | Path) -> "SnapshotRecord":
        data = json.loads(Path(path).read_text())
        return cls(snapshots=[Snapshot.model_validate(item) for item in data])

def save_checkpoint(snapshot: Snapshot, path: str | Path) -> None:
    cp = Checkpoint(**snapshot.model_dump(mode="json"))
    cp.is_checkpoint = True
    SnapshotRecord([cp]).to_json(path)

def load_checkpoint(path: str | Path) -> Checkpoint:
    rec = SnapshotRecord.from_json(path)
    for s in rec.snapshots:
        if s.is_checkpoint:
            return Checkpoint(**s.model_dump(mode="json"))
    raise ValueError("no checkpoint found")

def save_snapshot(snapshot: Snapshot, path: str | Path) -> None:
    SnapshotRecord([snapshot]).to_json(path)

def load_snapshot(path: str | Path) -> Snapshot:
    return SnapshotRecord.from_json(path).snapshots[0]
