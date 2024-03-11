from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser

from api.forum.tables import Reply, Topic
from main import app


def test_get_all_replies(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/replies/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


def test_get_single_reply(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/replies/1/")
    assert response.status_code == 200
    assert response.json()["description"] == "Reply description one"


def test_get_record_not_found(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/replies/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


def test_create_replie(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    user = BaseUser.select().first().run_sync()
    topic = Topic.select().first().run_sync()

    payload = {
        "description": "Reply description three",
        "created": "2024-03-10T16:38:01",
        "topic": topic["id"],
        "reply_user": user["id"],
    }
    response = client.post(
        "/replies/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = (
        Reply.select(Reply.description)
        .where(Reply._meta.primary_key == response.json()[0]["id"])
        .run_sync()
    )
    assert response.status_code == 201
    assert result[0]["description"] == "Reply description three"


def test_update_reply(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    payload = {
        "description": "Updated reply description two",
    }
    response = client.patch(
        "/replies/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = client.get(
        "/replies/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Updated reply description two"


def test_update_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)

    payload = {
        "name": "Updated reply description two",
    }

    response = client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_delete_replie(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    response = client.delete(
        "/replies/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 204


def test_delete_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)
    response = client.delete(
        "/replies/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
