from datetime import datetime
from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField, ListField, FloatField, Q

class Round(Document):
    """
    Class made to handle the blocks in every delegate round and stores it in database
    """
    height = IntField()
    end = IntField()
    start = IntField()
    weight = IntField()

    forged = IntField()  # TODO: the main thing missing right now

    timestamp = DateTimeField(default=datetime.now)
    votes = ListField(ReferenceField(Vote))

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

    def get_previous_vote(self):
        return Vote.objects(account=self.account, round__height=self.round.height)


class Account(Document):

    address = StringField()
    votes = ListField(ReferenceField('Vote'))
    # data about how it likes to have things

    def get_number_of_votes(self, amount=-1, percent=-1):
        return Vote.objects(account=self, amount__gte=amount, percent__gte=percent).count()

    def get_number_of_excluded_votes(self, amount=-1, percent=-1):
        return Vote.objects(Q(account=self) & (Q(amount__lt=amount) | Q(percent__lt=percent))).count()

