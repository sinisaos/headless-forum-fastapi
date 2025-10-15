import pytest


@pytest.mark.anyio
async def test_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Piccolo headless forum"}
