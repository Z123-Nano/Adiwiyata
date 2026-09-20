"""Scenario service — branch from Snapshot; source unchanged; overrides explicit."""
from simulation.api.schemas.scenario import ScenarioResponse
from simulation.api.services.snapshot_service import snapshot_service

class ScenarioService:
    def __init__(self):
        self._store = [
            ScenarioResponse(
                scenario_id="scen-001",
                source_snapshot_id="snap-001",
                status="VALID",
                provenance="TASK_040 derived from snap-001; overrides explicit; source unchanged",
                overrides={"note": "example override category only; no biological mutation"},
                notes="Scenario branch; snapshot source preserved.",
                is_derived=True,
            ),
        ]
    def list_all(self):
        return list(self._store)
    def get_by_id(self, sid: str):
        for s in self._store:
            if s.scenario_id == sid:
                return s
        return None
    def create_from_snapshot(self, source_snapshot_id: str, overrides: dict = None):
        src = snapshot_service.get_by_id(source_snapshot_id)
        if src is None:
            return None
        # Source snapshot NOT mutated; new independent scenario
        new_id = f"scen-{len(self._store)+1:03d}"
        s = ScenarioResponse(
            scenario_id=new_id,
            source_snapshot_id=source_snapshot_id,
            status="VALID",
            provenance=f"TASK_040 branch from {source_snapshot_id}; source unchanged",
            overrides=overrides or {},
            notes="Created from snapshot; immutable source preserved.",
            is_derived=True,
        )
        self._store.append(s)
        return s

scenario_service = ScenarioService()
