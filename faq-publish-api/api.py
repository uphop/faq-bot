"""FQA REST API (CRUD)"""

import argparse
import os
from os.path import join, dirname
import sys
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes import topic_api, user_api, snapshot_api

# init config
load_dotenv()

# Init Flask app
FLASK_APP_NAME = os.environ.get('FLASK_APP_NAME', 'faq-publish-api')
api = Flask(FLASK_APP_NAME)

# Init Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': FLASK_APP_NAME
    }
)

# Enable loging
logging.root.handlers = []
logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Register API blueprints
api.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
api.register_blueprint(user_api.get_blueprint())
api.register_blueprint(topic_api.get_blueprint())
api.register_blueprint(snapshot_api.get_blueprint())

# Default error handlers
@api.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@api.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@api.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(409)
def handle_409_error(_error):
    """Return a http 409 error to client"""
    return make_response(jsonify({'error': 'Conflict'}), 409)

@api.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

# Default handler
if __name__ == '__main__':
    # get Flask server config
    FLASK_APP_HOST = os.environ.get('FLASK_APP_HOST', '0.0.0.0')
    FLASK_APP_PORT = int(os.environ.get('FLASK_APP_PORT', 5000))
    FLASK_APP_DEBUG = eval(os.environ.get('FLASK_APP_DEBUG', 'False'))

    # ...and launch
    api.logger.info(f'Starting API {FLASK_APP_NAME}...')
    api.run(host=FLASK_APP_HOST, port=FLASK_APP_PORT, debug=FLASK_APP_DEBUG)