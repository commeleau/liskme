# from ming.config import configure
# from ming.datastore import create_datastore
# from ming.odm.odmsession import ThreadLocalODMSession
#
# configure(**{'ming.mysession.uri': 'mongodb://localhost:27017/tutorial'})
#
# session = ThreadLocalODMSession.by_name('pool_session')


import ming.odm
from session import mainsession, DBSession

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    mainsession.bind = engine
    ming.odm.Mapper.compile_all()

    for mapper in ming.odm.Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)