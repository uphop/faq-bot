from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base

class Snapshot(Base):
    __tablename__ = "snapshot"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"))
    created = Column(String)
    published = Column(String, nullable=True)
    broadcast_id = Column(String, nullable=True)
    broadcast_name = Column(String, nullable=True)
    broadcast_url = Column(String, nullable=True)

    def __init__(self, id, user_id, created, published, broadcast_id, broadcast_name, broadcast_url):
        self.id = id
        self.user_id = user_id
        self.created = created
        self.published = published
        self.broadcast_id = broadcast_id
        self.broadcast_name = broadcast_name
        self.broadcast_url = broadcast_url