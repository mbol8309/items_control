from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


def open_db(filename):
    if os.path.isfile(filename):
        resetglobal()
        global engine
        global session
        engine = Engine(filename)
        session = Session()


def create_db(filename):
    if not os.path.isfile(filename):
        resetglobal()
        global engine
        global session
        engine = Engine(filename)
        session = Session()
        from items_control import orm
        orm.Base.metadata.create_all(engine)


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

    def __new__(cls, filename):
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
            cls.instance = create_engine('sqlite:///%s' % filename)

        return cls.instance


engine = Engine(None)
session = Session()
