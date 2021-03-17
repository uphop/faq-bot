import os
import requests
import json
import logging
logger = logging.getLogger(__name__)

"""
Wrapper for Rasa HTTP API. 
"""
class RasaApiClient:
    def __init__(self):
        # load configuration
        self.RASA_API_BASE_URL = os.getenv('RASA_API_BASE_URL', 'http://localhost:5006')

    def post_message(self, message, sender):
        # prepare request
        request_url = f"{self.RASA_API_BASE_URL}/webhooks/rest/webhook"
        payload = {
            'message': message,
            'sender': sender,
        }

        # call publish API
        try:
            response = requests.post(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200 and response.json():
            body = response.json()
            return body

    