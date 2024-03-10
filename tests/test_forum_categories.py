from fastapi.testclient import TestClient

from api.forum.tables import Category
from main import app


def test_get_all_categories(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


def test_get_single_category(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/categories/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test category one"


def test_get_record_not_found(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/categories/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


def test_create_category(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    payload = {
        "name": "Test category three",
        "description": "Test category description three",
    }
    response = client.post(
        "/categories/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = (
        Category.select(Category.name)
        .where(Category._meta.primary_key == response.json()[0]["id"])
        .run_sync()
    )
    assert response.status_code == 201
    assert result[0]["name"] == "Test category three"


def test_update_category(test_db, create_test_data, create_access_token):
    client = TestClient(app)

    payload = {
        "name": "Updated test category two",
    }
    response = client.patch(
        "/categories/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = client.get(
        "/categories/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated test category two"


def test_update_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)

    payload = {
        "name": "Updated test category two",
    }

    response = client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_delete_category(test_db, create_test_data, create_access_token):
    client = TestClient(app)
    response = client.delete(
        "/categories/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 204


def test_delete_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(app)
    response = client.delete(
        "/categories/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
