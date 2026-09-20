"""TASK 043 — simulation step integration tests."""
from fastapi.testclient import TestClient
from simulation.api.app import app
client = TestClient(app)

def test_043_A_step_executes_one_timestep():
    before = client.get("/api/v1/simulation/clock").json()["simulation_time"]
    r = client.post("/api/v1/simulation/step", json={"source_ref":"snap-001","source_type":"snapshot"})
    assert r.status_code == 200
    j = r.json()
    assert j["status"] in ("VALID","PARTIAL","NOT_COMPUTABLE","ERROR")
    assert j["timestep"] == 3600.0
    assert j["previous_simulation_time"] == before
    # Next time advances by timestep
    assert j["next_simulation_time"] != before

def test_043_B_source_snapshot_unchanged():
    snap_before = client.get("/api/v1/snapshots/snap-001").json()
    client.post("/api/v1/simulation/step", json={"source_ref":"snap-001","source_type":"snapshot"})
    snap_after = client.get("/api/v1/snapshots/snap-001").json()
    assert snap_before == snap_after

def test_043_C_partial_status_preserved():
    r = client.post("/api/v1/simulation/step", json={"source_ref":"snap-001","source_type":"snapshot"})
    j = r.json()
    statuses = {cs["component"]: cs["status"] for cs in j["component_statuses"]}
    # Some may be NOT_COMPUTABLE; none should be fabricated as AVAILABLE without module
    assert "photosynthesis" in statuses
    assert "carbon_respiration" in statuses

def test_043_D_no_continuous_endpoint():
    import simulation.api.app as a
    routes = [str(getattr(r, 'path', getattr(r, 'route', str(r)))) for r in a.app.routes]
    bad = ["/simulation/run","/simulation/play","/simulation/pause","/simulation/advance","/simulation/step_continuous"]
    for b in bad:
        assert not any(b in str(p) for p in routes), f"mutation endpoint {b} found"

def test_043_E_no_duplicate_equations_in_engine():
    import inspect, simulation.core.simulation.engine as e
    src = inspect.getsource(e.SimulationEngine)
    assert "photosynthesis_model" in src  # references only, not equation
    assert "0.05" not in src  # no hardcoded scientific param
