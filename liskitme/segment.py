from liskitme.model import init_model
from sqlalchemy import create_engine

from liskitme.model.chain import Vote, Transaction
from ming import schema as s
from ming import create_datastore, configure
from ming.schema import FancySchemaItem
from ming.odm import ThreadLocalODMSession

from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty

# configure(**{'ming.mysession.uri': 'mongodb://localhost:27017/tutorial'})
# bind = create_datastore('tutorial')
# session = ThreadLocalODMSession.by_name('mysession')


class Segment(MappedClass):
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """


    # class __mongometa__:
    #     session = session
    #     name = 'wiki_page'
    #
    # _id = FieldProperty(s.ObjectId)
    # round = FieldProperty(s.Int)
    # start = FieldProperty(s.Int)
    # end = FieldProperty(s.Int)
    # accounts = FieldProperty(s.Array(s.Object))


    # engine and delegate are temporarily hard coded TODO: remove them and place in config
    engine = create_engine('sqlite:///blockchain-last.db', echo=True)
    delegate = "e0f1c6cca365cd61bbb01cfb454828a698fa4b7170e85a597dde510567f9dda5"


    # private variables for caching and storing of transactions
    __transactions = []
    __cached = False

    def __init__(self, end=-1):
        """
        Init with starting and ending block
        voters parameter should be the dictionary of the voters of the precedent round
        :param start:
        :param end:
        :param voters:
        """

        super(Segment, self).__init__()

        # TODO: remove inizialisation of DB
        init_model(self.engine)

        # Get blocks in Segment and set start and end blocks
        self.end = end
        # Init voters dictionary
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
        # return reduce(lambda x, y: x + y.get_votes_for(self.delegate), self.__blocks, [])
        return Vote.get_votes_for_delegate_before_block(self.delegate, self.end)

    def add(self, vote):
        """
        add a vote to single account
        :param vote:
        :return:
        """
        if vote.account in self.__voters:
            self.__voters[vote.account].vote(vote)
        else:
            self.__voters[vote.account] = Account(account=vote.account, segment=self)

    def start_query_amount(self):
        q = Transaction.start_query_get_amount()
        return Transaction.query_get_transactions_before_block(self.end, q)

    def income_amount_for_account(self, account):
        return Transaction.query_get_income_transactions_for_account(account, self.start_query_amount()).scalar()

    def outcome_amount_for_account(self, account):
        return Transaction.query_get_outcome_transactions_for_account(account, self.start_query_amount()).scalar()


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
        operator = vote.get_operator_for_delegate(self.__segment.delegate)
        if operator == '-':
            self.__voting = False
        if operator == '+':
            self.__voting = True

    def __calc_amount(self):
        """
        calculate the amount
        :return:
        """
        self.__amount = self.get_income_amount() - self.get_outcome_amount()
        self.__cached = True

    def get_income_amount(self):
        """
        get income transactions
        :return:
        """
        return self.__segment.income_amount_for_account(self.account)

    def get_outcome_amount(self):
        """
        get outcome transactions
        :return:
        """
        return self.__segment.outcome_amount_for_account(self.account)

    def __repr__(self):
        return "<Account(amount='%s',voting='%s')>" % (self.amount/10000/10000, self.__voting)


