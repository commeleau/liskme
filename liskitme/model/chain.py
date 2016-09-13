import datetime
import logging

import re

from sqlalchemy.dialects import postgresql

from liskitme.model.helpers import BaseQuery
from liskitme.model import DBSession
from liskitme.model import DeclarativeBase
from liskitme.schedule import base_timestamp
from sqlalchemy import Column, Integer, String, BigInteger, Binary, Text, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func


class Transaction(DeclarativeBase, BaseQuery):
    """
    Class that map the table of transactions on the blockchain database
    """
    __tablename__ = 'trs'

    id = Column(String, primary_key=True)
    blockId = Column(String, ForeignKey('blocks.id'))
    type = Column(Integer)
    timestamp = Column(Integer)
    senderPublicKey = Column(Binary)
    senderId = Column(String)
    recipientId = Column(String)
    # senderUsername = Column(String)
    # recipientUsername = Column(String)
    amount = Column(BigInteger)
    fee = Column(BigInteger)
    signature = Column(Binary)
    signSignature = Column(Binary)
    requesterPublicKey = Column(Binary)
    signatures = Column(Text)

    # relationship with Vote setted to eager loading for performance and quick analising the segment
    vote = relation('Vote', back_populates='transaction', uselist=False)
    # relationship with Block
    blocks = relation("Block", back_populates="transactions")


    @property
    def datetime(self):
        """
        return the datetime shifted with base_timestamp
        :return: datetime
        """
        return datetime.datetime.fromtimestamp(self.timestamp + base_timestamp)

    @staticmethod
    def start_query_get_amount():
        return DBSession.query(func.sum(Transaction.amount))

    @classmethod
    def query_get_outcome_transactions_for_account(cls, account, query=None):
        if not query:
            query = cls.query()
        return query.filter(Transaction.senderId == account)

    @classmethod
    def query_get_income_transactions_for_account(cls, account, query=None):
        if not query:
            query = cls.query()
        return query.filter(Transaction.recipientId == account)

    @classmethod
    def query_get_transactions_before_block(cls, block, query=None):
        if not query:
            query = cls.query()
        return query.join(Block).filter(Block.height <= block)

    def __repr__(self):
        return "<Transaction(id='%s',datetime=%s)>" % (self.id, self.datetime)


class Block(DeclarativeBase, BaseQuery):
    """
    Class that map the table of blocks on the blockchain database
    """
    __tablename__ = 'blocks'

    id = Column(String, primary_key=True)
    version = Column(Integer)
    timestamp = Column(Integer)
    height = Column(Integer)
    numberOfTransactions = Column(Integer)
    totalAmount = Column(BigInteger)
    totalFee = Column(BigInteger)
    reward = Column(BigInteger)
    payloadLength = Column(Integer)
    payloadHash = Column(Binary)
    generatorPublicKey = Column(Binary)
    blockSignature = Column(Binary)
    previousBlock = Column(Integer, ForeignKey('blocks.id'))
    following = relation("Block", uselist=False, backref=backref('previous', remote_side=[id], uselist=False))
    transactions = relation('Transaction', back_populates='blocks')

    @property
    def datetime(self):
        """
        return the datetime shifted with base_timestamp
        :return: datetime
        """
        return datetime.datetime.fromtimestamp(self.timestamp + base_timestamp)

    def __repr__(self):
        return "<Block(height='%s',datetime=%s)>" % (self.height, self.datetime)

    def get_votes_for(self, delegate):
        """
        return votes for one delegate
        :param delegate:
        :return: array of Vote
        """
        return [t.vote for t in self.transactions if t.vote and t.vote.has_delegate(delegate)]

    @classmethod
    def highest_block_before(cls, end=-1):
        """
        :param end:
        :return block:
        :rtype:Block
        """
        query = cls.query().order_by(cls.height.desc())
        if end >= 0:
            query = query.filter(cls.height <= end)
        return query.first()

    @classmethod
    def blocks_from_x_to_y(cls, start=-1, end=-1):
        """
        return blocks from start to end
        if parameter are < 0 it won't be considered
        :param start:
        :param end:
        :return:
        """
        query = cls.query()
        if end >= 0:
            query = query.filter(cls.height < end)
        if start >= 0:
            query = query.filter(cls.height >= start)
        return query.all()


class Vote(DeclarativeBase, BaseQuery):
    """
    Class that models the vote table
    """

    __tablename__ = 'votes'

    votes = Column(String)
    transactionId = Column(String, ForeignKey('trs.id'), primary_key=True)

    transaction = relationship('Transaction', back_populates='vote')

    def __repr__(self):
        return "<Vote(votes='%s')>" % self.votes

    @classmethod
    def get_votes_for_delegate_before_block(cls, delegate, block):
        """

        :param delegate:
        :type delegate:str
        :param block:
        :type block:Block
        :return:
         :rtype:list of Vote
        """

        outcome = DBSession.query(
            Transaction.senderId.label('account'),
            func.sum(Transaction.amount).label('outcome_amount')
        ).group_by(Transaction.senderId).subquery('outcome')

        income = DBSession.query(
            Transaction.recipientId.label('account'),
            func.sum(Transaction.amount).label('income_amount')
        ).group_by(Transaction.recipientId).subquery('income')

        query = cls.query_get_votes_for_delegate(delegate, DBSession.query(Vote, Transaction, income.c.income_amount, outcome.c.outcome_amount))
        query = cls.query_get_votes_before_block(block, query)
        query = query.join(income, income.c.account == Transaction.senderId).join(outcome, outcome.c.account == Transaction.senderId)
        # logging.debug(str(query.statement.compile(compile_kwargs={"literal_binds": True}, dialect=postgresql.dialect())))
        return query.all()

    @classmethod
    def query_get_votes_before_block(cls, block, query=None):
        if not query:
            query = cls.query()
        return query.join(Transaction).join(Block).filter(Block.height <= block)

    @classmethod
    def query_get_votes_for_delegate(cls, delegate, query=None):
        if not query:
            query = cls.query()
        return query.filter(Vote.votes.like('%' + delegate + '%'))

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
        p = re.compile(ur'([-,+])%s' % delegate)
        m = p.search(self.votes)
        return m.group(1)
