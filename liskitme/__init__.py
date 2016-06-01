from liskitme.model import init_model

from sqlalchemy.engine import create_engine

base_timestamp = 1428544800

# engine and delegate are temporarily hard coded TODO: remove them and place in config
engine = create_engine('sqlite:///blockchain-last.db', echo=True)
delegate = "e0f1c6cca365cd61bbb01cfb454828a698fa4b7170e85a597dde510567f9dda5"

init_model(engine)
