import os
import requests
import json
import logging
logger = logging.getLogger(__name__)

"""
Wrapper for Publish API. 
"""
class PublishApiClient:
    def __init__(self):
        # load configuration
        self.PUBLISH_API_BASE_URL = os.getenv('PUBLISH_API_BASE_URL', 'http://localhost:5000')

    def create_user(self, name, sender_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user"
        payload = {
            'name': name,
            'sender_id': sender_id
        }

        # call publish API
        try:
            response = requests.post(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 201 and response.json():
            body = response.json()
            return body.get('id', '')

    def update_user(self, user_id, sender_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}"
        payload = {
            'sender_id': sender_id
        }

        # call publish API
        try:
            response = requests.put(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 204:
            return user_id
    
    def create_topic(self, user_id, question, answer):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/topic"
        payload = {
            'question': question,
            'answer': answer
        }

        # call publish API
        try:
            response = requests.post(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 201 and response.json():
            body = response.json()
            return body.get('id', '')

    def get_topics(self, user_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/topic"

        # call publish API
        try:
            response = requests.get(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200 and response.json():
            body = response.json()
            return body

    def delete_topic(self, user_id, topic_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/topic/{topic_id}"

        # call publish API
        try:
            response = requests.delete(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 204:
            return topic_id

    def create_snapshot(self, user_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/snapshot"

        # call publish API
        try:
            response = requests.post(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 201 and response.json():
            body = response.json()
            return body.get('id', '')

    def get_snapshots(self, user_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/snapshot"

        # call publish API
        try:
            response = requests.get(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200 and response.json():
            body = response.json()
            return body

    def get_user_by_sender_id(self, sender_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/sender/{sender_id}"

        # call publish API
        try:
            response = requests.get(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200 and response.json():
            body = response.json()
            return body

    def get_published_snapshot(self, user_id):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{user_id}/snapshot/published"

        # call publish API
        try:
            response = requests.get(request_url)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 200 and response.json():
            body = response.json()
            return body


