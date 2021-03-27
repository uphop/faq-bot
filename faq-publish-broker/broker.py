import os
import sys
import logging
from dotenv import load_dotenv
from celery import Celery

# init config
load_dotenv()
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'memory://localhost/')
CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'publish_queue')

# Enable loging
logging.root.handlers = []
logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Init Celery broker
broker = Celery('queues',
             broker=CELERY_BROKER,
             include=['queues.broadcast_tasks'])

# Optional configuration, see the application user guide.
broker.conf.update(
    task_routes = {
        'queues.broadcast_tasks.publish_snapshot': {
            'queue': CELERY_QUEUE
        }
    },
    result_expires=3600,
)

# Default handler
if __name__ == '__main__':
    broker.start()