from liskitme.model import init_model
from sqlalchemy import create_engine

from liskitme.model.chain import Block


class Segment:
    """
    Class made to handle the blocks in every delegate round
    """

    # engine and delegate are temporarily hard coded TODO: remove them and place in config
    engine = create_engine('sqlite:///blockchain.db', echo=True)
    delegate = "10310263204519541551L"

    # private variables for caching and storing of transactions
    __transactions = []
    __cached = False

    def __init__(self, start=-1, end=-1, voters=None):
        """
        Init with starting and ending block
        voters parameter should be the dictionary of the voters of the precedent round
        :param start:
        :param end:
        :param voters:
        """

        # TODO: remove inizialisation of DB
        init_model(self.engine)

        # Get blocks in Segment and set start and end blocks
        self.__blocks = Block.blocks_from_x_to_y(start, end)
        self.start = self.__blocks[0]
        self.end = self.__blocks[-1]
        # Init voters dictionary
        try:
            self.__voters = {x: Account(x, self) for x in voters.keys()}
        except AttributeError:
            self.__voters = {}

    @property
    def transactions(self):
        """
        get transactions for account statistics
        :return:
        """
        if len(self.__transactions) == 0:
            self.__transactions = reduce(lambda x, y: x + y, [b.transactions for b in self.__blocks])
        return self.__transactions

    @property
    def voters(self):
        """
        get voters: if not cached it will calculate them
        :return:
        """
        if not self.__cached:
            for vote in self.get_votes():
                self.add(vote)
        return self.__voters

    def get_votes(self):
        """
        get the votes for the segment
        :return:
        """
        return reduce(lambda x, y: x + y.get_votes_for(self.delegate), self.__blocks, [])

    def add(self, vote):
        """
        add a vote to single account
        :param vote:
        :return:
        """
        if vote.account in self.__voters.has_key:
            self.__voters[vote.account].vote(vote)
        else:
            self.__voters[vote.account] = Account(account=vote.account, segment=self)


class Account:
    """
    class that define a single account
    """

    __amount = 0
    __cached = False
    __voting = True

    def __init__(self, account, segment):
        # TODO: add validation on account
        self.account = account
        self.__segment = segment

    @property
    def amount(self):
        """
        return lisk amount if not cached it calcs it
        :return:
        """
        if not self.__cached:
            self.__calc_amount()
        return self.__amount

    def vote(self, vote):
        """
        add a vote to the account (revoke or add)
        :param vote:
        :return:
        """
        operator = vote.get_operator_for(self.__segment.delegate)
        if operator == '-':
            self.__voting = False
        if operator == '+':
            self.__voting = True

    def __calc_amount(self):
        """
        calculate the amount
        :return:
        """
        # transactions = self.get_transactions()
        for in_t in self.get_income_transactions():
            self.__amount += in_t.amount
        for out_t in self.get_outcome_transactions():
            self.__amount += out_t.amount
        self.__cached = True

    def get_transactions(self):
        """
        get income transactions
        :return:
        """
        return self.get_income_transactions() + self.get_outcome_transactions()

    def get_income_transactions(self):
        """
        get income transactions
        :return:
        """
        return [t for t in self.__segment.transactions if t.recipientId == self.account]

    def get_outcome_transactions(self):
        """
        get outcome transactions
        :return:
        """
        return [t for t in self.__segment.transactions if t.senderId == self.account]




