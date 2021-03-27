import os
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SessionHelper(metaclass=Singleton):
    def __init__(self):
        self.session = None
        
    def get_session(self):
        if self.session is None:
            # init engine
            USER_TOPICS_DATASTORE_CONNECTION_STRING = os.environ.get('USER_TOPICS_DATASTORE_CONNECTION_STRING', 'sqlite:///data//datastores/local.sqlite3?check_same_thread=False')
            engine = create_engine(USER_TOPICS_DATASTORE_CONNECTION_STRING)

            # create all tables in the engine
            Base.metadata.create_all(engine)

            # bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
            Base.metadata.bind = engine

            # init database session
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
        
        return self.session