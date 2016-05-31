
from ming import schema as s
from ming.odm import MappedClass
from ming.odm import FieldProperty

from session import DBSession



class Round(MappedClass):
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """

    class __mongometa__:
        session = DBSession
        name = 'Round'
        unique_indexes = [('_id'),]

    _id = FieldProperty(s.ObjectId)
    height = FieldProperty(s.Int)
    end = FieldProperty(s.Int)
    # accounts = FieldProperty(s.Array)

    # private variables for caching and storing of transactions
    __transactions = []
    __cached = False

