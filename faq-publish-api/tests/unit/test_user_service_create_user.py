import unittest
import os
import uuid
import names
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestCreateUser(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()

    def tearDown(self):
        self.user_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_create_user_sunny_day(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # check if ID is UUID
        try:
            uuid_obj = uuid.UUID(user_id, version=4)
        except ValueError:
            self.fail('Expected UUID, but got something else.')
        
        # get new user and check if all fields are the same as expected
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertTrue(user['id'] == user_id)
        self.assertTrue(user['name'] == user_name)
        self.assertTrue('created' in user)

    def test_create_user_existing_name(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # now try to create user with the same name
        user_id_2 = self.user_service.create_user(user_name)
        # check if ID is not generated
        self.assertIsNotNone(user_id_2)
        self.assertTrue(user_id == user_id_2)

    def test_create_user_empty_name(self):
        user_id = self.user_service.create_user(None)
        # check if ID is not generated
        self.assertIsNone(user_id)

        user_id = self.user_service.create_user('')
        # check if ID is not generated
        self.assertIsNone(user_id)

        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()

