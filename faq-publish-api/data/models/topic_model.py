from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base

class Topic(Base):
    __tablename__ = "topic"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"))
    question = Column(String)
    answer = Column(String)
    created = Column(String)

    def __init__(self, id, user_id, question, answer, created):
        self.id = id
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.created = created