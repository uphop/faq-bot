import unittest
import os
import names
import uuid
import requests
import json

class TestGetUserById(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/user'

    def tearDown(self):
        pass

    def test_get_user_by_id_sunny_day(self):
        # create user
        user_name = names.get_full_name()
        payload_1 = {
            'name': user_name
        }
        response_1 = requests.post(self.API_URL, json=payload_1)
        self.assertIsNotNone(response_1)
        self.assertTrue(response_1.status_code == 201)
        body_1 = response_1.json()
        self.assertIsNotNone(body_1)
        self.assertIsNotNone(body_1['id'])
        self.assertTrue(len(body_1['id']) > 0)
        id = body_1['id']

        # retrieve user by id
        response_2 = requests.get(self.API_URL + '/' + id)
        self.assertIsNotNone(response_2)
        self.assertTrue(response_2.status_code == 200)
        body_2 = response_2.json()
        self.assertIsNotNone(body_2)
        self.assertTrue(body_2['id'] == id)
        self.assertTrue(body_2['name'] == user_name)
        self.assertTrue('created' in body_2)

    def test_get_user_by_id_nonexisting_user(self):
        # create user
        user_name = names.get_full_name()
        payload_1 = {
            'name': user_name
        }
        response_1 = requests.post(self.API_URL, json=payload_1)
        self.assertIsNotNone(response_1)
        self.assertTrue(response_1.status_code == 201)
        body_1 = response_1.json()
        self.assertIsNotNone(body_1)
        self.assertIsNotNone(body_1['id'])
        self.assertTrue(len(body_1['id']) > 0)
        id = body_1['id']

        # retrieve user by id
        nonexisting_user_id = str(uuid.uuid4())
        response_2 = requests.get(self.API_URL + '/' + nonexisting_user_id)
        self.assertIsNotNone(response_2)
        self.assertTrue(response_2.status_code == 404)
        
        body_2 = response_2.json()
        self.assertIsNotNone(body_2)
        self.assertIsNotNone(body_2['error'])
        self.assertTrue(body_2['error'] == 'Not found')

if __name__ == '__main__':
    unittest.main()
