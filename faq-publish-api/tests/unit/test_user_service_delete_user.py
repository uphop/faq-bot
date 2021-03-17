import unittest
import os
import uuid
import names
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestDeleteUser(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()

    def tearDown(self):
        self.user_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_delete_user_sunny_day(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # get new user
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNotNone(user)

        # delete user by id
        returned_id = self.user_service.delete_user(user_id)
        self.assertIsNotNone(returned_id)
        self.assertTrue(returned_id == user_id)

        # get deleted user
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNone(user)

    def test_delete_user_double_delete(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # get new user
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNotNone(user)

        # delete user by id
        returned_id = self.user_service.delete_user(user_id)
        self.assertIsNotNone(returned_id)
        self.assertTrue(returned_id == user_id)

        # get deleted user
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNone(user)

        # delete user by id
        returned_id = self.user_service.delete_user(user_id)
        self.assertIsNone(returned_id)

    def test_delete_user_nonexisting(self):
        # create user 1
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # get new user
        user = self.user_service.get_user_by_id(user_id)
        self.assertIsNotNone(user)

        nonexisting_user_id = str(uuid.uuid4())
        
        # delete user by id
        returned_id = self.user_service.delete_user(nonexisting_user_id)
        self.assertIsNone(returned_id)

    def test_delete_user_empty_id(self):
        empty_user_id = ''
        
        # delete user by id
        returned_id = self.user_service.delete_user(empty_user_id)
        self.assertIsNone(returned_id)
        
        empty_user_id = None
        
        # delete user by id
        returned_id = self.user_service.delete_user(empty_user_id)
        self.assertIsNone(returned_id)

if __name__ == '__main__':
    unittest.main()

