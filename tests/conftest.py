import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from piccolo.apps.user.tables import BaseUser
from piccolo.table import create_db_tables, drop_db_tables

from api.forum.tables import Category, Reply, Topic
from main import app

TABLES = [BaseUser, Category, Reply, Topic]


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(autouse=True)
async def test_db():
    await create_db_tables(*TABLES, if_not_exists=True)
    yield
    await drop_db_tables(*TABLES)


@pytest_asyncio.fixture()
async def create_test_data():
    user = BaseUser(
        username="testuser",
        email="testuser@user.com",
        password="testuser123",
        active=True,
    )
    await user.save()

    second_user = BaseUser(
        username="seconduser",
        email="seconduser@user.com",
        password="seconduser123",
        active=True,
    )
    await second_user.save()

    user = await BaseUser.select().first()

    first_category = Category(
        name="Test category one",
        description="Test category description one",
    )

    await first_category.save()

    second_category = Category(
        name="Test category two",
        description="Test category description two",
    )

    await second_category.save()

    category = await Category.select().first()

    first_topic = Topic(
        subject="Test topic one",
        category=category["id"],
        topic_user=user["id"],
    )

    await first_topic.save()

    second_topic = Topic(
        subject="Test topic two",
        category=category["id"],
        topic_user=user["id"],
    )

    await second_topic.save()

    first_reply = Reply(
        description="Reply description one",
        topic=first_topic["id"],
        reply_user=user["id"],
    )

    await first_reply.save()

    second_reply = Reply(
        description="Reply description two",
        topic=first_topic["id"],
        reply_user=user["id"],
    )

    await second_reply.save()


@pytest_asyncio.fixture()
async def create_access_token(async_client) -> str:
    payload = {
        "username": "testuser",
        "password": "testuser123",
    }

    response = await async_client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    access_token = response.json()["access_token"]
    return access_token
