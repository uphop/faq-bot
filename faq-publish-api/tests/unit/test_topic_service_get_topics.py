import unittest
import os
import uuid
import names
import random
from services.topic_service import TopicService
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestGetTopics(unittest.TestCase):
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

    def test_get_topics_sunny_day(self):
        question_1 = self.make_random_sentence()
        answer_1 = self.make_random_sentence()
        topic_id_1 = self.topic_service.create_topic(self.user_id, question_1, answer_1)
        self.assertIsNotNone(topic_id_1)

        question_2 = self.make_random_sentence()
        answer_2 = self.make_random_sentence()
        topic_id_2 = self.topic_service.create_topic(self.user_id, question_2, answer_2)
        self.assertIsNotNone(topic_id_2)

        # get new topic and check if all fields are the same as expected
        topics = self.topic_service.get_topics(self.user_id)
        self.assertIsNotNone(topics)
        self.assertTrue(len(topics) == 2)
        for topic in topics:
            self.assertTrue(topic['user_id'] == self.user_id)
            self.assertTrue(topic['id'] in [topic_id_1, topic_id_2])
            self.assertTrue('question' in topic)
            self.assertTrue('answer' in topic)
            self.assertTrue('created' in topic)

    def test_get_topics_empty_list(self):
        topics = self.topic_service.get_topics(self.user_id)
        self.assertIsNotNone(topics)
        self.assertTrue(len(topics) == 0)

    def test_get_topics_nonexisting_user(self):
        nonexisting_user_id = str(uuid.uuid4())
        topics = self.topic_service.get_topics(nonexisting_user_id)
        self.assertIsNone(topics)

    def test_get_topics_empty_user_id(self):
        empty_user_id = ''
        topics = self.topic_service.get_topics(empty_user_id)
        self.assertIsNone(topics)

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])

if __name__ == '__main__':
    unittest.main()

