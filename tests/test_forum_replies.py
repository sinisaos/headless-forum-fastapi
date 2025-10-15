import pytest
from piccolo.apps.user.tables import BaseUser

from api.forum.tables import Reply, Topic


@pytest.mark.anyio
async def test_get_all_replies(
    test_db,
    create_test_data,
    async_client,
):
    response = await async_client.get("/replies/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


@pytest.mark.anyio
async def test_get_single_reply(
    test_db,
    create_test_data,
    async_client,
):
    response = await async_client.get("/replies/1/")
    assert response.status_code == 200
    assert response.json()["description"] == "Reply description one"


@pytest.mark.anyio
async def test_get_record_not_found(
    test_db,
    create_test_data,
    async_client,
):
    response = await async_client.get("/replies/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


@pytest.mark.anyio
async def test_create_replie(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    user = await BaseUser.select().first()
    topic = await Topic.select().first()

    payload = {
        "description": "Reply description three",
        "created": "2024-03-10T16:38:01",
        "topic": topic["id"],
        "reply_user": user["id"],
    }
    response = await async_client.post(
        "/replies/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = await Reply.select(Reply.description).where(
        Reply._meta.primary_key == response.json()[0]["id"]
    )
    assert response.status_code == 201
    assert result[0]["description"] == "Reply description three"


@pytest.mark.anyio
async def test_update_reply(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "description": "Updated reply description two",
    }
    response = await async_client.patch(
        "/replies/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = await async_client.get(
        "/replies/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Updated reply description two"


@pytest.mark.anyio
async def test_update_record_not_found(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "name": "Updated reply description two",
    }

    response = await async_client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.anyio
async def test_delete_replie(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    response = await async_client.delete(
        "/replies/2/",
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
        "/replies/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
