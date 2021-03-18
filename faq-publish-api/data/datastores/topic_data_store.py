from data.datastores.session_helper import SessionHelper
from data.models.topic_model import Topic
import logging
logger = logging.getLogger(__name__)

class TopicDataStore:        
    def create_topic(self, user_id, id, question, answer, created):
        # insert into data store and commit
        session = SessionHelper().get_session()
        session.add(Topic(user_id=user_id, id=id, question=question, answer=answer, created=created))
        session.commit()

    def get_topics(self, user_id):
        # select all topics
        session = SessionHelper().get_session()
        return session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id).all()

    def get_topic_by_id(self, user_id, id):
        # select user by ID
        session = SessionHelper().get_session()
        return session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id, Topic.id == id).one_or_none()

    def delete_topic(self, user_id, id):
        # delete record from data store and commit
        session = SessionHelper().get_session()
        session.query(Topic).filter(Topic.user_id == user_id, Topic.id == id).delete()
        session.commit()


