"""Endpoints to manage FAQ topic CRUD requests"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from services.topic_service import TopicService
import logging
logger = logging.getLogger(__name__)

# Init API blueprint
topic_api = Blueprint('topic_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return topic_api

# Init topic service
topic_service = TopicService()

@topic_api.route('/user/<string:_user_id>/topic', methods=['POST'])
def create_topic(_user_id):
    """Creates a new FAQ topic.
    @param _user_id: author's identifier
    @param question: post : the question to expect from requesters
    @param answer: post : the response which should be provided back to requesters
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # Retrive and parse JSON body
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('question'):
        abort(400)
    if not data.get('answer'):
        abort(400)

    # Store new question / answer pair
    id = topic_service.create_topic(_user_id, data['question'], data['answer'])
    if not id:
        # HTTP 409 Conflict
        abort(409)

    # HTTP 201 Created
    return jsonify({"id": id}), 201

@topic_api.route('/user/<string:_user_id>/topic', methods=['GET'])
def get_topics(_user_id):
    """Return all active topics
    @param _user_id: author's identifier
    @return: 200: an array of all captured topics as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve topics from data store
    topics = topic_service.get_topics(_user_id)
    
    # HTTP 404 Not Found
    if topics is None:
        abort(404)

    return jsonify(topics)

@topic_api.route('/user/<string:_user_id>/topic/<string:_topic_id>', methods=['GET'])
def get_topic_by_id(_user_id, _topic_id):
    """Get topic by it's identifier
    @param _user_id: author's identifier
    @param _topic_id: topic identifier
    @return: 200: a topic as a flask/response object \
    with application/json mimetype.
    @raise 404: if topic is not found
    """
    # Retrieve topics from data store
    topic = topic_service.get_topic_by_id(_user_id, _topic_id)

    # HTTP 404 Not Found
    if topic is None:
        abort(404)

    return jsonify(topic)

@topic_api.route('/user/<string:_user_id>/topic/<string:_topic_id>', methods=['DELETE'])
def delete_topic(_user_id, _topic_id):
    """Delete a topic record
    @param _user_id: author's identifier
    @param _topic_id: topic identifier
    @return: 204: an empty payload.
    @raise 404: if topic is not found
    """
    # Remove topic from data store
    deleted_id = topic_service.delete_topic(_user_id, _topic_id)

    # HTTP 404 Not Found
    if deleted_id is None:
        abort(404)

    # HTTP 204 Deleted
    return '', 204