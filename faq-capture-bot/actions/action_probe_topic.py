from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormValidationAction
from actions.publish_api_client import PublishApiClient
from actions.rasa_api_client import RasaApiClient
import logging
logger = logging.getLogger(__name__)

"""
Action for get answer to FAQ topic.
"""
class ActionProbeTopic(Action):
    def __init__(self):
        self.publish_api_client = PublishApiClient()
        self.rasa_api_client = RasaApiClient()

    def name(self) -> Text:
        return "action_probe_topic"
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # retrieve @mentions from entity
        originator_sender_id = next(tracker.get_latest_entity_values('mentioned_slack_user'), '')
        if len(originator_sender_id) == 0:
            dispatcher.utter_message(template='utter_check_user_failed')
            return []
        
        # extract question from the latest message's text
        full_message_text = tracker.latest_message.get('text')
        mentioned_slack_user_substr = f'<{originator_sender_id}>'
        question_start_idx = full_message_text.find(mentioned_slack_user_substr) + len(mentioned_slack_user_substr)
        question = full_message_text[question_start_idx:].strip()
        if len(question) == 0:
            dispatcher.utter_message(template='utter_ask_question_empty')
            return []

        # retrieve user by originator_sender_id
        originator_sender_id = originator_sender_id.replace('@', '')
        user = self.publish_api_client.get_user_by_sender_id(originator_sender_id)
        if user is None:
            dispatcher.utter_message(template='utter_check_user_failed')
            return []
        
        # get user's active snapshot
        snapshot = self.publish_api_client.get_published_snapshot(user['id'])
        if snapshot is None:
            dispatcher.utter_message(template='utter_get_snapshots_failed')
            return []

        # ask snapshot a question
        # TODO: route question to the target bot
        bot_response = self.rasa_api_client.post_message(message=question, sender=tracker.sender_id)
        if bot_response is None or len(bot_response) == 0:
            dispatcher.utter_message(template='utter_get_answer_failed')
            return []

        # retrieve bot answer
        answer = bot_response[0]["text"]

        # post asnwer back to the requester
        dispatcher.utter_message(template='utter_get_answer', originator_sender_id=originator_sender_id, originator_answer=answer)
        return []
                