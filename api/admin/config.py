from piccolo_admin.endpoints import create_admin

from api.forum.tables import Category, Reply, Topic

ADMIN = create_admin(
    tables=[Category, Reply, Topic],
)
