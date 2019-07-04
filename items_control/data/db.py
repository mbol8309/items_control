import sqlalchemy
import os

def open_db(filename):
    if os.path.isfile(filename):
        engine=Engine(filename)
        session=Session()

def create_db(filename):
    if not os.path.isfile(filename):
        engine=Engine(filename)
        session=Session()
        from items_control import orm
        orm.Base.metadata.create_all(engine)

class Session(object):

   def __new__(cls):

       if not hasattr(cls, 'instance'):

           cls.instance = sqlalchemy.orm.sessionmaker(bind=engine)

       return cls.instance

class Engine(object):

   def __new__(cls,filename): is None:
       filename = "/items_control/data/db.sqlite"

       if filename is None:
           filename = "/items_control/data/db.sqlite"

       if not hasattr(cls, 'instance'):

           cls.instance = sqlalchemy.create_engine('sqlite://%s' % filename)

       return cls.instance

engine = Engine(None)
session = Session()




