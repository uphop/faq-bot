import os
from queues import broadcast_tasks
import logging
logger = logging.getLogger(__name__)

'''
Braodcast queue client.
'''
class BroadcastQueue:
    def __init__(self):
        self.CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'publish_queue')

    def submit_snapshot(self, snapshot_submission):
        result = broadcast_tasks.publish_snapshot.apply_async(args=[snapshot_submission], queue=self.CELERY_QUEUE, serializer='json')
        return result.id