from flask import Flask
from liskitme import config
from liskitme.pool import init_model as init_mongo_model


init_mongo_model(
    config.get('mongo', 'db_name'),
    host=config.get('mongo', 'host'), port=int(config.get('mongo', 'port')),
    username=config.get('mongo', 'username'), password=config.get('mongo', 'password'))

app = Flask(__name__)

import flisk.main
