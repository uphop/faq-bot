import unittest
import os
import names
import requests
import json

class TestCreateUser(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/user'

    def tearDown(self):
        pass

    def test_create_user_sunny_day(self):
        user_name = names.get_full_name()
        payload = {
            'name': user_name
        }

        response = requests.post(self.API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 201)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertTrue(len(body['id']) > 0)

    def test_create_user_empty_payload(self):
        response = requests.post(self.API_URL)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 400)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Misunderstood')

    def test_create_user_missing_name(self):
        payload = {}
        response = requests.post(self.API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 400)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Misunderstood')

if __name__ == '__main__':
    unittest.main()
