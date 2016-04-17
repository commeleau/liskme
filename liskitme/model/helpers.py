from liskitme.model import DBSession


class BaseQuery:

    def __init__(self):
        pass

    @classmethod
    def query(cls):
        return DBSession.query(cls)

    @classmethod
    def all(cls):
        return cls.query().all()
