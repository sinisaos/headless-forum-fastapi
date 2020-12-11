from piccolo.apps.user.tables import BaseUser
from piccolo.columns import ForeignKey, Text, Timestamp, Varchar
from piccolo.columns.readable import Readable
from piccolo.table import Table


class Category(Table):
    """
    An Category table.
    """

    name = Varchar()
    description = Text()

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Topic(Table):
    """
    An Topic table.
    """

    subject = Varchar()
    created = Timestamp()
    category = ForeignKey(references=Category)
    topic_user = ForeignKey(references=BaseUser)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.subject])


class Reply(Table):
    """
    An Reply table.
    """

    description = Text()
    created = Timestamp()
    topic = ForeignKey(references=Topic)
    reply_user = ForeignKey(references=BaseUser)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.topic])
