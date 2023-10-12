from fastapi.testclient import TestClient

from .main import app
import json

client = TestClient(app)


def test_get_clients():
    response = client.get("/clients/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) == list

