from liskitme.model import init_model as init_sqlalchemy_model
from liskitme.pool import init_model as init_ming_model
from ming.datastore import create_datastore
from sqlalchemy.engine import create_engine

"""
first timestamp
"""
base_timestamp = 1428544800

"""
Our delegate
"""
delegate = "e0f1c6cca365cd61bbb01cfb454828a698fa4b7170e85a597dde510567f9dda5"

"""
Init of sql database PostGres Soon
"""
# engine and delegate are temporarily hard coded TODO: remove them and place in config
engine = create_engine('sqlite:///blockchain-last.db', echo=True)
init_sqlalchemy_model(engine)

"""
Init of mongo database
"""
bind = create_datastore('mongodb://localhost:27017/lisk-pool')
init_ming_model(bind)