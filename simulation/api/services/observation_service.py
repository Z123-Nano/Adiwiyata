"""Observation service — fixture/service-backed; no DB; deterministic."""
from typing import List, Optional
from simulation.core.measurements.fixtures import SYNTHETIC_OBSERVATIONS, SYNTH_PHENO_OBS, SYNTH_TRANSPLANT_OBS
from simulation.core.contracts.domain import Observation

class ObservationService:
    def __init__(self):
        self._store: List[Observation] = list(SYNTHETIC_OBSERVATIONS)
        if not self._store:
            self._store = [SYNTH_PHENO_OBS, SYNTH_TRANSPLANT_OBS]
        self._counter = len(self._store)

    def list_all(self) -> List[Observation]:
        return list(self._store)

    def get_by_id(self, observation_id: str) -> Optional[Observation]:
        for o in self._store:
            if o.id == observation_id:
                return o
        return None

    def create(self, observation: Observation) -> Observation:
        # Deterministic service-backed id (not hardcoded constant like "o_new")
        if not observation.id:
            observation.id = f"o-svc-{self._counter:03d}"
            self._counter += 1
        self._store.append(observation)
        return observation

observation_service = ObservationService()
