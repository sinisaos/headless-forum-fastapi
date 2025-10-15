import pytest

from api.forum.tables import Category


@pytest.mark.anyio
async def test_get_all_categories(test_db, create_test_data, async_client):
    response = await async_client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


@pytest.mark.anyio
async def test_get_single_category(test_db, create_test_data, async_client):
    response = await async_client.get("/categories/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test category one"


@pytest.mark.anyio
async def test_get_record_not_found(test_db, create_test_data, async_client):
    response = await async_client.get("/categories/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


@pytest.mark.anyio
async def test_create_category(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "name": "Test category three",
        "description": "Test category description three",
    }
    response = await async_client.post(
        "/categories/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    result = await Category.select(Category.name).where(
        Category._meta.primary_key == response.json()[0]["id"]
    )
    assert response.status_code == 201
    assert result[0]["name"] == "Test category three"


@pytest.mark.anyio
async def test_update_category(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "name": "Updated test category two",
    }
    response = await async_client.patch(
        "/categories/2/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200

    response = await async_client.get(
        "/categories/2/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated test category two"


@pytest.mark.anyio
async def test_update_record_not_found(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    payload = {
        "name": "Updated test category two",
    }

    response = await async_client.put(
        "/answers/10/",
        json=payload,
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.anyio
async def test_delete_category(
    test_db,
    create_test_data,
    create_access_token,
    async_client,
):
    response = await async_client.delete(
        "/categories/2/",
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
        "/categories/10/",
        headers={"Authorization": f"Bearer {create_access_token}"},
    )
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
