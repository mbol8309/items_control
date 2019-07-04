import sqlalchemy

class Session(object):

   def __new__(cls):

       if not hasattr(cls, 'instance'):

           cls.instance = sqlalchemy.orm.sessionmaker(bind=engine)

       return cls.instance

class Engine(object):

   def __new__(cls):

       if not hasattr(cls, 'instance'):

           cls.instance = sqlalchemy.create_engine('sqlite:///items_control/data/db.sqlite')

       return cls.instance



engine = Engine()
session = Session()




