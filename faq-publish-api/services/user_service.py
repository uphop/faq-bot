import os
import uuid
from datetime import datetime, timedelta
import requests
from data.datastores.user_data_store import UserDataStore
import logging
logger = logging.getLogger(__name__)

'''
Manages user entity.
'''
class UserService:
    def __init__(self):
        # init data store
        self.data_store = UserDataStore()

        # load configuration
        self.CAPTURE_BOT_BASE_URL = os.getenv('CAPTURE_BOT_BASE_URL', 'http://localhost:5005')

    def create_user(self, name, sender_id):
        """Creates a new user.
        @param name: the full user's name
        @param sender_id: sender identifier
        """
        # check if name is passed
        if not name or len(name) == 0:
            logger.error('Name is not passed.')
            return
        
        # check if sender_id is passed
        if not sender_id or len(sender_id) == 0:
            logger.error('Sender ID is not passed.')
            return

        # check if name not taken yet
        user_with_same_name = self.get_user_by_name(name)
        if len(user_with_same_name) == 1:
            logger.error('Duplicate name is found: ' + str(name))
            return user_with_same_name[0]['id']
        elif len(user_with_same_name) > 1:
            logger.error('Multiple names are found: ' + str(name))
            return

        # generate new user identifier and add to data store
        id = str(uuid.uuid4())
        self.data_store.create_user(id, name, datetime.now().timestamp(), sender_id)
        logger.debug('Created new user ' + str(id))
        return id

    def get_users(self):
        """Return all users.
        """
        # retrieve all users from data store, convert to list and return
        results = self.data_store.get_users()
        return [self.map_user(id, name, created, sender_id) for id, name, created, sender_id, in results]

    def get_user_by_id(self, id):
        """Get user by identifier.
        @param id: user's ID
        """
        # check if ID is passed
        if not id or len(id) == 0:
            logger.error('User ID is not passed.')
            return

        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_id(id)
        if not result is None:
            return self.map_user(result.id, result.name, result.created, result.sender_id)

    def get_user_by_name(self, name):
        """Get user by name.
        @param name: user's full name
        """
        # check if name is passed
        if not name or len(name) == 0:
            logger.error('Name is not passed.')
            return

        # retrieve user from data store by full name
        results = self.data_store.get_user_by_name(name)
        return [self.map_user(id, name, created, sender_id) for id, name, created, sender_id, in results] if not results is None else []

    def get_user_by_sender_id(self, sender_id):
        """Get user by sender ID.
        @param sender_id: user's sender ID
        """
        # check if ID is passed
        if not sender_id or len(sender_id) == 0:
            logger.error('User sender ID is not passed.')
            return

        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_sender_id(sender_id)
        if not result is None:
            return self.map_user(result.id, result.name, result.created, result.sender_id)

    def delete_user(self, id):
        """Delete user by identifier.
        @param id: user's ID
        """
        # check if ID is passed
        if not id or len(id) == 0:
            logger.error('User ID is not passed.')
            return
            
        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_id(id)
        if not result is None:
            # delete user from data store by ID
            self.data_store.delete_user(id)
            logger.debug('Deleted user ' + str(id))
            return id

    def update_user(self, id, sender_id):
        """Update user by identifier.
        @param id: user's ID
        @param sender_id: user's sender_id
        """
        # check if ID is passed
        if not id or len(id) == 0:
            logger.error('User ID is not passed.')
            return

        # check if sender_id is passed
        if not sender_id or len(sender_id) == 0:
            logger.error('Sender_id is not passed.')
            return
            
        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_id(id)
        if not result is None:
            # update user in data store by ID
            self.data_store.update_user(id, sender_id)
            logger.debug('Updated user ' + str(id))
            return id

    def notify_user_snapshot_updated(self, id, broadcast_name):
        user = self.get_user_by_id(id)

        # prepare request
        request_url = f"{self.CAPTURE_BOT_BASE_URL}/conversations/{user['sender_id']}/trigger_intent?output_channel=latest"
        payload = {
            'name': 'external_notify_snapshot_published',
            'entities': {
                'broadcast_name': broadcast_name
            }
        }

        # call publish API
        try:
            response = requests.post(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200:
            return

    def map_user(self, id, name, created, sender_id):
        """Maps data store row to dict.
        """
        return {'id': id, 'name': name, 'created': created, 'sender_id': sender_id}
