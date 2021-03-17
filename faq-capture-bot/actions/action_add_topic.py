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
class ActionAddTopic(Action):
    def __init__(self):
        self.publish_api_client = PublishApiClient()

    def name(self) -> Text:
        return "action_add_topic"
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # check user
        user_id = tracker.get_slot('user_id')
        if user_id is None:
            dispatcher.utter_message(template='utter_check_user_failed')
            return []
        
        # retrieve slot values
        question = tracker.get_slot("question")
        answer = tracker.get_slot("answer")
            
        # create new topic
        topic_id = self.publish_api_client.create_topic(user_id, question, answer)
        if topic_id is None:
            dispatcher.utter_message(template='utter_add_topic_failed')
            return []
        
        # reset slots
        return [SlotSet("question", None), SlotSet("answer", None)]
                