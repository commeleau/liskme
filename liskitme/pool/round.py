from datetime import datetime
from ming import schema as s
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty

from session import DBSession


class Round(MappedClass):
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """

    class __mongometa__:
        session = DBSession
        name = 'Round'
        unique_indexes = [('_id', 'height'), ]

    _id = FieldProperty(s.ObjectId)
    height = FieldProperty(s.Int)
    end = FieldProperty(s.Int)
    start = FieldProperty(s.Int)
    weight = FieldProperty(s.Int)

    mined = FieldProperty(s.Int)  # TODO: the main thing missing right now

    timestamp = FieldProperty(s.DateTime, if_missing=datetime.now)
    voters = RelationProperty('Voter')


class Voter(MappedClass):

    class __mongometa__:
        session = DBSession
        name = 'Voter'
        unique_indexes = [('_id', ), ]
        indexes = [('account', ), ]

    _id = FieldProperty(s.ObjectId)
    account = FieldProperty(s.String)
    kappa = FieldProperty(s.Int)
    weight = FieldProperty(s.Int)
    amount = FieldProperty(s.Int)
    percent = FieldProperty(s.Float)
    round_id = ForeignIdProperty('Round')
    round = RelationProperty('Round')
