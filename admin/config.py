from piccolo_admin.endpoints import create_admin

from forum.tables import Category, Reply, Topic

ADMIN = create_admin(
    tables=[Category, Reply, Topic],
)
