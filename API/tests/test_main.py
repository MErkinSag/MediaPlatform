from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_server_up():
    response = client.get("http://localhost:8000/")

    assert response.status_code == 200
    assert response.json() == {"msg": "server is up and running"}
