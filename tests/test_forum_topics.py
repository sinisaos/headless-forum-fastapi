from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser

from api.forum.tables import Category, Topic
from main import app


def test_get_all_topics(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/topics/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


def test_get_single_topic(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/topics/1/")
    assert response.status_code == 200
    assert response.json()["subject"] == "Test topic one"


def test_get_record_not_found(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/topics/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


def test_create_topic(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    user = BaseUser.select().first().run_sync()
    category = Category.select().first().run_sync()

    payload = {
        "subject": "Test topic three",
        "created": "2024-03-10T16:38:01",
        "category": category["id"],
        "topic_user": user["id"],
    }
    response = client.post(
        "/topics/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = (
        Topic.select(Topic.subject)
        .where(Topic._meta.primary_key == response.json()[0]["id"])
        .run_sync()
    )
    assert response.status_code == 201
    assert result[0]["subject"] == "Test topic three"


def test_update_topic(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    payload = {
        "subject": "Updated test topic two",
    }
    response = client.patch(
        "/topics/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = client.get(
        "/topics/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["subject"] == "Updated test topic two"


def test_update_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)

    payload = {
        "name": "Updated test topic two",
    }

    response = client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_delete_topic(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    response = client.delete(
        "/topics/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 204


def test_delete_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)
    response = client.delete(
        "/topics/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
