"""Synthetic scenario fixtures — TASK 015. Labeled; source snapshot unchanged."""
from datetime import datetime, timezone
from simulation.core.scenario.contracts import Scenario, ScenarioModification
from simulation.core.snapshot.fixtures import SYNTH_SNAPSHOT
from simulation.core.snapshot.persistence import save_snapshot
from simulation.core.snapshot.persistence import save_snapshot, load_snapshot

SYNTH_MOD_ENV_OVERRIDE = ScenarioModification(
    id="mod-001",
    target_id="env-01",
    modification_type="environment_override",
    payload={"temperature_c": 25.0},  # config, not calibrated science
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="synthetic_example_TASK_015; not calibrated; override only",
    is_synthetic_example=True,
)

SYNTH_MOD_SPATIAL = ScenarioModification(
    id="mod-002",
    target_id="rack-1",
    modification_type="spatial_metadata",
    payload={"note": "hypothetical relocation"},
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="synthetic_example_TASK_015",
    is_synthetic_example=True,
)

SYNTH_SCENARIO = Scenario(
    # Save synthetic snapshot to file so string refs resolve
    scenario_id="scen-015-001",
    name="What-if warmer day",
    description="Hypothetical branch from snapshot snap-014-001 with environment override.",
    source_snapshot_ref=SYNTH_SNAPSHOT.snapshot_id,
    created_at=datetime(2026,6,21,12,30,0,tzinfo=timezone.utc),
    schema_version="v1",
    modifications=[SYNTH_MOD_ENV_OVERRIDE, SYNTH_MOD_SPATIAL],
    parameter_overrides={"temperature_baseline_c": 25.0},
    provenance="synthetic_scenario_TASK_015",
    is_synthetic_example=True,
)
save_snapshot(SYNTH_SNAPSHOT, "/tmp/snap-014-001.json")
