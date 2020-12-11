from piccolo.apps.migrations.auto import MigrationManager

ID = "2020-12-10T21:10:36"
VERSION = "0.14.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="forum")

    manager.drop_column(
        table_class_name="Topic", tablename="topic", column_name="description"
    )

    manager.rename_column(
        table_class_name="Topic",
        tablename="topic",
        old_column_name="title",
        new_column_name="subject",
    )

    return manager
