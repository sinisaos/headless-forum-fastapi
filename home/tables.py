from piccolo.columns import Boolean, Varchar
from piccolo.table import Table


class Task(Table):
    """
    An example table.
    """

    name = Varchar()
    completed = Boolean(default=False)
