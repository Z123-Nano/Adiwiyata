"""Measurement / Observation persistence — TASK 012.
Human-readable JSON serialization; raw preservation; no DB dependency.
Synthetic fixtures must set is_synthetic_example=True.
No calibration / validation / conversion (lux stays lux).
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from simulation.core.contracts.domain import Measurement, Observation

class MeasurementRecord:
    def __init__(self, measurements: Optional[List[Measurement]] = None):
        self.measurements = measurements or []
    def add(self, m: Measurement) -> None:
        self.measurements.append(m)
    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps([m.model_dump() for m in self.measurements], indent=2, default=str))
    @classmethod
    def from_json(cls, path: str | Path) -> "MeasurementRecord":
        data = json.loads(Path(path).read_text())
        return cls(measurements=[Measurement.model_validate(item) for item in data])
    def by_variable(self, variable: str) -> List[Measurement]:
        return [m for m in self.measurements if m.variable == variable]

class ObservationRecord:
    def __init__(self, observations: Optional[List[Observation]] = None):
        self.observations = observations or []
    def add(self, o: Observation) -> None:
        self.observations.append(o)
    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps([o.model_dump() for o in self.observations], indent=2, default=str))
    @classmethod
    def from_json(cls, path: str | Path) -> "ObservationRecord":
        data = json.loads(Path(path).read_text())
        return cls(observations=[Observation.model_validate(item) for item in data])

def save_measurements(measurements: List[Measurement], path: str | Path) -> None:
    MeasurementRecord(measurements).to_json(path)

def load_measurements(path: str | Path) -> List[Measurement]:
    return MeasurementRecord.from_json(path).measurements

def save_observations(observations: List[Observation], path: str | Path) -> None:
    ObservationRecord(observations).to_json(path)

def load_observations(path: str | Path) -> List[Observation]:
    return ObservationRecord.from_json(path).observations
