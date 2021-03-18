from data.datastores.session_helper import SessionHelper
from data.models.meta import Base
from data.models.user_model import User
import logging
logger = logging.getLogger(__name__)

class UserDataStore:
    def create_user(self, id, name, created, sender_id):
        # insert into data store and commit
        session = SessionHelper().get_session()
        session.add(User(id=id, name=name, created=created, sender_id=sender_id))
        session.commit()

    def get_users(self):
        # select all users
        session = SessionHelper().get_session()
        return session.query(User.id, User.name, User.created, User.sender_id).all()

    def get_user_by_id(self, id):
        # select user by ID
        session = SessionHelper().get_session()
        return session.query(User.id, User.name, User.created, User.sender_id).filter(User.id == id).one_or_none()

    def get_user_by_name(self, name):
        # select user by full name
        session = SessionHelper().get_session()
        return session.query(User.id, User.name, User.created, User.sender_id).filter(User.name == name)

    def get_user_by_sender_id(self, sender_id):
        # select user by sender ID
        session = SessionHelper().get_session()
        return session.query(User.id, User.name, User.created, User.sender_id).filter(User.sender_id == sender_id).one_or_none()

    def delete_user(self, id):
        # delete record from data store and commit
        session = SessionHelper().get_session()
        session.query(User).filter(User.id == id).delete()
        session.commit()

    def update_user(self, id, sender_id):
        # update record in data store and commit
        session = SessionHelper().get_session()
        user = session.query(User).filter(User.id == id).one_or_none()
        user.sender_id = sender_id
        session.commit()


