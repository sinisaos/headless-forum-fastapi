from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table


class BaseUser(Table, tablename="piccolo_user"):
    pass


class Topic(Table, tablename="topic"):
    pass


ID = "2020-12-10T20:27:25"
VERSION = "0.14.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="forum")

    manager.add_table("Reply", tablename="reply")

    manager.add_column(
        table_class_name="Reply",
        tablename="reply",
        column_name="description",
        column_class_name="Text",
        params={
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Reply",
        tablename="reply",
        column_name="created",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Reply",
        tablename="reply",
        column_name="topic",
        column_class_name="ForeignKey",
        params={
            "references": Topic,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Reply",
        tablename="reply",
        column_name="reply_user",
        column_class_name="ForeignKey",
        params={
            "references": BaseUser,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    return manager
