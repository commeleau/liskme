from liskitme.model import DeclarativeBase
from liskitme.model.helpers import BaseQuery
from sqlalchemy import Column, Integer, String, BigInteger, Binary, Text, ForeignKey
from sqlalchemy.orm import relation
import re


class Vote(DeclarativeBase, BaseQuery):
    """
    Class that models the vote table
    """

    __tablename__ = 'votes'

    votes = Column(String)
    transactionId = Column(String, ForeignKey('trs.id'), primary_key=True)

    transaction = relation('Transaction', back_populates='vote')

    def __repr__(self):
        return "<Vote(votes='%s')>" % self.votes

    @property
    def account(self):
        """
        get account
        :return:
        """
        return self.transaction.senderId

    def has_delegate(self, delegate):
        """
        get if has delegate
        :param delegate:
        :return:
        """
        p = re.compile(ur'([-,+])%s' % delegate)
        return re.search(p, self.votes)

    def get_operator_for_delegate(self, delegate):
        """
        get operetor of vote operation on delegate
        :param delegate:
        :return:
        """
        m = re.search(delegate, self.votes)
        return m.group(0)
