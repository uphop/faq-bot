from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)

class ActionNotifySnapshotPublished(Action):
    def name(self) -> Text:
        return "action_notify_snapshot_published"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        broadcast_name = next(tracker.get_latest_entity_values('broadcast_name'), '')
        return [SlotSet('broadcast_name', broadcast_name)]