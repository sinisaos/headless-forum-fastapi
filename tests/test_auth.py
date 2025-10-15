import pytest


@pytest.mark.anyio
async def test_user_register(test_db, create_test_data, async_client):
    payload = {
        "username": "user",
        "email": "user@user.com",
        "password": "user123",
        "active": True,
    }

    response = await async_client.post(
        "/accounts/register/",
        json=payload,
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user"


@pytest.mark.anyio
async def test_register_failed(test_db, create_test_data, async_client):
    payload = {
        "username": "testuser",
        "email": "testuser@user.com",
        "password": "testuser123",
        "active": True,
    }

    response = await async_client.post(
        "/accounts/register/",
        json=payload,
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "User with that email or username already exists.",
    }


@pytest.mark.anyio
async def test_login(test_db, create_test_data, async_client):
    payload = {
        "username": "testuser",
        "password": "testuser123",
    }

    response = await async_client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_failed(test_db, create_test_data, async_client):
    payload = {
        "username": "wronguser",
        "password": "wronguser123",
    }

    response = await async_client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
