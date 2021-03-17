from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormValidationAction
from actions.publish_api_client import PublishApiClient
import logging
logger = logging.getLogger(__name__)

"""
Action for adding new FAQ topic.
"""
class ActionGetTopics(Action):
    def __init__(self):
        self.publish_api_client = PublishApiClient()

    def name(self) -> Text:
        return "action_get_topics"
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # retrieve user ID
        user_id = tracker.get_slot('user_id')
        if user_id is None:
            dispatcher.utter_message(template='utter_check_user_failed')
            return []

        # retrieve user's topics
        topics = self.publish_api_client.get_topics(user_id)
        if topics is None or len(topics) == 0:
            # no topics atm, nothing to do
            dispatcher.utter_message(template='utter_get_topics_empty')
            return []

        # init list of topics
        topic_list = {
            'blocks': [
                {
                    'type': 'section',
                    'fields': []
                }
            ]
        }

        # retrieve user's published topics
        published_topics = []
        snapshots = self.publish_api_client.get_snapshots(user_id)
        if snapshots is not None:
            for snapshot in snapshots:
                for published_topic in snapshot['topics']:
                    published_topics.append(published_topic['topic_id'])

        # ietrate through topics and add question / answer fields
        for topic in topics:
            publishing_flag = ':white_check_mark:' if topic['id'] in published_topics else ':o2:'

            topic_list['blocks'][0]['fields'].append({
                'type': 'mrkdwn',
                'text': publishing_flag + ' ' + topic['question']
            })
            
            topic_list['blocks'][0]['fields'].append({
                'type': 'mrkdwn',
                'text': topic['answer']
            })
        
        dispatcher.utter_message(template='utter_get_topics', json_message = topic_list)
        return []