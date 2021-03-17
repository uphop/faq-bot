import unittest
import os
import names
import uuid
import requests
import json
import random

class TestGetTopics(unittest.TestCase):
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

    def test_get_topics_sunny_day(self):
        user_id = self.create_user()
        topic_id_1 = self.create_topic(user_id)
        topic_id_2 = self.create_topic(user_id)
        response = requests.get(self.USER_API_URL + '/' + user_id + self.TOPIC_API_URL)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(len(body) == 2)
        for topic in body:
            self.assertIsNotNone(topic['id'])
            self.assertTrue(topic['id'] in [topic_id_1, topic_id_2])
            self.assertIsNotNone(topic['user_id'])
            self.assertTrue(topic['user_id'] == user_id)
            self.assertIsNotNone(topic['question'])
            self.assertTrue(len(topic['question']) > 0)
            self.assertIsNotNone(topic['answer'])
            self.assertTrue(len(topic['answer']) > 0)
            self.assertIsNotNone(topic['created'])
            self.assertTrue(len(topic['created']) > 0)

    def test_get_topics_nonexisting_user(self):
        nonexisting_user_id = str(uuid.uuid4())
        response = requests.get(self.USER_API_URL + '/' + nonexisting_user_id + self.TOPIC_API_URL)

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
