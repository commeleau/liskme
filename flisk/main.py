import json

import flask
from flisk import app
import liskitme
from liskitme.pool.round import Account, Vote, Round


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/account/')
def show_users():
    # show the user profile for that user
    accounts = Account.objects()
    list_result = [dict(address=entry.address) for entry in accounts]
    return flask.jsonify(accounts=list_result, num=len(list_result))

@app.route('/account2/')
def show_users2():
    # show the user profile for that user
    r = Round.highest_round()

    accounts = Vote.objects(voted=True, round=r)
    list_result = [dict(address=entry.address, voted=entry.voted) for entry in accounts]

    accounts = Vote.objects(voted=False, round=r)
    list_resultfalse = [dict(address=entry.address, voted=entry.voted) for entry in accounts]

    return flask.jsonify(date=r.timestamp, accounts=list_result, false=list_resultfalse, num=len(list_result))


@app.route('/account/<address>')
def show_user_profile(address):

    # account = Account.objects(address=address).get()

    votes = Vote.objects(address=address)
    # account = ReferenceField(Account)
    # kappa = IntField()
    # weight = IntField()
    # amount = IntField()
    # percent = FloatField()
    # round = ReferenceField('Round')
    # voted = BooleanField(default=False)
    list_result = [dict(voted=entry.voted,
                        date=entry.round.timestamp, kappa=entry.kappa,
                        weight=entry.weight, amount=entry.amount, percent=entry.percent) for entry in votes]
    # show the user profile for that user
    return flask.jsonify(dict(address=address, votes=list_result, num=len(list_result), last=list_result[-1]))
