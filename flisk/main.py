import flask
from flisk import app
from liskitme.pool.round import Account


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/account/<address>')
def show_user_profile(address):

    # show the user profile for that user
    return flask.jsonify(**Account.objects(address=address))
