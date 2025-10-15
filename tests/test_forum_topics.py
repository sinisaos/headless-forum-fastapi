import pytest
from piccolo.apps.user.tables import BaseUser

from api.forum.tables import Category, Topic


@pytest.mark.anyio
async def test_get_all_topics(test_db, create_test_data, async_client):
    response = await async_client.get("/topics/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


@pytest.mark.anyio
async def test_get_single_topic(test_db, create_test_data, async_client):
    response = await async_client.get("/topics/1/")
    assert response.status_code == 200
    assert response.json()["subject"] == "Test topic one"


@pytest.mark.anyio
async def test_get_record_not_found(test_db, create_test_data, async_client):
    response = await async_client.get("/topics/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


@pytest.mark.anyio
async def test_create_topic(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    user = await BaseUser.select().first()
    category = await Category.select().first()

    payload = {
        "subject": "Test topic three",
        "created": "2024-03-10T16:38:01",
        "category": category["id"],
        "topic_user": user["id"],
    }
    response = await async_client.post(
        "/topics/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = await Topic.select(Topic.subject).where(
        Topic._meta.primary_key == response.json()[0]["id"]
    )
    assert response.status_code == 201
    assert result[0]["subject"] == "Test topic three"


@pytest.mark.anyio
async def test_update_topic(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "subject": "Updated test topic two",
    }
    response = await async_client.patch(
        "/topics/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = await async_client.get(
        "/topics/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["subject"] == "Updated test topic two"


@pytest.mark.anyio
async def test_update_record_not_found(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "name": "Updated test topic two",
    }

    response = await async_client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.anyio
async def test_delete_topic(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    response = await async_client.delete(
        "/topics/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_record_not_found(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    response = await async_client.delete(
        "/topics/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
