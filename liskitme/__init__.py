from liskitme.model import init_model
from ming.config import configure
from ming.datastore import create_datastore
from ming.odm.odmsession import ThreadLocalODMSession
from sqlalchemy.engine import create_engine

base_timestamp = 1428544800


configure(**{'ming.mysession.uri': 'mongodb://localhost:27017/tutorial'})
bind = create_datastore('tutorial')
session = ThreadLocalODMSession.by_name('mysession')

# engine and delegate are temporarily hard coded TODO: remove them and place in config
engine = create_engine('sqlite:///blockchain-last.db', echo=True)
delegate = "e0f1c6cca365cd61bbb01cfb454828a698fa4b7170e85a597dde510567f9dda5"

init_model(engine)
