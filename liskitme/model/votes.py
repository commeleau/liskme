from liskitme.model import DeclarativeBase
from liskitme.model.helpers import BaseQuery
from sqlalchemy import Column, Integer, String, BigInteger, Binary, Text, ForeignKey
from sqlalchemy.orm import relation
import re


class Vote(DeclarativeBase, BaseQuery):

    __tablename__ = 'votes'

    votes = Column(String)
    transactionId = Column(String, ForeignKey('trs.id'), primary_key=True)

    transaction = relation('Transaction', back_populates='vote')

    def __repr__(self):
        return "<Vote(votes='%s')>" % self.votes

    # def __add__(self, other): completamente sbagliato
    #     votes = []
    #
    #     re.search()
    #     self_votes = {x[1:]: x[0] for x in self.votes.split(',') if len(x) > 0}
    #     other_votes = {x[1:]:  x[0] for x in other.votes.split(',') if len(x) > 0}
    #
    #     votes += [
    #                  "+%s" % vote
    #                  for vote, operation in self_votes.iteritems()
    #                  if operation == '+' and not other_votes.get(vote, False) or
    #                  operation == '+' and other_votes[vote] == '+'
    #                  ] + [
    #                  "+%s" % vote
    #                  for vote, operation in other_votes.iteritems()
    #                  if operation == '+' and not self_votes.get(vote, False)
    #                  ] + [
    #                  "-%s" % vote
    #                  for vote, operation in self_votes.iteritems()
    #                  if operation == '-' and not other_votes.get(vote, False) or
    #                  operation == '-' and other_votes[vote] == '-'
    #                  ] + [
    #                  "-%s" % vote
    #                  for vote, operation in other_votes.iteritems()
    #                  if operation == '-' and not self_votes.get(vote, False)
    #                  ]
    #     v = Vote()
    #     v.votes = ','.join(votes)
    #     return v

    @property
    def account(self):
        return self.transaction.senderId

    def has_delegate(self, delegate):
        p = re.compile(ur'([-,+])%s' % delegate)
        return re.search(p, self.votes)

    def get_operator_for_delegate(self, delegate):
        m = re.search(delegate, self.votes)
        return m.group(0)
    #
    # @classmethod
    # def votes_in_blocks(cls, blocks):
    #     v = Vote()
    #     v.votes = ''
    #     return reduce(lambda x, y: x + y, [block.votes() for block in blocks], v)



