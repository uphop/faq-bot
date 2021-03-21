import os
import sys
from shutil import copyfile, copytree, rmtree
import requests
import json
import logging
import uuid
from coolname import generate_slug
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
sys.path.append('./')
from transforms.bot_transform import BotTransform
from transforms.synonim_transform import SynonimTransform
from transforms.nlu_transform import NLUTransform
from transforms.domain_transform import DomainTransform
from transforms.model_transform import ModelTransform
from transforms.runtime_transform import RuntimeTransform

logger = logging.getLogger(__name__)


'''
Manages broadcast entity.
'''
class BroadcastService:
    def __init__(self):
        # load configuration
        self.PUBLISH_API_BASE_URL = os.getenv('PUBLISH_API_BASE_URL', 'http://localhost:5000')

    """
    Main processing chain of broadcast bot publishing.
    Prepares NLU / domain based on captured FAQs, and trains a replica of broadcast with that training data.
    """
    def publish_snapshot(self, snapshot_submission):
        logger.debug('Publishing started.')

        snapshot = snapshot_submission['snapshot']
        snapshot_id = snapshot['id']
        user_id = snapshot['user_id']
        snapshot_topics = snapshot['topics']
        target_spot = snapshot_submission['target_spot']

        # create broadcast identity
        broadcast_id = str(uuid.uuid4())
        broadcast_name = generate_slug()
        
        # clone bot
        bot_output_folder = BotTransform(snapshot_id).transform()

        # run topics through transformers
        items = SynonimTransform().transform(snapshot_topics)
        nlu_output_file = NLUTransform(bot_output_folder).transform(items)
        domain_output_file = DomainTransform(bot_output_folder).transform(items)

        # train cloned bot
        model_output_file = ModelTransform(bot_output_folder).transform(snapshot_id)
        
        # prepare bot runtime
        broadcast_url = RuntimeTransform(bot_output_folder).transform(user_id, target_spot, broadcast_name)

        # clean-up
        BotTransform(snapshot_id).cleanup()

        # update snapshot
        self.notify_master(snapshot_id, user_id, broadcast_id, broadcast_name, broadcast_url)

   
    def notify_master(self, id, user_id, broadcast_id, broadcast_name, broadcast_url):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/snapshot/{id}"
        payload = {
            'broadcast_id': broadcast_id,
            'broadcast_name': broadcast_name,
            'broadcast_url': broadcast_url
        }

        # call publish API
        try:
            response = requests.put(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        # check status code and return result
        if response.status_code == 201 and response.json():
            body = response.json()
            return body.get('id', '')


# Default handler
if __name__ == '__main__':
    snapshot = {
        "broadcast_name": "norma_williams",
        "created": "1615630111.54651",
        "id": "369f10c1-db94-442e-a5f6-b279b0858acc",
        "published": "1615630176.59936",
        "topics": [
            {
                "answer": "Get burger!",
                "created": "1615630081.75888",
                "question": "What should I have for lunch tomorrow?",
                "topic_id": "69639485-1228-40a0-acde-6224ffc66e78",
                "user_id": "6d49c900-bca0-4fe8-bc02-bfc90635a5ed"
            },
            {
                "answer": "Nika for sure!",
                "created": "1615630100.83781",
                "question": "Who should I kiss tonight?",
                "topic_id": "85a7a15b-69da-470d-ae14-1f032b025e4c",
                "user_id": "6d49c900-bca0-4fe8-bc02-bfc90635a5ed"
            },
            {
                "answer": "+37065641046",
                "created": "1615630100.83781",
                "question": "What is your phone number?",
                "topic_id": "85a7a15b-69da-470d-ae14-1f032b025e4d",
                "user_id": "6d49c900-bca0-4fe8-bc02-bfc90635a5ed"
            }
        ],
        "user_id": "6d49c900-bca0-4fe8-bc02-bfc90635a5ed"
    }

    snapshot_submission = {
        'snapshot': snapshot,
        'target_spot': 123
    }

    from dotenv import load_dotenv
    load_dotenv()

    svc = BroadcastService()
    svc.publish_snapshot(snapshot_submission)
