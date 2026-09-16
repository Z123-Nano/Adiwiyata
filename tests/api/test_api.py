from fastapi.testclient import TestClient
from api.src.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "hello" in r.json()["message"]
