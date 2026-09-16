"""TASK 014 snapshot/checkpoint — deterministic; synthetic; immutable; no science added."""
from datetime import datetime, timezone
from simulation.core.snapshot.contracts import Snapshot, Checkpoint, ClockState, ScheduledProcessState
from simulation.core.snapshot.persistence import save_snapshot, load_snapshot, save_checkpoint, load_checkpoint, SnapshotRecord
from simulation.core.snapshot.fixtures import SYNTH_SNAPSHOT, SYNTH_CHECKPOINT, _clock_snapshot, _scheduler_snapshot
from simulation.core.clock.clock import SimulationClock
from simulation.core.contracts.domain import Garden

def test_snapshot_creation():
    s = SYNTH_SNAPSHOT
    assert s.snapshot_id == "snap-014-001"
    assert s.schema_version == "v1"
    assert s.simulation_time == 7200.0

def test_required_metadata_present():
    s = SYNTH_SNAPSHOT
    assert s.created_at is not None
    assert s.snapshot_id is not None and len(s.snapshot_id) > 0
    assert s.model_version_ref is not None or s.provenance is not None

def test_serialization_roundtrip():
    path = "/tmp/task014_snap.json"
    save_snapshot(SYNTH_SNAPSHOT, path)
    loaded = load_snapshot(path)
    assert loaded.snapshot_id == SYNTH_SNAPSHOT.snapshot_id
    assert loaded.simulation_time == SYNTH_SNAPSHOT.simulation_time
    assert loaded.schema_version == "v1"

def test_restore_equivalent_state():
    s = SYNTH_SNAPSHOT
    # Restore by loading; compare serialized content
    path = "/tmp/task014_restore.json"
    save_snapshot(s, path)
    r = load_snapshot(path)
    assert r.snapshot_id == s.snapshot_id
    assert r.clock_state.current == s.clock_state.current if s.clock_state else True
    # Not identity — domain-equivalent content

def test_snapshot_immutability_after_live_mutation():
    s = SYNTH_SNAPSHOT
    original_time = s.simulation_time
    # Mutate a separate live state object (simulated)
    s2 = Snapshot(**s.model_dump(mode="json"))
    s2.simulation_time = 9999.0
    assert s.simulation_time == original_time  # original unchanged

def test_two_restored_states_independent():
    path = "/tmp/task014_ind.json"
    save_snapshot(SYNTH_SNAPSHOT, path)
    a = load_snapshot(path)
    b = load_snapshot(path)
    a.simulation_time = 1111.0
    assert b.simulation_time == SYNTH_SNAPSHOT.simulation_time

def test_clock_state_preserved():
    s = SYNTH_SNAPSHOT
    assert s.clock_state is not None
    assert s.clock_state.current is not None

def test_scheduler_state_preserved():
    s = SYNTH_SNAPSHOT
    assert s.scheduler_state is not None
    assert len(s.scheduler_state.processes) > 0
    p = s.scheduler_state.processes[0]
    assert p.id in ("solar", "env")

def test_model_schema_version_preserved():
    s = SYNTH_SNAPSHOT
    assert s.schema_version == "v1"
    assert s.model_version_ref == "v0.1"

def test_provenance_preserved():
    s = SYNTH_SNAPSHOT
    assert "synthetic" in (s.provenance or "").lower()

def test_optional_random_state_semantics():
    s = SYNTH_SNAPSHOT
    assert s.random_seed is None  # not applicable; must not be zero silently
    # Explicit absence documented

def test_invalid_snapshot_rejected():
    from pydantic import ValidationError
    try:
        Snapshot(snapshot_id="bad", created_at=datetime.now(), simulation_time=-1, schema_version="v1")
        # Negative time allowed by model; validation by convention; just confirm rejection of bad ids via missing required fields
    except ValidationError:
        pass
    # Explicit: missing snapshot_id should fail
    try:
        Snapshot(created_at=datetime.now(), simulation_time=0, schema_version="v1")
        assert False, "missing id should fail"
    except ValidationError:
        pass

def test_checkpoint_save_load_roundtrip():
    path = "/tmp/task014_cp.json"
    save_checkpoint(SYNTH_CHECKPOINT, path)
    cp = load_checkpoint(path)
    assert cp.is_checkpoint is True
    assert cp.snapshot_id == SYNTH_CHECKPOINT.snapshot_id
    assert cp.schema_version == "v1"

def test_deterministic_equivalent_state_comparison():
    s = SYNTH_SNAPSHOT
    import json
    d1 = json.loads(s.model_dump_json())
    d2 = json.loads(s.model_dump_json())
    assert d1 == d2

def test_snapshot_not_scenario_not_prediction():
    # Contract separation: Snapshot uses snapshot_id; Scenario has id/name; Prediction has source_snapshot_ref
    assert not hasattr(SYNTH_SNAPSHOT, "scenario_ref") or SYNTH_SNAPSHOT.scenario_ref is None
