""" Unit tests for the address validation flask server. """
import copy
import json
import unittest

import muse_usps_server
import nose.tools


TEST_ADDRESS = {'address_line_1': '1600 Pennsylvania Ave NW',
                'address_line_2': '',
                'city': 'Washington',
                'state': 'DC',
                'zip_code': '20500'}


class MuseUspsServerTestCase(unittest.TestCase):
    """ Flask server testing class. """

    def setUp(self):
        """ Puts flask in testing mode and makes a test client. """
        muse_usps_server.APPLICATION.testing = True
        self.app = muse_usps_server.APPLICATION.test_client()

    def test_valid_address(self):
        """ Tests what should be a valid request. """
        expected = {'address_line_1': '1600 PENNSYLVANIA AVE NW',
                    'address_line_2': '',
                    'city': 'WASHINGTON',
                    'state': 'DC',
                    'zip_code': '20500-0003',
                    'usps_extra': {
                        'ReturnText': 'Default address: The address you ' +
                                      'entered was found but more ' +
                                      'information is needed (such as an ' +
                                      'apartment, suite, or box number) to ' +
                                      'match to a specific address.'}}
        response = self.app.post('/validate',
                                 data=json.dumps(TEST_ADDRESS),
                                 content_type='application/json')
        actual = json.loads(response.get_data().decode('utf-8'))
        assert expected == actual

    def test_missing_field(self):
        """ Tests a request that should return a 400 error. """
        address = copy.deepcopy(TEST_ADDRESS)
        address['address_line_1'] = ''
        expected = {'error': 'Address Not Found.'}
        response = self.app.post('/validate',
                                 data=json.dumps(address),
                                 content_type='application/json')
        assert response.status_code == 400
        actual = json.loads(response.get_data().decode('utf-8'))
        assert actual == expected
