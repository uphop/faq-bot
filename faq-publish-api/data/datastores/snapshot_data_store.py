import os
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from data.models.snapshot_model import Snapshot
from data.models.topic_model import Topic
from data.models.snapshot_topic_model import SnapshotTopic
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)

class SnapshotDataStore:
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

    def create_snapshot(self, user_id, id, created, topics):
        # insert into data store and commit
        session = self.get_session()
        session.add(Snapshot(user_id=user_id, id=id, created=created, published=None, broadcast_name=None))
        for topic in topics:
            session.add(SnapshotTopic(snapshot_id=id, topic_id=topic['id']))
        session.commit()

    def get_snapshots(self, user_id):
        # select all snapshots
        return self.session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published, Snapshot.broadcast_name).filter(Snapshot.user_id == user_id)

    def get_snapshot_by_id(self, user_id, id):
        # select snapshot by ID
        session = self.get_session()
        return session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published, Snapshot.broadcast_name).filter(Snapshot.user_id == user_id, Snapshot.id == id).one_or_none()

    def get_snapshot_topics_by_id(self, user_id, id):
        # select snapshot topics by ID
        session = self.get_session()
        return session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Snapshot.user_id == user_id, Snapshot.id == id, SnapshotTopic.snapshot_id == Snapshot.id, SnapshotTopic.topic_id == Topic.id).all()

    def delete_snapshot(self, user_id, id):
        # delete record from data store and commit
        session = self.get_session()
        session.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.id == id).delete()
        session.query(SnapshotTopic).filter(SnapshotTopic.snapshot_id == id).delete()
        session.commit()
    
    def update_snapshot(self, user_id, id, published, broadcast_name):
        # update record in data store and commit
        session = self.get_session()
        snapshot = session.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.id == id).one_or_none()
        snapshot.published = published
        snapshot.broadcast_name = broadcast_name
        session.commit()


