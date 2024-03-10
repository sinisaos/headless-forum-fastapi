"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig

from api.forum.tables import Category, Reply, Topic

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="forum",
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY,
        "piccolo_migrations",
    ),
    table_classes=[Category, Topic, Reply],
    migration_dependencies=[],
    commands=[],
)
