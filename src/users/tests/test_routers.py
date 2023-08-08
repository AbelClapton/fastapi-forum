from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)


def test_create_user():
    user = {"email": "random@email.com", "password": "randomstring"}

    response = client.post("/users/", json=user)
    assert response.status_code == 201
    print(response.json())
