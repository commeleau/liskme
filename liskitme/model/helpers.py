from liskitme import DBSession


class BaseQuery:
    """
    I hate to use session manually...
    """
    def __init__(self):
        pass

    @classmethod
    def query(cls, *args):
        a = [cls]
        a += args
        return DBSession.query(*a)

    @classmethod
    def all(cls):
        return cls.query().all()
