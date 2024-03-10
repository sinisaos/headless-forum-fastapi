from fastapi.testclient import TestClient

from main import app


def test_current_user(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    response = client.get(
        "/accounts/profile/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_current_user_topics(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    response = client.get(
        "/accounts/profile/topics/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()[0]["author"] == "testuser"
    assert len(response.json()[0]["topics"]) == 2


def test_current_user_replies(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    response = client.get(
        "/accounts/profile/replies/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()[0]["author"] == "testuser"
    assert len(response.json()[0]["replies"]) == 2
