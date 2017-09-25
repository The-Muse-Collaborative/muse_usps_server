""" Some docstring. """
import json

import flask
import muse_usps


# Load configuration options from json config file.
with open('muse_usps_server.json') as CONF_JSON_FILE:
    CONF_JSON = json.load(CONF_JSON_FILE)
USPS_API_URL = CONF_JSON['api_url']
USPS_USER_ID = CONF_JSON['user_id']

APPLICATION = flask.Flask(__name__)


@APPLICATION.route('/validate', methods=['POST'])
def validate_address():
    """ Validates an address that comes in as JSON data."""
    try:
        validated = muse_usps.validate(USPS_API_URL,
                                       USPS_USER_ID,
                                       flask.request.json)
        return flask.jsonify(validated)
    except RuntimeError as ex:
        return flask.jsonify({'error': str(ex).strip()}), 400
