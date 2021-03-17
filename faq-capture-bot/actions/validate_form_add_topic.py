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

class ValidateFormAddTopic(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_add_topic"

    async def validate_question(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print('Validating question: ' + value)
        if value:
            return {"question": value}

    async def validate_answer(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print('Validating answer: ' + value)
        if value:
            return {"answer": value}