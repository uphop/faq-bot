from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormValidationAction
from actions.publish_api_client import PublishApiClient
from actions.slack_api_client import SlackApiClient
import logging
logger = logging.getLogger(__name__)

"""
Action for checking if user is registered, and if not yet - create a new user.
"""
class ActionCheckUserRegistration(Action):
    def __init__(self):
        # init API clients
        self.publish_api_client = PublishApiClient()
        self.slack_api_client = SlackApiClient()

    def name(self) -> Text:
        return "action_check_user"
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # check if user ID is already retrieved
        user_id = tracker.get_slot('user_id')
        slot_list = []
        # if not yet, get user ID from tracker, retrieve user's details from Slack profile, and add as slots
        if user_id is None:
            user_details = self.slack_api_client.get_user_info(tracker.sender_id)
            if user_details is not None:
                # try to create new user in Publish API with the same name
                user_id = self.publish_api_client.create_user(user_details['real_name'], tracker.sender_id)

                # add user details to slots
                slot_list.append(SlotSet('user_id', user_id))
                slot_list.append(SlotSet('user_real_name', user_details['real_name']))
                slot_list.append(SlotSet('user_display_name', user_details['display_name']))
        else:
            # user is already known let's update her sender ID to keep the latest one in the user's profile
            user_id = self.publish_api_client.update_user(user_id, tracker.sender_id)
        
        return slot_list