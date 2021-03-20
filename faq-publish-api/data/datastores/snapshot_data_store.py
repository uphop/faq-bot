from data.datastores.session_helper import SessionHelper
from data.models.snapshot_model import Snapshot
from data.models.topic_model import Topic
from data.models.snapshot_topic_model import SnapshotTopic
import logging
logger = logging.getLogger(__name__)

class SnapshotDataStore:
    def create_snapshot(self, user_id, id, created, topics):
        # insert into data store and commit
        session = SessionHelper().get_session()
        session.add(Snapshot(user_id=user_id, id=id, created=created, published=None, broadcast_id=None, broadcast_name=None, broadcast_url=None))
        session.commit()
        for topic in topics:
            session.add(SnapshotTopic(snapshot_id=id, topic_id=topic['id']))
        session.commit()

    def get_snapshots(self, user_id):
        # select all snapshots
        session = SessionHelper().get_session()
        return session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published, Snapshot.broadcast_id, Snapshot.broadcast_name, Snapshot.broadcast_url).filter(Snapshot.user_id == user_id).all()

    def get_snapshot_by_id(self, user_id, id):
        # select snapshot by ID
        session = SessionHelper().get_session()
        return session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published, Snapshot.broadcast_id, Snapshot.broadcast_name, Snapshot.broadcast_url).filter(Snapshot.user_id == user_id, Snapshot.id == id).one_or_none()

    def get_snapshot_topics_by_id(self, user_id, id):
        # select snapshot topics by ID
        session = SessionHelper().get_session()
        return session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Snapshot.user_id == user_id, Snapshot.id == id, SnapshotTopic.snapshot_id == Snapshot.id, SnapshotTopic.topic_id == Topic.id).all()

    def delete_snapshot(self, user_id, id):
        # delete record from data store and commit
        session = SessionHelper().get_session()
        session.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.id == id).delete()
        session.query(SnapshotTopic).filter(SnapshotTopic.snapshot_id == id).delete()
        session.commit()
    
    def update_snapshot(self, user_id, id, published, broadcast_id, broadcast_name, broadcast_url):
        # update record in data store and commit
        session = SessionHelper().get_session()
        snapshot = session.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.id == id).one_or_none()
        snapshot.published = published
        snapshot.broadcast_id = broadcast_id
        snapshot.broadcast_name = broadcast_name
        snapshot.broadcast_url = broadcast_url
        session.commit()


