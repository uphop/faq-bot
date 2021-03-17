from broker import broker
from services.broadcast_service import BroadcastService
import logging
logger = logging.getLogger(__name__)

@broker.task
def publish_snapshot(snapshot):
    broadcast_service = BroadcastService()
    broadcast_service.publish_snapshot(snapshot)
    return 0