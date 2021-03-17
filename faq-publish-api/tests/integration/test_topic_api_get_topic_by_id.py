import unittest
import os
import names
import uuid
import requests
import json
import random

class TestGetTopicById(unittest.TestCase):
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

    def create_topic(self, user_id):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        payload = {
            'question': question,
            'answer': answer
        }
        response = requests.post(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL, json=payload)
        return response.json()['id']

    def test_get_topic_by_id_sunny_day(self):
        user_id = self.create_user()
        topic_id = self.create_topic(user_id)
        response = requests.get(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL + '/' + topic_id)
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertTrue(body['id'] == topic_id)
        self.assertIsNotNone(body['user_id'])
        self.assertTrue(body['user_id'] == user_id)
        self.assertIsNotNone(body['question'])
        self.assertTrue(len(body['question']) > 0)
        self.assertIsNotNone(body['answer'])
        self.assertTrue(len(body['answer']) > 0)
        self.assertIsNotNone(body['created'])
        self.assertTrue(len(body['created']) > 0)

    def test_get_topic_by_id_nonexisting_user(self):
        user_id = self.create_user()
        topic_id = self.create_topic(user_id)

        nonexisting_user_id = str(uuid.uuid4())
        response = requests.get(self.USER_API_URL + '/' + nonexisting_user_id + self.TOPIC_API_URL + '/' + topic_id)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 404)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Not found')

    def test_get_topic_by_id_nonexisting_topic(self):
        user_id = self.create_user()
        topic_id = self.create_topic(user_id)

        nonexisting_topic_id = str(uuid.uuid4())
        response = requests.get(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL + '/' + nonexisting_topic_id)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 404)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Not found')

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])


if __name__ == '__main__':
    unittest.main()
