from liskitme.model import init_model
from sqlalchemy import create_engine

from liskitme.model.chain import Block


class Segment:

    engine = create_engine('sqlite:///blockchain.db', echo=True)
    delegate = "10310263204519541551L"
    __transactions = []
    __cached = False

    def __init__(self, start=-1, end=-1, voters=None):
        init_model(self.engine)
        self.__blocks = Block.blocks_from_x_to_y(start, end)

        self.start = self.__blocks[0]
        self.end = self.__blocks[-1]
        try:
            self.__voters = {x: Account(x, self) for x in voters.keys()}
        except AttributeError:
            self.__voters = {}

    @property
    def transactions(self):
        if len(self.__transactions) == 0:
            self.__transactions = reduce(lambda x, y: x + y, [b.transactions for b in self.__blocks])
        return self.__transactions

    @property
    def voters(self):
        if not self.__cached:
            for vote in self.get_votes():
                self.add(vote)
        return self.__voters

    def get_votes(self):
        return reduce(lambda x, y: x + y.get_votes_for(self.delegate), self.__blocks, [])

    def add(self, vote):
        if vote.account in self.__voters.has_key:
            self.__voters[vote.account].vote(vote)
        else:
            self.__voters[vote.account] = Account(account=vote.account, segment=self)


class Account:

    __amount = 0
    __cached = False
    __voting = True

    def __init__(self, account, segment):
        # TODO: add validation on account
        self.account = account
        self.__segment = segment

    @property
    def amount(self):
        if not self.__cached:
            self.__calc_amount()
        return self.__amount

    def vote(self, vote):
        operator = vote.get_operator_for(self.__segment.delegate)
        if operator == '-':
            self.__voting = False
        if operator == '+':
            self.__voting = True

    def __calc_amount(self):
        # transactions = self.get_transactions()
        for in_t in self.get_income_transactions():
            self.__amount += in_t.amount
        for out_t in self.get_outcome_transactions():
            self.__amount += out_t.amount
        self.__cached = True

    def get_transactions(self):
        return self.get_income_transactions() + self.get_outcome_transactions()

    def get_income_transactions(self):
        return [t for t in self.__segment.transactions if t.recipientId == self.account]

    def get_outcome_transactions(self):
        return [t for t in self.__segment.transactions if t.senderId == self.account]




