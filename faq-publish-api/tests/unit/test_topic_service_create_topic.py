import unittest
import os
import uuid
import names
import random
from services.topic_service import TopicService
from services.user_service import UserService
from dotenv import load_dotenv
load_dotenv()

class TestCreateTopic(unittest.TestCase):
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

    def test_create_topic_sunny_day(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()

        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        
        # check if ID is generated
        self.assertIsNotNone(topic_id)

        # check if ID is UUID
        try:
            uuid_obj = uuid.UUID(topic_id, version=4)
        except ValueError:
            self.fail('Expected UUID, but got something else.')

        # get new topic and check if all fields are the same as expected
        topic = self.topic_service.get_topic_by_id(self.user_id, topic_id)
        self.assertIsNotNone(topic)
        self.assertTrue(topic['user_id'] == self.user_id)
        self.assertTrue(topic['id'] == topic_id)
        self.assertTrue(topic['question'] == question)
        self.assertTrue(topic['answer'] == answer)
        self.assertTrue('created' in topic)

    def test_create_topic_nonexisting_user(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()

        nonexisting_user_id = str(uuid.uuid4())
        topic_id = self.topic_service.create_topic(nonexisting_user_id, question, answer)
        
        # check if ID is generated
        self.assertIsNone(topic_id)

    def test_create_topic_empty_user_id(self):
        question = self.make_random_sentence()
        answer = self.make_random_sentence()

        empty_user_id = ''
        topic_id = self.topic_service.create_topic(empty_user_id, question, answer)
        
        # check if ID is generated
        self.assertIsNone(topic_id)

    def test_create_topic_empty_question(self):
        question = ''
        answer = self.make_random_sentence()

        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        
        # check if ID is generated
        self.assertIsNone(topic_id)

    def test_create_topic_empty_answer(self):
        question = self.make_random_sentence()
        answer = None

        topic_id = self.topic_service.create_topic(self.user_id, question, answer)
        
        # check if ID is generated
        self.assertIsNone(topic_id)


    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])

if __name__ == '__main__':
    unittest.main()

