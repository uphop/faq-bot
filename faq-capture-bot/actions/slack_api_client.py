import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
logger = logging.getLogger(__name__)

'''
Wrapper for Slack API. 
'''
class SlackApiClient:
    def __init__(self):
        self.slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

    def get_user_info(self, username):
        '''
        Gets user profile details from Slack by user name.
        '''
        try:
            result = self.slack_client.users_info(user=username)
            if result is not None and result.get('ok', False):
                return {
                    'real_name': result['user']['profile']['real_name'],
                    'display_name': result['user']['profile']['display_name']
                }

        except SlackApiError as e:
            logger.error("Error fetching user details: {}".format(e))

    def notify_user(self, channel, text):
        '''
        Sends text message to Slack channel.
        '''
        try:
            response = self.slack_client.chat_postMessage(
                channel=channel,
                text=text
            )

        except SlackApiError as e:
            logger.error("Error posting message: {}".format(e))
