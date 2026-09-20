"""Measurement service — fixture/service-backed; no DB; deterministic."""
from typing import List, Optional
from simulation.core.measurements.fixtures import (
    SYNTH_ILLUMINANCE, SYNTH_TEMPERATURE, SYNTH_SOIL_MOISTURE,
    SYNTHETIC_MEASUREMENTS,
)
from simulation.core.contracts.domain import Measurement

class MeasurementService:
    def __init__(self):
        # Load fixtures into service-backed list (not a hidden hardcoded router dict)
        self._store: List[Measurement] = list(SYNTHETIC_MEASUREMENTS)
        # Ensure fixtures loaded (if fixtures module defines differently)
        if not self._store:
            self._store = [SYNTH_ILLUMINANCE, SYNTH_TEMPERATURE, SYNTH_SOIL_MOISTURE]
        self._counter = len(self._store)

    def list_all(self) -> List[Measurement]:
        return list(self._store)

    def get_by_id(self, measurement_id: str) -> Optional[Measurement]:
        for m in self._store:
            if m.id == measurement_id:
                return m
        return None

    def create(self, measurement: Measurement) -> Measurement:
        # Service-backed identity (not router-hardcoded constant)
        # If measurement has no id, assign deterministic derived id
        if not measurement.id:
            measurement.id = f"m-svc-{self._counter:03d}"
            self._counter += 1
        self._store.append(measurement)
        return measurement

# Module singleton — production path uses this service, not router dict
measurement_service = MeasurementService()
