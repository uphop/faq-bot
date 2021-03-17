import unittest
import os
import uuid
import names
import random
from services.topic_service import TopicService
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestDeleteTopic(unittest.TestCase):
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

    def test_delete_topic_sunny_day(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        topic = self.topic_service.get_topic_by_id(self.user_id, topic_id)
        self.assertIsNotNone(topic)

        # delete topic by id
        returned_id = self.topic_service.delete_topic(self.user_id, topic_id)
        self.assertIsNotNone(returned_id)
        self.assertTrue(returned_id == topic_id)

        # get deleted topic
        topic = self.topic_service.get_topic_by_id(self.user_id, topic_id)
        self.assertIsNone(topic)

    def test_delete_topic_double_delete(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        topic = self.topic_service.get_topic_by_id(self.user_id, topic_id)
        self.assertIsNotNone(topic)

        # delete topic by id
        returned_id = self.topic_service.delete_topic(self.user_id, topic_id)
        self.assertIsNotNone(returned_id)
        self.assertTrue(returned_id == topic_id)

        # get deleted topic
        topic = self.topic_service.get_topic_by_id(self.user_id, topic_id)
        self.assertIsNone(topic)

        # delete topic by id
        returned_id = self.topic_service.delete_topic(self.user_id, topic_id)
        self.assertIsNone(returned_id)

    def test_delete_topic_nonexisting_user(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        # delete topic by id
        nonexisting_user_id = str(uuid.uuid4())
        returned_id = self.topic_service.delete_topic(nonexisting_user_id, topic_id)
        self.assertIsNone(returned_id)

    def test_delete_topic_empty_user_id(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        # delete topic by id
        empty_user_id = ''
        returned_id = self.topic_service.delete_topic(empty_user_id, topic_id)
        self.assertIsNone(returned_id)

    def test_delete_topic_nonexisting_topic(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        # delete topic by id
        nonexisting_topic_id = str(uuid.uuid4())
        returned_id = self.topic_service.delete_topic(self.user_id, nonexisting_topic_id)
        self.assertIsNone(returned_id)

    def test_delete_topic_empty_topic_id(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        self.assertIsNotNone(topic_id)

        # delete topic by id
        empty_topic_id = None
        returned_id = self.topic_service.delete_topic(self.user_id, empty_topic_id)
        self.assertIsNone(returned_id)

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])

if __name__ == '__main__':
    unittest.main()

