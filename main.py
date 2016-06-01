from flask.ext.pymongo import PyMongo
from liskitme.model import init_model
from liskitme.model.chain import Transaction, Block
from ming.datastore import create_datastore
from sqlalchemy import create_engine
from liskitme.pool import init_model

engine = create_engine('sqlite:///blockchain-last.db', echo=True)

init_model(engine=engine)

# b = Block.query().first()
#
# print b
#
# follow = b.following
#
# print follow
#
# print follow.previous

# blocks = Block.votes_from_x_to_y(0, 101)

# print blocks
# print blocks[50].votes()

bind = create_datastore('mongodb://localhost:27017/lisk-pool')

init_model(bind)