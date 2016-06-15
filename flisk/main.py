from flisk import app

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/account/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username
