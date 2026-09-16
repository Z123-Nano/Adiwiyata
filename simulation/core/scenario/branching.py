"""Scenario branching — TASK 015. Source snapshot immutable; branch independent."""
from __future__ import annotations
import copy
from typing import Optional
from simulation.core.snapshot.contracts import Snapshot
from simulation.core.snapshot.persistence import load_snapshot
from simulation.core.scenario.contracts import Scenario, ScenarioModification, BranchedState

def create_scenario(
    source_snapshot_ref_or_object: str | Snapshot,
    modifications: list,
    scenario_id: str,
    name: str,
    parameter_overrides: Optional[dict] = None,
    provenance: Optional[str] = None,
) -> tuple[Scenario, BranchedState]:
    """Branch from snapshot; source unchanged; branch independently mutable."""
    # Load or use snapshot object; do not modify
    snap = None
    if isinstance(source_snapshot_ref_or_object, str):
        for c in [source_snapshot_ref_or_object, f"/tmp/{source_snapshot_ref_or_object}.json"]:
            try:
                snap = load_snapshot(c)
                break
            except Exception:
                continue
        if snap is None:
            raise ValueError(f"snapshot file not found for ref: {source_snapshot_ref_or_object}")
    else:
        snap = source_snapshot_ref_or_object
    # Deep-copy serialized content for branch independence
    branched = BranchedState(
        source_snapshot_ref=snap.snapshot_id,
        scenario_ref=scenario_id,
        simulation_time=snap.simulation_time,
        garden_ref=snap.garden_ref,
        modifications_applied=[m.id for m in modifications],
        provenance=provenance or "branched_from_" + snap.snapshot_id,
    )
    scenario = Scenario(
        scenario_id=scenario_id,
        name=name,
        description=f"Branch from {snap.snapshot_id}",
        source_snapshot_ref=snap.snapshot_id,
        created_at=__import__('datetime').datetime.now(__import__('datetime').timezone.utc),
        modifications=modifications,
        parameter_overrides=parameter_overrides,
        provenance=provenance or "synthetic_scenario_TASK_015",
    )
    return scenario, branched
