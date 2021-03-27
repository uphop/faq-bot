import os
import requests
import json
import logging
logger = logging.getLogger(__name__)

"""
Wrapper for Rasa HTTP API. 
"""
class RasaApiClient:
    def __init__(self, base_url):
        # load configuration
        self.base_url = base_url

    def post_message(self, message, sender):
        # prepare request
        request_url = f"{self.base_url}/webhooks/rest/webhook"
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

    