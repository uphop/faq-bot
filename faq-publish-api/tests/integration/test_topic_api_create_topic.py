import unittest
import os
import names
import uuid
import requests
import json
import random

class TestCreateTopic(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        self.USER_API_URL = self.BASE_URL + '/user'
        self.TOPIC_API_URL = '/topic'

    def tearDown(self):
        pass

    def create_user(self):
        user_name = names.get_full_name()
        payload = {
            'name': user_name
        }
        response = requests.post(self.USER_API_URL, json=payload)
        return response.json()['id']

    def test_create_topic_sunny_day(self):
        user_id = self.create_user()
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        payload = {
            'question': question,
            'answer': answer
        }
        response = requests.post(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 201)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertTrue(len(body['id']) > 0)

    def test_create_topic_empty_payload(self):
        user_id = self.create_user()
        response = requests.post(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 400)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Misunderstood')

    def test_create_topic_missing_question(self):
        user_id = self.create_user()
        answer = self.make_random_sentence()
        payload = {
            'question': '',
            'answer': answer
        }
        response = requests.post(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 400)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Misunderstood')

    def test_create_topic_missing_answer(self):
        user_id = self.create_user()
        question = self.make_random_sentence()
        payload = {
            'question': question,
            'answer': ''
        }
        response = requests.post(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 400)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Misunderstood')

    def test_create_topic_nonexisting_user(self):
        nonexisting_user_id = str(uuid.uuid4())
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        payload = {
            'question': question,
            'answer': answer
        }
        response = requests.post(self.USER_API_URL + '/' + nonexisting_user_id + self.TOPIC_API_URL, json=payload)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 409)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Conflict')

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])


if __name__ == '__main__':
    unittest.main()
