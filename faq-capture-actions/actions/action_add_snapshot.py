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
Action for adding new FAQ snapshot.
"""
class ActionAddSnapshot(Action):
    def __init__(self):
        self.publish_api_client = PublishApiClient()

    def name(self) -> Text:
        return "action_add_snapshot"
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # retrieve slot values
        user_id = tracker.get_slot('user_id')
        if user_id is None:
            dispatcher.utter_message(template='utter_check_user_failed')
            return []

        # create a new snapshot
        snapshot_id = self.publish_api_client.create_snapshot(user_id)
        if snapshot_id is None:
            dispatcher.utter_message(template='utter_add_snapshot_failed')
            return []
            
        dispatcher.utter_message(template='utter_add_snapshot_confirmation')
        return []