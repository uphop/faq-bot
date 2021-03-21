import uuid
from datetime import datetime, timedelta
from data.datastores.snapshot_data_store import SnapshotDataStore
from services.user_service import UserService
from services.topic_service import TopicService
from queues.broadcast_queue import BroadcastQueue

import logging
logger = logging.getLogger(__name__)

'''
Manages snapshot entity.
'''
class SnapshotService:
    def __init__(self):
        # init data store
        self.data_store = SnapshotDataStore()
        # init other services
        self.user_service = UserService()
        self.topic_service = TopicService()
        self.broadcast_queue = BroadcastQueue()

    def create_snapshot(self, user_id):
        """Creates a new snapshot.
        @param: user_id: author's identifier
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # check if such user exists
        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            logger.error('User does not exist: ' + str(user_id))
            return

        # delete user's active snapshot, if there is any
        current_snapshots = self.get_snapshots(user_id)
        for current_snapshot in current_snapshots:
            deleted_id = self.delete_snapshot(user_id, current_snapshot['id'])
            if deleted_id is None:
                logger.error(
                    'Failed to delete snapshots for user: ' + str(user_id))
                return

        # get all active topics for the user
        topics = self.topic_service.get_topics(user_id)
        if topics is None or len(topics) == 0:
            logger.error('User does not have topics: ' + str(user_id))
            return

        # generate new snapshot identifier and add to data store
        id = str(uuid.uuid4())
        self.data_store.create_snapshot(
            user_id, id, datetime.now().timestamp(), topics)
        logger.debug('Created new snapshot ' + str(id) +
                     ' for user ' + str(user_id))

        # get snapshot
        snapshot = self.get_snapshot_by_id(user_id, id)

         # send snapshot details to worker, to publish a new broacast bot
        snapshot_submission = {
             'snapshot': snapshot,
             'target_spot': user['spot_id']
        }
        self.broadcast_queue.submit_snapshot(snapshot_submission)
        logger.debug('Snapshot submitted for broadcasting ' + str(id) + ' for user ' + str(user_id))

        return id

    def get_snapshots(self, user_id):
        """Return all snapshots for a user.
        @param: user_id: author's identifier
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # retrieve all snapshots from data store, convert to list and return
        response = []
        results = self.data_store.get_snapshots(user_id)
        if not results is None:
            for user_id, id, created, published, broadcast_id, broadcast_name, broadcast_url, in results:
                snapshot = self.get_snapshot_by_id(user_id, id)
                response.append(snapshot)
        return response

    def get_published_snapshot(self, user_id):
        """Return currenlty published snapshot for a user.
        @param: user_id: author's identifier
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # retrieve all snapshots from data store, convert to list and return
        results = self.data_store.get_snapshots(user_id)
        if not results is None:
            for user_id, id, created, published, broadcast_id, broadcast_name, broadcast_url, in results:
                if not published is None and not broadcast_name is None and not broadcast_url is None:
                    snapshot = self.get_snapshot_by_id(user_id, id)
                    return snapshot

    def get_snapshot_by_id(self, user_id, id):
        """Get snapshot by identifier.
        @param: user_id: author's identifier
        @param id: snapshot's ID
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # check if snapshot ID passed
        if id is None or len(id) == 0:
            logger.error('Snapshot ID is not passed.')
            return

        # retrieve snapshot from data store by ID; if snapshot not found, return None
        snapshot = self.data_store.get_snapshot_by_id(user_id, id)
        if not snapshot is None:
            response = self.map_snapshot(
                snapshot.user_id, snapshot.id, snapshot.created, snapshot.published, snapshot.broadcast_id, snapshot.broadcast_name, snapshot.broadcast_url)

            snapshot_topics = self.data_store.get_snapshot_topics_by_id(
                user_id, id)
            response['topics'] = self.map_snapshot_topics(snapshot_topics)

            return response

    def delete_snapshot(self, user_id, id):
        """Delete snapshot by identifier.
        @param: user_id: author's identifier
        @param id: snapshot's ID
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # check if snapshot ID passed
        if id is None or len(id) == 0:
            logger.error('Snapshot ID is not passed.')
            return

        # retrieve snapshot from data store by ID; if user not found, return None
        result = self.data_store.get_snapshot_by_id(user_id, id)
        if result is None:
            logger.error('Snapshot is not found: ' + str(id))
            return

        # delete snapshot from data store by ID
        self.data_store.delete_snapshot(user_id, id)
        logger.debug('Deleted snapshot ' + str(id) +
                     ' for user ' + str(user_id))
        return id

    def update_snapshot(self, user_id, id, broadcast_id, broadcast_name, broadcast_url):
        """Update snapshot by identifier.
        @param: user_id: author's identifier
        @param id: snapshot's ID
        @param name: broadcast name
        """
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            logger.error('User ID is not passed.')
            return

        # check if snapshot ID passed
        if id is None or len(id) == 0:
            logger.error('Snapshot ID is not passed.')
            return

        # check if broadcast ID passed
        if broadcast_id is None or len(broadcast_id) == 0:
            logger.error('Broadcast ID is not passed.')
            return

        # check if broadcast name passed
        if broadcast_name is None or len(broadcast_name) == 0:
            logger.error('Broadcast name is not passed.')
            return

        # check if broadcast URL passed
        if broadcast_url is None or len(broadcast_url) == 0:
            logger.error('Broadcast name is not passed.')
            return

        # retrieve snapshot from data store by ID; if user not found, return None
        result = self.data_store.get_snapshot_by_id(user_id, id)
        if result is None:
            logger.error('Snapshot is not found: ' + str(id))
            return

        # update snapshot in data store by ID
        self.data_store.update_snapshot(user_id, id, datetime.now().timestamp(), broadcast_id, broadcast_name, broadcast_url)
        logger.debug('Updated snapshot ' + str(id) +
                     ' for user ' + str(user_id))

        # notify user about completed snapshot update
        self.user_service.notify_user_snapshot_updated(user_id, broadcast_name)

        return id


    def map_snapshot(self, user_id, id, created, published, broadcast_id, broadcast_name, broadcast_url):
        """Maps data store row to dict.
        """
        response = {
            'user_id': user_id,
            'id': id,
            'created': created
        }

        if published is not None:
            response['published'] = published
        
        if broadcast_id is not None:
            response['broadcast_id'] = broadcast_id

        if broadcast_name is not None:
            response['broadcast_name'] = broadcast_name

        if broadcast_url is not None:
            response['broadcast_url'] = broadcast_url

        return response

    def map_snapshot_topics(self, snapshot_topics):
        if snapshot_topics is not None:
            return [
                {
                    'user_id': user_id,
                    'topic_id': topic_id,
                    'question': question,
                    'answer': answer,
                    'created': created
                } for user_id, topic_id, question, answer, created, in snapshot_topics
            ]
