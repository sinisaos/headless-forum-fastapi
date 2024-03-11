from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser
from piccolo.table import create_db_tables_sync, drop_db_tables_sync

from api.forum.tables import Category, Reply, Topic
from main import app
from tests.piccolo_conf_test import DB

TABLES = [BaseUser, Category, Topic, Reply]


@pytest.fixture(autouse=True)
def test_db():
    db_path = Path(DB.path)
    for _table in TABLES:
        _table._meta._db = DB
    create_db_tables_sync(*TABLES, if_not_exists=True)
    yield
    drop_db_tables_sync(*TABLES)
    db_path.unlink()


@pytest.fixture
def create_test_data():
    user = BaseUser(
        username="testuser",
        email="testuser@user.com",
        password="testuser123",
        active=True,
    )
    user.save().run_sync()

    second_user = BaseUser(
        username="seconduser",
        email="seconduser@user.com",
        password="seconduser123",
        active=True,
    )
    second_user.save().run_sync()

    user = BaseUser.select().first().run_sync()

    first_category = Category(
        name="Test category one",
        description="Test category description one",
    )

    first_category.save().run_sync()

    second_category = Category(
        name="Test category two",
        description="Test category description two",
    )

    second_category.save().run_sync()

    category = Category.select().first().run_sync()

    first_topic = Topic(
        subject="Test topic one",
        category=category["id"],
        topic_user=user["id"],
    )

    first_topic.save().run_sync()

    second_topic = Topic(
        subject="Test topic two",
        category=category["id"],
        topic_user=user["id"],
    )

    second_topic.save().run_sync()

    first_reply = Reply(
        description="Reply description one",
        topic=first_topic["id"],
        reply_user=user["id"],
    )

    first_reply.save().run_sync()

    second_reply = Reply(
        description="Reply description two",
        topic=first_topic["id"],
        reply_user=user["id"],
    )

    second_reply.save().run_sync()


@pytest.fixture
def create_access_token() -> str:
    client = TestClient(app)
    payload = {
        "username": "testuser",
        "password": "testuser123",
    }

    response = client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    access_token = response.json()["access_token"]
    return access_token
