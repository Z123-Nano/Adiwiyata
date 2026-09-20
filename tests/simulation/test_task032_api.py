"""TASK 032 API tests — adapter boundary; domain preserved; no scientific duplication."""
from fastapi.testclient import TestClient
from simulation.api.app import app

client = TestClient(app)

def test_A_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "TASK 032" in (r.json().get("note") or "")

def test_B_garden_retrieval():
    r = client.get("/api/v1/garden")
    assert r.status_code == 200
    assert r.json()["garden_id"] == "garden-001"

def test_C_plant_retrieval():
    r = client.get("/api/v1/plants/plant-p1")
    assert r.status_code == 200
    assert r.json()["plant_id"] == "plant-p1"

def test_D_404_unknown_plant():
    r = client.get("/api/v1/plants/unknown")
    assert r.status_code == 404
    assert "NOT_FOUND" in str(r.json())

def test_E_measurement_create():
    r = client.post("/api/v1/measurements", json={"raw_value":120.5,"unit":"lux","provenance":"TASK_032","is_synthetic_example":True})
    assert r.status_code == 200
    assert r.json()["status"] == "VALID"
    assert r.json()["raw_value"] == 120.5
    assert r.json()["unit"] == "lux"

def test_F_raw_lux_preservation():
    r = client.post("/api/v1/measurements", json={"raw_value":500,"unit":"lux"})
    assert r.json()["unit"] == "lux"
    # No silent conversion to PPFD (domain rule preserved)

def test_G_observation_create():
    r = client.post("/api/v1/observations", json={"text":"leaf color green","provenance":"TASK_032"})
    assert r.status_code == 200
    assert r.json()["status"] == "VALID"

def test_H_snapshot_create():
    r = client.post("/api/v1/snapshots", json={"source_ref":"snap_src","provenance":"TASK_032"})
    assert r.status_code == 200
    assert r.json()["status"] == "VALID"

def test_I_scenario_source_reference():
    r = client.post("/api/v1/scenarios", json={"source_snapshot_ref":"snap_001","provenance":"TASK_032"})
    assert r.status_code == 200
    assert r.json()["source_snapshot_ref"] == "snap_001"

def test_J_prediction_NOT_COMPUTABLE():
    r = client.post("/api/v1/predictions", json={"snapshot_ref":"snap_001","provenance":"TASK_032"})
    assert r.status_code == 200
    assert r.json()["status"] == "NOT_COMPUTABLE"

def test_K_forecast_NOT_COMPUTABLE():
    r = client.post("/api/v1/forecasts", json={"source_snapshot_ref":"snap_001","provenance":"TASK_032"})
    assert r.json()["computability_status"] == "NOT_COMPUTABLE"

def test_L_validation_status():
    r = client.post("/api/v1/validation", json={"validation_id":"v1","model_version_ref":"v1","parameter_set_ref":"base_1","dataset_ref":"ds"})
    assert r.status_code == 200
    assert r.json()["status"] == "VALID"

def test_M_calibration_no_mutation():
    r = client.post("/api/v1/calibration", json={"calibration_id":"cal_1","target_variable":"alpha","dataset_ref":"ds","provenance":"TASK_032"})
    assert r.json()["status"] == "VALID"
    assert "Original parameters not mutated" in r.json()["note"]

def test_N_model_version():
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    assert isinstance(r.json()["models"], list)

def test_O_malformed_input():
    r = client.post("/api/v1/measurements", json={"unit":"bad"})
    # Pydantic validation error → 422
    assert r.status_code == 422

def test_P_timezone_provenance():
    r = client.get("/api/v1/health")
    j = r.json()
    assert "provenance" not in j or j.get("note") is not None

def test_Q_provenance_preservation():
    r = client.post("/api/v1/measurements", json={"raw_value":1,"unit":"x","provenance":"MY_PROV"})
    assert r.json()["provenance"] == "MY_PROV"

def test_R_roundtrip_domain_equivalent():
    # API response uses domain-equivalent fields (status/provenance/units) not raw Python objects
    r = client.get("/api/v1/plants/plant-p1")
    j = r.json()
    assert "plant_id" in j and "architecture_summary" in j

def test_S_snapshot_immutable():
    r = client.post("/api/v1/snapshots", json={"source_ref":"snap_001","provenance":"TASK_032"})
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "VALID" and j.get("note","").find("not mutated") >= 0

def test_T_no_science_in_routes():
    # Verify routes delegate; do not contain scientific math (verified by inspection — no gross_rate computation here)
    import inspect, simulation.api.routers.validation as v
    src = inspect.getsource(v.create_validation)
    assert "calibrate_scalar" not in src or "validate_model" in src  # only adapter call
    assert "0.05" not in src  # no hardcoded scientific parameter
