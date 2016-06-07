
from mongoengine import connect


def init_model(database, host="localhost", port=27017, username="", password=""):
    """Call me before using any of the tables or classes in the model."""
    connect(database, host=host, port=port, username=username, password=password)
