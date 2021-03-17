import unittest
import os
import uuid
import names
import random
from services.topic_service import TopicService
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestGetTopicById(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.user_service = UserService()
        self.topic_service = TopicService()

        self.user_name = names.get_full_name()
        self.user_id = self.user_service.create_user(self.user_name)

    def tearDown(self):
        self.user_service = None
        self.topic_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_get_topic_by_id_sunny_day(self):
        question_1 = self.make_random_sentence()
        answer_1 = self.make_random_sentence()
        topic_id_1 = self.topic_service.create_topic(self.user_id, question_1, answer_1)
        self.assertIsNotNone(topic_id_1)

        question_2 = self.make_random_sentence()
        answer_2 = self.make_random_sentence()
        topic_id_2 = self.topic_service.create_topic(self.user_id, question_2, answer_2)
        self.assertIsNotNone(topic_id_2)

        # get new topic and check if all fields are the same as expected
        topic_1 = self.topic_service.get_topic_by_id(self.user_id, topic_id_1)
        self.assertIsNotNone(topic_1)
        self.assertTrue(topic_1['user_id'] == self.user_id)
        self.assertTrue(topic_1['id'] == topic_id_1)
        self.assertTrue(topic_1['question'] == question_1)
        self.assertTrue(topic_1['answer'] == answer_1)
        self.assertTrue('created' in topic_1)

        topic_2 = self.topic_service.get_topic_by_id(self.user_id, topic_id_2)
        self.assertIsNotNone(topic_1)
        self.assertTrue(topic_2['user_id'] == self.user_id)
        self.assertTrue(topic_2['id'] == topic_id_2)
        self.assertTrue(topic_2['question'] == question_2)
        self.assertTrue(topic_2['answer'] == answer_2)
        self.assertTrue('created' in topic_2)

    def test_get_topic_by_id_nonexisting_user(self):
        question_1 = self.make_random_sentence()
        answer_1 = self.make_random_sentence()
        topic_id_1 = self.topic_service.create_topic(self.user_id, question_1, answer_1)
        self.assertIsNotNone(topic_id_1)

        nonexisting_user_id = str(uuid.uuid4())
        topic_1 = self.topic_service.get_topic_by_id(nonexisting_user_id, topic_id_1)
        self.assertIsNone(topic_1)

    def test_get_topics_empty_user_id(self):
        question_1 = self.make_random_sentence()
        answer_1 = self.make_random_sentence()
        topic_id_1 = self.topic_service.create_topic(self.user_id, question_1, answer_1)
        self.assertIsNotNone(topic_id_1)

        empty_user_id = ''
        topic_1 = self.topic_service.get_topic_by_id(empty_user_id, topic_id_1)
        self.assertIsNone(topic_1)

    def test_get_topic_by_id_nonexisting_topic(self):
        question_1 = self.make_random_sentence()
        answer_1 = self.make_random_sentence()
        topic_id_1 = self.topic_service.create_topic(self.user_id, question_1, answer_1)
        self.assertIsNotNone(topic_id_1)

        nonexisting_topic_id = str(uuid.uuid4())
        topic_1 = self.topic_service.get_topic_by_id(self.user_id, nonexisting_topic_id)
        self.assertIsNone(topic_1)

    def test_get_topics_empty_topic_id(self):
        empty_topic_id = None
        topic_1 = self.topic_service.get_topic_by_id(self.user_id, empty_topic_id)
        self.assertIsNone(topic_1)

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])

if __name__ == '__main__':
    unittest.main()

