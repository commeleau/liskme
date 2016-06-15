from datetime import datetime

from liskitme.schedule.schedule import get_block_height_from_round_height
from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField, ListField, FloatField, Q, BooleanField


class Round(Document):
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """
    height = IntField()
    end = IntField()
    weight = IntField()

    forged = IntField()  # TODO: the main thing missing right now

    timestamp = DateTimeField(default=datetime.now)
    votes = ListField(ReferenceField(Vote))

    @classmethod
    def create_from_chain(cls, height, segment):
        """
        :param height: round height
        :type height: int
        :param segment: segment base
        :type segment: liskitme.schedule.segment.Segment
        :return:
        :rtype:Round
        """
        if segment.end != get_block_height_from_round_height(height):
            # These exception is throw generally if the block is not yet at the end of asked segment.
            # Or the blockchain is not sincronized or it's too early
            raise ValueError("Segment doesn't reach round height")
        r = Round(height=height, end=segment.end, timestamp=segment.highest_block.datetime)
        r.save()
        return r

    @classmethod
    def highest_round(cls):
        return cls.objects().order_by('-height').first()


class Vote(Document):

    account = ReferenceField(Account)
    kappa = IntField()
    weight = IntField()
    amount = IntField()
    percent = FloatField()
    round = ReferenceField(Round)
    voted = BooleanField(default=False)

    def get_previous_vote(self):
        return Vote.objects(account=self.account, round__height=self.round.height)


class Account(Document):

    address = StringField()
    votes = ListField(ReferenceField('Vote'))
    # data about how it likes to have things

    @classmethod
    def get_or_create(cls, account):
        """
        :param account:
         :type account:LiskAccount
        :return:
         :rtype:Account
        """
        return cls.objects(account=account.account) \
            .modify(upsert=True, new=True,
                    set__address=account.account)

    def get_number_of_votes(self, amount=-1, percent=-1, voted=True):
        return Vote.objects(account=self, amount__gte=amount, percent__gte=percent, vote=voted).count()

    def get_number_of_excluded_votes(self, amount=-1, percent=-1, voted=True):
        return Vote.objects(Q(account=self) & (Q(amount__lt=amount) | Q(percent__lt=percent)) & Q(voted=voted)).count()

