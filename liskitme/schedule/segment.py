import time

from liskitme.model.chain import Vote, Transaction, Block
from liskitme.schedule import delegate
import logging
"""
This Module define classes to easily extract round info from the blockchain using the sql models
"""


class Segment:
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """
    # private variables for caching and storing of transactions
    __transactions = []
    __cached = False

    __votes = []

    def __init__(self, end=-1):
        """
        Init a segment to a final block
        voters parameter should be the dictionary of the voters of the precedent round
        :param end:
        """
        self.highest_block = Block.highest_block_before(end)
        # Get blocks in Segment and set start and end blocks
        self.end = self.highest_block.height
        # Init voters dictionary
        self.__voters = {}

    @property
    def round(self):
        return (self.end+1)/101

    @property
    def voters(self):
        """
        get voters: if not cached it will calculate them
        :return:
        :rtype:list of LiskAccount
        """
        if not self.__cached:
            for vote in self.get_votes():
                self.add(vote)
            self.__cached = True
        return self.__voters

    def get_votes(self):
        """
        get the votes for the segment
        :return:
        :rtype:list of Vote
        """
        # return reduce(lambda x, y: x + y.get_votes_for(self.delegate), self.__blocks, [])
        logging.debug("query votes")
        start = time.clock()
        self.__votes = Vote.get_votes_for_delegate_before_block(delegate, self.end)
        logging.debug("query votes end in %f" % (time.clock() - start))
        return self.__votes

    def add(self, vote):
        """
        add a vote to single account
        :param vote:
        :return:
        """
        if vote[0].account in self.__voters:
            self.__voters[vote[0].account].vote(vote[0])
        else:
            account = LiskAccount(account=vote[0].account, amount=vote[2] - vote[3], segment=self)
            account.vote(vote[0])
            self.__voters[vote[0].account] = account

    def start_query_amount(self):
        """

        :return:
         :rtype:sqlalchemy.orm.query.Query
        """
        q = Transaction.start_query_get_amount()
        return Transaction.query_get_transactions_before_block(self.end, q)

    def income_amount_for_account(self, account):
        """

        :param account:
        :return:
        :rtype:int
        """
        return Transaction.query_get_income_transactions_for_account(account, self.start_query_amount()).scalar()

    def outcome_amount_for_account(self, account):
        """

        :param account:
        :return:
        :rtype:int
        """
        return Transaction.query_get_outcome_transactions_for_account(account, self.start_query_amount()).scalar()


class LiskAccount:
    """
    class that define a single account
    """

    __amount = 0
    __cached = False
    voting = True
    account = 0

    def __init__(self, account, amount, segment):
        # TODO: add validation on account
        self.account = account
        self.__amount = amount
        self.__cached = True
        self.__segment = segment

    @property
    def amount(self):
        """
        return lisk amount if not cached it calcs it
        :return:
        :rtype:int
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
        operator = vote.get_operator_for_delegate(delegate)
        if operator == '-':
            self.voting = False
        if operator == '+':
            self.voting = True

    def __calc_amount(self):
        """
        calculate the amount
        :return:
        """
        logging.debug('Calcolo di amout per %s' % self.account)
        self.__amount = self.get_income_amount() - self.get_outcome_amount()
        self.__cached = True
        logging.debug('Fine calcolo di amout per %s' % self.account)

    def get_income_amount(self):
        """
        get income transactions
        :return:
        :rtype:int
        """
        return self.__segment.income_amount_for_account(self.account)

    def get_outcome_amount(self):
        """
        get outcome transactions
        :return:
        :rtype:int
        """
        return self.__segment.outcome_amount_for_account(self.account)

    def __repr__(self):
        return "<Account(amount='%s',voting='%s')>" % (self.amount/10000/10000, self.voting)


