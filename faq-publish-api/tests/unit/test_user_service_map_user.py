import unittest
import os
import uuid
import names
import random
from datetime import datetime, timedelta
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestMapUser(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()

    def tearDown(self):
        self.user_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_map_user(self):
        id = str(uuid.uuid4())
        name = names.get_full_name()
        created = datetime.now().timestamp()

        user = self.user_service.map_user(id, name, created)
        self.assertIsNotNone(user)
        self.assertTrue(user['id'] == id)
        self.assertTrue(user['name'] == name)
        self.assertTrue(user['created'] == created)

if __name__ == '__main__':
    unittest.main()

