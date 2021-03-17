import unittest
import os
import names
import requests
import json

class TestGetUsers(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/user'

    def tearDown(self):
        pass

    def test_get_users_sunny_day(self):
        # create users
        user_name_1 = names.get_full_name()
        payload_1 = {
            'name': user_name_1
        }
        response_1 = requests.post(self.API_URL, json=payload_1)
        self.assertIsNotNone(response_1)
        self.assertTrue(response_1.status_code == 201)
        body_1 = response_1.json()
        self.assertIsNotNone(body_1)
        self.assertIsNotNone(body_1['id'])
        self.assertTrue(len(body_1['id']) > 0)
        id_1 = body_1['id']

        user_name_2 = names.get_full_name()
        payload_2 = {
            'name': user_name_2
        }
        response_2 = requests.post(self.API_URL, json=payload_2)
        self.assertIsNotNone(response_2)
        self.assertTrue(response_2.status_code == 201)
        body_2 = response_2.json()
        self.assertIsNotNone(body_2)
        self.assertIsNotNone(body_2['id'])
        self.assertTrue(len(body_2['id']) > 0)
        id_2 = body_2['id']

        # retrieve users
        response_3 = requests.get(self.API_URL)
        self.assertIsNotNone(response_3)
        self.assertTrue(response_3.status_code == 200)
        body_3 = response_3.json()
        self.assertIsNotNone(body_3)
        self.assertTrue(len(body_3) >= 2)

        user_id_1_found = False
        user_id_2_found = False
        for user in body_3:
            if user['id'] == id_1:
                user_id_1_found = True
            if user['id'] == id_2:
                user_id_2_found = True
        self.assertTrue(user_id_1_found and user_id_2_found)

if __name__ == '__main__':
    unittest.main()
