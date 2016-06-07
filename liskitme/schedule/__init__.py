from liskitme import config
from liskitme.model import init_model as init_sqlalchemy_model
from liskitme.pool import init_model as init_mongo_model
from sqlalchemy.engine import create_engine

"""
first timestamp
"""
base_timestamp = config.get('main', 'base_timestamp')

"""
Our delegate
"""
delegate = config.get('main', 'delegate')

"""
Init of sql database PostGres Soon
"""
# engine and delegate are temporarily hard coded TODO: remove them and place in config
engine = create_engine(config.get('chain', 'db_url'), echo=True)
init_sqlalchemy_model(engine)

"""
Init of mongo database
"""
# bind = create_datastore('mongodb://localhost:27017/lisk-pool')
init_mongo_model(
    config.get('mongo', 'db_name'),
    host=config.get('mongo', 'host'), port=config.get('mongo', 'port'),
    username=config.get('mongo', 'username'), password=config.get('mongo', 'password'))
