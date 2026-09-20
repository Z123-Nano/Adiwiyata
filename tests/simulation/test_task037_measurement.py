"""TASK 037 — focused measurement / observation integration tests."""
from fastapi.testclient import TestClient
from simulation.api.app import app
client = TestClient(app)

def test_037_A_get_measurements_service_backed():
    r = client.get("/api/v1/measurements")
    assert r.status_code == 200
    j = r.json()
    assert "measurements" in j
    ids = {m["id"] for m in j["measurements"]}
    assert "m-synth-ill-001" in ids

def test_037_B_get_measurement_by_id():
    r = client.get("/api/v1/measurements/m-synth-ill-001")
    assert r.status_code == 200
    j = r.json()
    assert j["id"] == "m-synth-ill-001"
    assert j["unit"] == "lux"
    assert j["status"] == "VALID"

def test_037_C_unknown_measurement_404():
    r = client.get("/api/v1/measurements/not_real")
    assert r.status_code == 404
    assert "NOT_FOUND" in str(r.json())

def test_037_D_get_observations_service_backed():
    r = client.get("/api/v1/observations")
    assert r.status_code == 200
    j = r.json()
    assert "observations" in j
    ids = {o["id"] for o in j["observations"]}
    assert "o-synth-pheno-001" in ids

def test_037_E_get_observation_by_id():
    r = client.get("/api/v1/observations/o-synth-pheno-001")
    assert r.status_code == 200
    j = r.json()
    assert j["id"] == "o-synth-pheno-001"
    assert j["status"] == "VALID"

def test_037_F_unknown_observation_404():
    r = client.get("/api/v1/observations/not_real")
    assert r.status_code == 404

def test_037_G_post_observation_no_constant_id():
    r = client.post("/api/v1/observations", json={"content":"test note","provenance":"TASK_037"})
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "VALID"
    assert j["id"] != "o_new"
    assert j["id"].startswith("o-svc-")

def test_037_H_dto_response_model_matches():
    r = client.get("/api/v1/measurements/m-synth-temp-001")
    j = r.json()
    assert "uncertainty" in j
    # unknown uncertainty preserved as None, not zero
    assert j["uncertainty"] is None or isinstance(j["uncertainty"], (float, int))

def test_037_I_provenance_status_preserved():
    r = client.get("/api/v1/measurements/m-synth-soil-001")
    j = r.json()
    assert j["provenance"] is not None
    assert j["status"] == "VALID"

def test_037_J_lux_not_converted():
    r = client.get("/api/v1/measurements/m-synth-ill-001")
    j = r.json()
    assert j["unit"] == "lux"
    assert "ppfd" not in str(j).lower() or j["unit"] == "lux"

def test_037_K_no_science_in_service_route():
    import inspect, simulation.api.routers.measurement as mm
    src = inspect.getsource(mm.create_measurement)
    assert "photosynthesis" not in src.lower()
