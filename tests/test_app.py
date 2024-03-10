from fastapi.testclient import TestClient

from main import app


def test_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Piccolo headless forum"}
