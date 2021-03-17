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
        self.tasks = {}

    def submit_snapshot(self, snapshot):
        result = broadcast_tasks.publish_snapshot.apply_async(args=[snapshot], queue=self.CELERY_QUEUE, serializer='json')
        self.tasks[snapshot['id']] = result
        return result.id