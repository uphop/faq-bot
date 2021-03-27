import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)


'''
Braodcast queue client.
'''
class BroadcastQueueClient:
    def __init__(self):
        # init config
        self.CELERY_BROKER = os.environ.get('CELERY_BROKER', 'memory://localhost/')
        self.CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'publish_queue')

        # Init Celery broker
        self.broker = Celery('queues', broker=self.CELERY_BROKER)

    def submit_snapshot(self, snapshot_submission):
        result = self.broker.send_task('queues.broadcast_tasks.publish_snapshot', args=[snapshot_submission], queue=self.CELERY_QUEUE, serializer='json')
        return result.id