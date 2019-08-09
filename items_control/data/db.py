from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import os


def open_db(filename, debug=False):
    if os.path.isfile(filename):

        resetglobal()
        global engine
        global session
        global session_factory
        env = os.environ
        if 'DEBUG_DB' in env and env['DEBUG_DB'] == '1':
            debug = True
        engine = Engine(filename, debug)
        session = Session()
        session_factory = sessionmaker(bind=engine)


def create_db(filename):
    if not os.path.isfile(filename):
        resetglobal()
        global engine
        global session
        global session_factory
        engine = create_engine(filename)
        session = Session()
        session_factory = sessionmaker(bind=engine)
        from items_control import orm
        orm.Base.metadata.create_all(engine)


def getScopedSession():
    global session_factory
    global engine
    return scoped_session(session_factory)


def resetglobal():
    global engine
    global session
    engine = None
    session = None
    if hasattr(Engine, 'instance'):
        del Engine.instance
    if hasattr(Session, 'instance'):
        del Session.instance

class Session(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = sessionmaker(bind=engine)

        return cls.instance


class Engine(object):

    def __new__(cls, filename, debug=False):
        # filename = "/items_control/data/db.sqlite"

        if filename is None:
            filename = "/items_control/data/db.sqlite"

        # if not hasattr(cls, 'filename'):
        #     cls.filename = filename
        # else:
        #     if cls.filename != filename:
        #         cls.filename = filename
        #         del cls.instance

        if not hasattr(cls, 'instance'):
            cls.instance = create_engine('sqlite:///%s' % filename, echo=debug)

        return cls.instance


engine = None
session = None
session_factory = None
