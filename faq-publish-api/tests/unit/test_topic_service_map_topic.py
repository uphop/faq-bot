import unittest
import os
import uuid
import names
import random
from datetime import datetime, timedelta
from services.topic_service import TopicService
from dotenv import load_dotenv
load_dotenv()

class TestMapTopic(unittest.TestCase):
    LOCAL_DB_FILE = '/data//datastores/local_test.sqlite3'

    def setUp(self):
        os.environ['USER_TOPICS_DATASTORE_CONNECTION_STRING'] = 'sqlite://' + self.LOCAL_DB_FILE + '?check_same_thread=False'
        self.topic_service = TopicService()

    def tearDown(self):
        self.topic_service = None
        if os.path.exists('.' + self.LOCAL_DB_FILE):
            os.remove('.' + self.LOCAL_DB_FILE)

    def test_map_topic(self):
        user_id = str(uuid.uuid4())
        id = str(uuid.uuid4())
        question = self.make_random_sentence()
        answer = self.make_random_sentence()
        created = datetime.now().timestamp()

        topic = self.topic_service.map_topic(user_id, id, question, answer, created)
        self.assertIsNotNone(topic)
        self.assertTrue(topic['user_id'] == user_id)
        self.assertTrue(topic['id'] == id)
        self.assertTrue(topic['question'] == question)
        self.assertTrue(topic['answer'] == answer)
        self.assertTrue(topic['created'] == created)

    def make_random_sentence(self):
        nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
        verbs = ["runs", "hits", "jumps", "drives", "barfs"]
        adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
        adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

        random_entry = lambda x: x[random.randrange(len(x))]
        return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])

        
if __name__ == '__main__':
    unittest.main()

