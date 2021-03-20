from sqlalchemy import Column, String, Integer, Table, Sequence
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base
from data.models.topic_model import Topic

class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    spot_id = Column(Integer, default=Sequence('spot_id_seq', metadata=Base.metadata), nullable=False)
    name = Column(String)
    created = Column(String)
    topics = relationship("Topic", backref=backref("user"))
    sender_id = Column(String, nullable=True)

    def __init__(self, id, name, created, sender_id):
        self.id = id
        self.name = name
        self.created = created
        self.sender_id = sender_id