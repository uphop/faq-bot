import unittest
import os
import uuid
import names
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestGetUsers(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()

    def tearDown(self):
        self.user_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_get_users_sunny_day(self):
        # create user 1
        user_name_1 = names.get_full_name()
        user_id_1 = self.user_service.create_user(user_name_1)

        # check if ID is generated
        self.assertIsNotNone(user_id_1)

        # create user 2
        user_name_2 = names.get_full_name()
        user_id_2 = self.user_service.create_user(user_name_2)

        # check if ID is generated
        self.assertIsNotNone(user_id_2)

        # get user list and check for user 1 and user 2
        users = self.user_service.get_users()
        self.assertIsNotNone(users)
        self.assertTrue(len(users) == 2)
        for user in users:
            self.assertTrue(user['id'] in [user_id_1, user_id_2])
            self.assertTrue('id' in user)
            self.assertTrue('name' in user)
            self.assertTrue('created' in user)

    def test_get_users_empty_list(self):
        # get user list and check that it is empty
        users = self.user_service.get_users()
        self.assertIsNotNone(users)
        self.assertTrue(len(users) == 0)

if __name__ == '__main__':
    unittest.main()

