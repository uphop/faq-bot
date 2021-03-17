import os
import logging
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from data.models.topic_model import Topic
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)

class TopicDataStore:
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
        
    def create_topic(self, user_id, id, question, answer, created):
        # insert into data store and commit
        session = self.get_session()
        session.add(Topic(user_id=user_id, id=id, question=question, answer=answer, created=created))
        session.commit()

    def get_topics(self, user_id):
        # select all topics
        session = self.get_session()
        session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id)

    def get_topic_by_id(self, user_id, id):
        # select user by ID
        session = self.get_session()
        return session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id, Topic.id == id).one_or_none()

    def delete_topic(self, user_id, id):
        # delete record from data store and commit
        session = self.get_session()
        session.query(Topic).filter(Topic.user_id == user_id, Topic.id == id).delete()
        session.commit()


