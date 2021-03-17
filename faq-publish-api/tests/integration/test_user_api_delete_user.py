import unittest
import os
import names
import uuid
import requests
import json

class TestDeleteUser(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/user'

    def tearDown(self):
        pass

    def test_delete_user_sunny_day(self):
        # create user
        user_name = names.get_full_name()
        payload = {
            'name': user_name
        }
        response_1 = requests.post(self.API_URL, json=payload)
        self.assertIsNotNone(response_1)
        self.assertTrue(response_1.status_code == 201)
        body = response_1.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertTrue(len(body['id']) > 0)
        id = body['id']

        # delete user
        response_2 = requests.delete(self.API_URL + '/' + id)
        self.assertIsNotNone(response_2)
        self.assertTrue(response_2.status_code == 204)

    def test_delete_user_nonexisting_user(self):
        nonexisting_user_id = str(uuid.uuid4())
        response = requests.delete(self.API_URL + '/' + nonexisting_user_id)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 404)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Not found')

if __name__ == '__main__':
    unittest.main()
