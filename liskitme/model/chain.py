from liskitme.model import DeclarativeBase
from liskitme.model.helpers import BaseQuery
from sqlalchemy import Column, Integer, String, BigInteger, Binary, Text, ForeignKey
from sqlalchemy.orm import relation, backref
from liskitme import base_timestamp
import datetime
from liskitme.model.votes import Vote


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
    senderUsername = Column(String)
    recipientUsername = Column(String)
    amount = Column(BigInteger)
    fee = Column(BigInteger)
    signature = Column(Binary)
    signSignature = Column(Binary)
    requesterPublicKey = Column(Binary)
    signatures = Column(Text)

    # relationship with Vote setted to eager loading for performance and quick analising the segment
    vote = relation('Vote', back_populates='transaction', lazy='joined', uselist=False)
    # relationship with Block
    blocks = relation("Block", back_populates="transactions")


    @property
    def datetime(self):
        """
        return the datetime shifted with base_timestamp
        :return: datetime
        """
        return datetime.datetime.fromtimestamp(self.timestamp + base_timestamp)

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
    transactions = relation('Transaction', back_populates='blocks', lazy='joined')

    @property
    def datetime(self):
        """
        return the datetime shifted with base_timestamp
        :return: datetime
        """
        return datetime.datetime.fromtimestamp(self.timestamp + base_timestamp)

    def __repr__(self):
        return "<Block(height='%s',datetime=%s)>" % (self.height,self.datetime)

    def get_votes_for(self, delegate):
        """
        return votes for one delegate
        :param delegate:
        :return: array of Vote
        """
        return [t.vote for t in self.transactions if t.vote and t.vote.has_delegate(delegate)]

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
            query.filter(cls.height < end)
        if start >= 0:
            query.filter(cls.height >= start)
        return query.all()
