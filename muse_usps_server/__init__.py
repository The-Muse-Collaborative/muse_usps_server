""" Simple flask server allowing AJAX requests to validate addresses using the
USPS API. """
import json
import logging
import logging.config

import flask
import get_docker_secret
import muse_usps


# Load logging options from ini config file.
logging.config.fileConfig('logging.ini')
LOGGER = logging.getLogger(__name__)

# Get configuration secrets.
USPS_API_URL = get_docker_secret.get_docker_secret('muse_usps_server_api_url',
                                                   safe=False)
USPS_USER_ID = get_docker_secret.get_docker_secret('muse_usps_server_user_id',
                                                   safe=False)

APPLICATION = flask.Flask(__name__)


@APPLICATION.route('/validate', methods=['POST'])
def validate():
    """ Validates an address that comes in as JSON data.

    See muse_usps.validate documentation for request structure. Any extra
    fields are ignored. Returns a 400 error if the request was valid, but an
    error was reported by the USPS API. The 400 response will include an
    "error" field with the error message returned by the USPS API. All other
    backend errors will result in a 500 error with no response. """
    try:
        LOGGER.info('Address validation request: %s', flask.request.json)
        validated = muse_usps.validate(USPS_API_URL,
                                       USPS_USER_ID,
                                       flask.request.json)
        LOGGER.debug('Address validation response: %s', validated)
        return flask.jsonify(validated)
    except RuntimeError as ex:
        LOGGER.error('Address validation runtime error: %s', ex)
        return flask.jsonify({'error': str(ex).strip()}), 400
    except Exception as ex:
        LOGGER.error('Address validation unknown error: %s', ex)
        raise  # This will result in a 500 error.
