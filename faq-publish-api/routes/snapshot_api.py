"""Endpoints to manage FAQ snapshot CRUD requests"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from services.snapshot_service import SnapshotService
import logging
logger = logging.getLogger(__name__)

# Init API blueprint
snapshot_api = Blueprint('snapshot_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return snapshot_api

# Init snapshot service
snapshot_service = SnapshotService()

@snapshot_api.route('/user/<string:_user_id>/snapshot', methods=['POST'])
def create_snapshot(_user_id):
    """Creates a new FAQ snapshot.
    @param _user_id: author's identifier
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # Store new snapshot
    id = snapshot_service.create_snapshot(_user_id)
    if not id:
        # HTTP 409 Conflict
        abort(409)

    # HTTP 201 Created
    return jsonify({"id": id}), 201

@snapshot_api.route('/user/<string:_user_id>/snapshot', methods=['GET'])
def get_snapshots(_user_id):
    """Return all active snapshots
    @param _user_id: author's identifier
    @return: 200: an array of all user's snapshots as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve snapshots from data store
    snapshots = snapshot_service.get_snapshots(_user_id)
    
    # HTTP 404 Not Found
    if snapshots is None:
        abort(404)

    return jsonify(snapshots)

@snapshot_api.route('/user/<string:_user_id>/snapshot/<string:_snapshot_id>', methods=['GET'])
def get_snapshot_by_id(_user_id, _snapshot_id):
    """Get snapshot by it's identifier
    @param _user_id: author's identifier
    @param _snapshot_id: snapshot identifier
    @return: 200: a snapshot as a flask/response object \
    with application/json mimetype.
    @raise 404: if topic is not found
    """
    # Retrieve snapshot from data store
    snapshot = snapshot_service.get_snapshot_by_id(_user_id, _snapshot_id)

    # HTTP 404 Not Found
    if snapshot is None:
        abort(404)

    return jsonify(snapshot)

@snapshot_api.route('/user/<string:_user_id>/snapshot/published', methods=['GET'])
def get_published_snapshot(_user_id):
    """Get publihsed snapshot for a user.
    @param _user_id: author's identifier
    @return: 200: a snapshot as a flask/response object \
    with application/json mimetype.
    @raise 404: if topic is not found
    """
    # Retrieve snapshot from data store
    snapshot = snapshot_service.get_published_snapshot(_user_id)

    # HTTP 404 Not Found
    if snapshot is None:
        abort(404)

    return jsonify(snapshot)

@snapshot_api.route('/user/<string:_user_id>/snapshot/<string:_snapshot_id>', methods=['PUT'])
def update_snapshot(_user_id, _snapshot_id):
    """Updates a snapshot record
    @param _user_id: author's identifier
    @param _snapshot_id: snapshot identifier
    @return: 204: an empty payload.
    @raise 404: if snapshot is not found
    """
    # Retrive and parse JSON body
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('broadcast_id'):
        abort(400)
        
    if not data.get('broadcast_name'):
        abort(400)

    if not data.get('broadcast_url'):
        abort(400)

    # Store broadcast details
    id = snapshot_service.update_snapshot(_user_id, _snapshot_id, data['broadcast_id'], data['broadcast_name'], data['broadcast_url'])
    if not id:
        # HTTP 409 Conflict
        abort(404)

    # HTTP 204 Deleted
    return '', 204

@snapshot_api.route('/user/<string:_user_id>/snapshot/<string:_snapshot_id>', methods=['DELETE'])
def delete_snapshot(_user_id, _snapshot_id):
    """Delete a snapshot record
    @param _user_id: author's identifier
    @param _snapshot_id: snapshot identifier
    @return: 204: an empty payload.
    @raise 404: if snapshot is not found
    """
    # Remove snapshot from data store
    deleted_id = snapshot_service.delete_snapshot(_user_id, _snapshot_id)

    # HTTP 404 Not Found
    if deleted_id is None:
        abort(404)

    # HTTP 204 Deleted
    return '', 204