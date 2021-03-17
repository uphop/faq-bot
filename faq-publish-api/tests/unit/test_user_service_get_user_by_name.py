import unittest
import os
import uuid
import names
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestGetUserByName(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()

    def tearDown(self):
        self.user_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_get_user_by_name_sunny_day(self):
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

        # get user by name and check all fields
        user_list_1 = self.user_service.get_user_by_name(user_name_1)
        self.assertIsNotNone(user_list_1)
        self.assertTrue(len(user_list_1) == 1)
        
        user_1 = user_list_1[0]
        self.assertTrue(user_1['id'] == user_id_1)
        self.assertTrue(user_1['name'] == user_name_1)
        self.assertTrue('created' in user_1)

        user_list_2 = self.user_service.get_user_by_name(user_name_2)
        self.assertIsNotNone(user_list_2)
        self.assertTrue(len(user_list_2) == 1)
        
        user_2 = user_list_2[0]
        self.assertTrue(user_2['id'] == user_id_2)
        self.assertTrue(user_2['name'] == user_name_2)
        self.assertTrue('created' in user_2)

    def test_get_user_by_name_nonexisting(self):
        # create user 1
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        nonexisting_user_name = names.get_full_name()
        
        # get user by name and check if does not exist
        user_list = self.user_service.get_user_by_name(nonexisting_user_name)
        self.assertIsNotNone(user_list)
        self.assertTrue(len(user_list) == 0)

    def test_get_user_by_name_empty_name(self):
        # create user 1
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        empty_user_name = ''
        
        # get user by name and check if does not exist
        user_list = self.user_service.get_user_by_name(empty_user_name)
        self.assertIsNone(user_list)

        empty_user_name = None
        
        # get user by name and check if does not exist
        user_list = self.user_service.get_user_by_name(empty_user_name)
        self.assertIsNone(user_list)

    def test_get_user_by_name_empty_list(self):
        nonexisting_user_name = names.get_full_name()
        
        # get user by name and check if does not exist
        user_list = self.user_service.get_user_by_name(nonexisting_user_name)
        self.assertIsNotNone(user_list)
        self.assertTrue(len(user_list) == 0)


if __name__ == '__main__':
    unittest.main()

