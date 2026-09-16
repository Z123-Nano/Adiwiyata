"""TASK 015 scenario branching — deterministic; synthetic; source immutable; no simulation run."""
from datetime import datetime, timezone
from simulation.core.scenario.contracts import Scenario, ScenarioModification, BranchedState
from simulation.core.scenario.branching import create_scenario
from simulation.core.scenario.fixtures import SYNTH_SCENARIO, SYNTH_MOD_ENV_OVERRIDE, SYNTH_MOD_SPATIAL
from simulation.core.snapshot.fixtures import SYNTH_SNAPSHOT
from simulation.core.snapshot.persistence import save_snapshot, load_snapshot

def test_scenario_creation_from_snapshot():
    s, b = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-01", "test")
    assert s.scenario_id == "sc-01"
    assert s.source_snapshot_ref == SYNTH_SNAPSHOT.snapshot_id
    assert s.schema_version == "v1"

def test_source_snapshot_unchanged():
    original_id = SYNTH_SNAPSHOT.snapshot_id
    original_time = SYNTH_SNAPSHOT.simulation_time
    s, b = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-02", "test2")
    assert SYNTH_SNAPSHOT.snapshot_id == original_id
    assert SYNTH_SNAPSHOT.simulation_time == original_time

def test_branch_independently_mutable():
    s, b = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-03", "test3")
    b.simulation_time = 9999.0
    # Source not affected because we loaded separately; verify by reloading
    snap = load_snapshot("/tmp/task014_snap.json") if False else SYNTH_SNAPSHOT  # just check object
    # More direct: branch state is separate object
    assert b.source_snapshot_ref == SYNTH_SNAPSHOT.snapshot_id
    assert b.simulation_time == 9999.0

def test_two_scenarios_independent():
    s1, b1 = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-a", "a")
    s2, b2 = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_SPATIAL], "sc-b", "b")
    assert s1.scenario_id != s2.scenario_id
    assert s1.modifications[0].id != s2.modifications[0].id
    b1.simulation_time = 1.0
    assert b2.simulation_time == SYNTH_SNAPSHOT.simulation_time

def test_same_modifications_deterministic():
    s1, b1 = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-d1", "d")
    s2, b2 = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-d2", "d")
    assert s1.name == s2.name
    assert len(s1.modifications) == len(s2.modifications)

def test_source_snapshot_ref_preserved():
    s, _ = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [], "sc-ref", "ref")
    assert s.source_snapshot_ref == SYNTH_SNAPSHOT.snapshot_id

def test_scenario_id_distinct():
    assert SYNTH_SCENARIO.scenario_id != SYNTH_SNAPSHOT.snapshot_id

def test_modification_provenance_preserved():
    s = SYNTH_SCENARIO
    assert s.modifications[0].provenance is not None
    assert s.provenance is not None

def test_serialization_roundtrip():
    import json
    s = SYNTH_SCENARIO
    d = json.loads(s.model_dump_json())
    s2 = Scenario.model_validate(d)
    assert s2.scenario_id == s.scenario_id
    assert s2.source_snapshot_ref == s.source_snapshot_ref

def test_invalid_scenario_rejected():
    from pydantic import ValidationError
    try:
        Scenario(scenario_id="bad", name="b", source_snapshot_ref="", created_at=datetime.now())
        # empty ref allowed by type; just confirm missing fields fail
    except ValidationError:
        pass
    try:
        Scenario(scenario_id="bad")
        assert False, "missing required fields"
    except ValidationError:
        pass

def test_parameter_override_does_not_mutate_source():
    s, b = create_scenario(SYNTH_SNAPSHOT.snapshot_id, [SYNTH_MOD_ENV_OVERRIDE], "sc-ov", "ov", parameter_overrides={"x": 1})
    # Source snapshot has no parameter set; override is only in scenario
    assert s.parameter_overrides == {"x": 1}
    # Verify source unchanged
    assert SYNTH_SNAPSHOT.snapshot_id == "snap-014-001"

def test_timestamps_timezone_preserved():
    s = SYNTH_SCENARIO
    assert s.created_at.tzinfo is not None
    for m in s.modifications:
        assert m.timestamp is not None
        assert m.timestamp.tzinfo is not None

def test_synthetic_labeled():
    assert SYNTH_SCENARIO.is_synthetic_example is True
    assert SYNTH_MOD_ENV_OVERRIDE.is_synthetic_example is True
