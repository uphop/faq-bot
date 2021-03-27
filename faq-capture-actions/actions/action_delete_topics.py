from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormValidationAction
from actions.publish_api_client import PublishApiClient
import logging
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
load_dotenv()

"""
Action for adding new FAQ topic.
"""
class ActionDeleteTopics(Action):
    def __init__(self):
        self.publish_api_client = PublishApiClient()

    def name(self) -> Text:
        return "action_delete_topics"
        
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

        for topic in topics:
            # delete all topics one-by-one
            deleted_topic_id = self.publish_api_client.delete_topic(user_id, topic['id'])
            if deleted_topic_id is None:
                # if cannot delete specific topic - shout for help
                dispatcher.utter_message(template='utter_delete_topics_failed')
                return []

        # all topics deleted, utter confirmation
        dispatcher.utter_message(template='utter_delete_topics_confirmation')
        return []