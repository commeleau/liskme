

# Get last round height in mongo

# Starting from round height * 101 + 1 create a Segment every 101 block (as 1 segment for round)

"""
For each segment get:
- round height
- get all voters
for each voter:
    - add account in mongo if needed
    - calculate k
    - calculate vote weight
    - add vote in mongo
meanwhile calculate round weight
calculate percentage for each vote
go next segment

"""
from liskitme.pool.round import Account, Round, Vote
from liskitme.segment import Segment


def get_block_height_from_round_height(round_height):
    return round_height * 101 + 1


def calc_kappa(n):
    """
    Calculate the kappa.
    Now simple version number of votes plus one
    :param n:
    :return:
    """
    return n + 1


def parse_segment(round_height):

    segment = Segment(get_block_height_from_round_height(round_height))

    r = Round(height=round_height, segment=segment)
    r.weight = 0
    r.save()
    voters = segment.voters
    for vote in voters:
        account = Account.get_or_create(vote.account)
        v = Vote(account=account,
                 amount=vote.account.amount, round=r,
                 kappa=account.get_number_of_votes(),
                 weight=account.get_number_of_votes()*vote.account.amount
                 )
        r.weight += v.weight
        v.save()

    r.save()

    for v in r.votes:
        v.percent = v.weight/r.weight*100
        v.save()

    return r


r = Round.highest_round()

if r is None:
    h = 1
else:
    h = r.height

while True:
    try:
        parse_segment(h+101)
    except ValueError:
        break

