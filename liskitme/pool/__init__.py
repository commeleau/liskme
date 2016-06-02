from session import mainsession, DBSession
from mongoengine import connect


def init_model(database, host, port, username, password):
    """Call me before using any of the tables or classes in the model."""
    connect(database, host=host, port=port, username=username, password=password)
