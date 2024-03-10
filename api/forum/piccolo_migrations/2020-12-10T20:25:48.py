from piccolo.apps.migrations.auto import MigrationManager

ID = "2020-12-10T20:25:48"
VERSION = "0.14.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="forum")

    manager.add_table("Category", tablename="category")

    manager.add_column(
        table_class_name="Category",
        tablename="category",
        column_name="name",
        column_class_name="Varchar",
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Category",
        tablename="category",
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

    return manager
