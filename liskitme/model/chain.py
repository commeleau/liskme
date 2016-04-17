from liskitme.model import DeclarativeBase
from liskitme.model.helpers import BaseQuery
from sqlalchemy import Column, Integer, String, BigInteger, Binary, Text, ForeignKey
from sqlalchemy.orm import relation, backref
from liskitme.model.votes import Vote


class Transaction(DeclarativeBase, BaseQuery):

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
    vote = relation('Vote', back_populates='transaction', lazy='joined', uselist=False)
    blocks = relation("Block", back_populates="transactions")


class Block(DeclarativeBase, BaseQuery):

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

    def __repr__(self):
        return "<Block(height='%s')>" % self.height

    def get_votes_for(self, delegate):
        return [t.vote for t in self.transactions if t.vote and t.vote.has_delegate(delegate)]

    @classmethod
    def blocks_from_x_to_y(cls, start=-1, end=-1):
        query = cls.query()
        if end > 0:
            query.filter(cls.height < end)
        if start > 0:
            query.filter(cls.height >= start)
        return query.all()