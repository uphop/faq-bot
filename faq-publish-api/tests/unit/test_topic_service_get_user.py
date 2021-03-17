import unittest
import os
import uuid
import names
import random
from services.topic_service import TopicService
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestGetUser(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()
        self.topic_service = TopicService()

        self.user_name = names.get_full_name()
        self.user_id = self.user_service.create_user(self.user_name)

    def tearDown(self):
        self.user_service = None
        self.topic_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_get_user_sunny_day(self):
        user = self.topic_service.get_user(self.user_id)
        self.assertIsNotNone(user)

    def test_get_topics_nonexisting_user(self):
        nonexisting_user_id = str(uuid.uuid4())
        user = self.topic_service.get_user(nonexisting_user_id)
        self.assertIsNone(user)

    def test_get_topics_empty_user_id(self):
        empty_user_id = ''
        user = self.topic_service.get_user(empty_user_id)
        self.assertIsNone(user)
        
if __name__ == '__main__':
    unittest.main()

