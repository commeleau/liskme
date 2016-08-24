import logging

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
from liskitme.schedule.segment import Segment


def get_block_height_from_round_height(round_height):
    return round_height * 101 + 1


def calc_kappa(n):
    """
    Calculate the kappa.
    Now simple version number of votes plus one
    :param n:
    :return:
    :rtype: int
    """
    return n + 1


def calc_kappa_from_account(account):
    """
    Calculate the kappa.
    Now simple version is just a wrapper for calc_kappe with account number of votes
    :param account:
    :type account:Account
    :return:
    :rtype: int
    """
    return calc_kappa(account.get_number_of_votes())


def parse_segment(round_height):
    """
    Implementation of the blockchain parsing
    :param round_height: the round height that we have to parse
    :return:
    :rtype:Round
    """
    # get the segment for the asked round_height
    segment = Segment(get_block_height_from_round_height(round_height))
    # creation of the round
    r = Round.create_from_chain(height=round_height, segment=segment)
    # assigning base weight and save
    r.weight = 0
    r.save()
    # getting the voters
    voters = segment.voters
    logging.info('found %d voters' % len(segment.voters))
    # for each vote in voters gets or create the Account from mongo
    for vote in voters:
        account = Account.get_or_create(vote.account)
        # Calculates kappa
        kappa = calc_kappa_from_account(account)
        # Create the vote and save it
        v = Vote(account=account,
                 amount=vote.account.amount, round=r,
                 kappa=kappa,
                 weight=kappa*vote.account.amount,
                 voted=vote.voting
                 )
        v.save()
        # increments the round weight
        r.weight += v.weight
    # eventually save the round with updated round weight
    r.save()

    # cycle again votes in order to calculate percentage of the vote in round
    for v in r.votes:
        v.percent = v.weight/r.weight*100
        v.save()
    # end. we return round for better use of function
    return r


def run():
    """
    Runnable function that analyse the blockchain
    :return:
    """
    # Gets the highest round in the database
    r = Round.highest_round()

    # sets height
    if r is None:
        logging.info("db is empty prepare yourself")
        h = 1
    else:
        logging.info("Last round in db is %d " % r.height)
        h = r.height + 1

    # starts looping
    while True:
        try:
            logging.info('parsing round %s' % h)
            parse_segment(h)
            h += 1
        except ValueError:
            # These exception is throw generally if the block is not yet at the end of asked segment.
            # Or the blockchain is not sincronized or it's too early
            logging.warn('Not enough blocks to parse')
            break

