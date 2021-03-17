"""Endpoints to manage FAQ users CRUD requests"""
from flask import jsonify, abort, request, Blueprint
from services.user_service import UserService
import logging
logger = logging.getLogger(__name__)

# Init API blueprint
user_api = Blueprint('user_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return user_api

# Init user service
user_service = UserService()

@user_api.route('/user', methods=['POST'])
def create_user():
    """Creates a new FAQ author.
    @param name: post : the full author's name
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # Retrive and parse JSON body
    if not request.get_json():
        # HTTP 400 Bad Request (missing JSON payload)
        abort(400)

    data = request.get_json(force=True)

    if not data.get('name'):
        # HTTP 400 Bad Request (missing name in payload)
        abort(400)
    if not data.get('sender_id'):
        # HTTP 400 Bad Request (missing sender_id in payload)
        abort(400)

    # Store new user
    id = user_service.create_user(data['name'], data['sender_id'])
    if not id:
        # HTTP 400 Bad Request (cannot create user)
        abort(400)

    # HTTP 201 Created
    return jsonify({"id": id}), 201

@user_api.route('/user', methods=['GET'])
def get_users():
    """Return all active users
    @return: 200: an array of all active users as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve users from data store
    users = user_service.get_users()
    return jsonify(users)


@user_api.route('/user/<string:_user_id>', methods=['GET'])
def get_user_by_id(_user_id):
    """Get user by identifier
    @param _user_id: author's identifier
    @return: 200: a user as a flask/response object \
    with application/json mimetype.
    @raise 400: missing required parameter
    @raise 404: if user is not found
    """
    # Retrieve user from data store
    user = user_service.get_user_by_id(_user_id)

    # HTTP 404 Not Found
    if user is None:
        abort(404)

    return jsonify(user)

@user_api.route('/user/sender/<string:_user_sender_id>', methods=['GET'])
def get_user_by_sender_id(_user_sender_id):
    """Get user by sender identifier
    @param _user_sender_id: author's sender identifier
    @return: 200: a user as a flask/response object \
    with application/json mimetype.
    @raise 400: missing required parameter
    @raise 404: if user is not found
    """
    # Retrieve user from data store
    user = user_service.get_user_by_sender_id(_user_sender_id)

    # HTTP 404 Not Found
    if user is None:
        abort(404)

    return jsonify(user)

@user_api.route('/user/<string:_user_id>', methods=['PUT'])
def update_user(_user_id):
    """Delete a user record
    @param _user_id: author's identifier
    @return: 204: an empty payload.
    @raise 404: if user is not found
    """
    # Retrive and parse JSON body
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('sender_id'):
        abort(400)

    # Remove user from data store
    updated_id = user_service.update_user(_user_id, data['sender_id'])

    # HTTP 404 Not Found
    if updated_id is None:
        abort(404)

    # HTTP 204 Deleted
    return '', 204

@user_api.route('/user/<string:_user_id>', methods=['DELETE'])
def detete_user(_user_id):
    """Delete a user record
    @param _user_id: author's identifier
    @return: 204: an empty payload.
    @raise 404: if user is not found
    """
    # Remove user from data store
    deleted_id = user_service.delete_user(_user_id)

    # HTTP 404 Not Found
    if deleted_id is None:
        abort(404)

    # HTTP 204 Deleted
    return '', 204

