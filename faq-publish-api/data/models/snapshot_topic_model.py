from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base

class SnapshotTopic(Base):
    __tablename__ = "snapshot_topic"
    snapshot_id = Column(String, ForeignKey("snapshot.id"), primary_key = True)
    topic_id = Column(String, ForeignKey("topic.id"), primary_key = True)
    
    def __init__(self, snapshot_id, topic_id):
        self.snapshot_id = snapshot_id
        self.topic_id = topic_id