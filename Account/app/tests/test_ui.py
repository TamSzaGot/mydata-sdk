# -*- coding: utf-8 -*-

"""
Test Cases for External API

__author__ = "Jani Yli-Kantola"
__copyright__ = ""
__credits__ = ["Harri Hirvonsalo", "Aleksi Palomäki"]
__license__ = "MIT"
__version__ = "1.3.0"
__maintainer__ = "Jani Yli-Kantola"
__contact__ = "https://github.com/HIIT/mydata-stack"
__status__ = "Development"
"""

import unittest
from base64 import b64encode

from flask import json
from app import create_app
from app.tests.controller import is_json, validate_json, account_create, default_headers, account_info_update, \
    generate_string
from app.tests.schemas.schema_account import schema_account_create, schema_account_auth, schema_account_get, \
    schema_account_info_listing, schema_account_info
from app.tests.schemas.schema_error import schema_request_error_detail_as_str, schema_request_error_detail_as_dict
from app.tests.schemas.schema_system import schema_db_clear, system_running, schema_sdk_auth


class UiTestCase(unittest.TestCase):

    API_PREFIX_INTERNAL = "/account/api/v1.3/internal"
    API_PREFIX_EXTERNAL = "/account/api/v1.3/external"

    def setUp(self):
        """
        TestCase Set Up
        :return:
        """
        app = create_app()
        app.config['TESTING'] = True
        app = app.test_client()
        self.app = app

    def tearDown(self):
        """
        TestCase Tear Down
        :return:
        """
        pass

    ##########
    ##########
    def test_system_running(self):
        """
        Test system running
        :return:
        """
        url = '/system/status/'

        response = self.app.get(url)
        unittest.TestCase.assertEqual(self, response.status_code, 200)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, system_running))

    ##########
    ##########
    def test_system_routes(self):
        """
        Test system running
        :return:
        """
        url = '/system/routes/'

        response = self.app.get(url)
        unittest.TestCase.assertEqual(self, response.status_code, 200)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)

    ##########
    ##########
    def test_clear_db_positive(self):
        """
        Test database clearing
        :return:
        """
        response = self.app.get('/system/db/clear/')
        unittest.TestCase.assertEqual(self, response.status_code, 200)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_db_clear))

    ##########
    ##########
    def test_account_create_password_too_long(self):
        """
        Test Account creation. Password too long
        :return:
        """

        url = self.API_PREFIX_EXTERNAL + '/accounts/'
        account_json, username, password = account_create(password_length=21)
        response = self.app.post(url, data=account_json, headers=default_headers)

        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    def test_account_create_password_too_short(self):
        """
        Test Account creation. Password too short
        :return:
        """

        account_json, username, password = account_create(password_length=3)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    ##########
    ##########
    def test_account_create_username_too_long(self):
        """
        Test Account creation. Username too long
        :return:
        """

        account_json, username, password = account_create(username_length=256)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    def test_account_create_username_too_short(self):
        """
        Test Account creation. Username too short
        :return:
        """

        account_json, username, password = account_create(username_length=2)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))


    ##########
    ##########
    def test_account_create_firstname_too_long(self):
        """
        Test Account creation. First name too long
        :return:
        """

        account_json, username, password = account_create(firstname_length=256)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    def test_account_create_firstname_too_short(self):
        """
        Test Account creation. First name too short
        :return:
        """

        account_json, username, password = account_create(firstname_length=2)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    ##########
    ##########
    def test_account_create_lastname_too_long(self):
        """
        Test Account creation. Last name too long
        :return:
        """

        account_json, username, password = account_create(lastname_length=256)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    def test_account_create_lastname_too_short(self):
        """
        Test Account creation. Last name too short
        :return:
        """

        account_json, username, password = account_create(lastname_length=2)
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

    ##########
    ##########
    def test_account_create_positive(self):
        """
        Test Account creation. Positive case
        :return:
        """

        account_json, account_username, account_password = account_create()
        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 201, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_create))

        return account_username, account_password

    ##########
    ##########
    def test_account_create_username_exists(self):
        """
        Test Account creation. Username already exits
        :return:
        """

        account_username, account_password = self.test_account_create_positive()
        account_json, account_username, account_password = account_create(username=account_username)

        response = self.app.post(self.API_PREFIX_EXTERNAL + '/accounts/', data=account_json, headers=default_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 409, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_username, account_password

    ##########
    ##########
    def test_account_authentication(self):
        """
        Test user authentication
        :return:
        """

        account_username, account_password = self.test_account_create_positive()

        request_headers = default_headers
        request_headers['Authorization'] = 'Basic ' + b64encode("{0}:{1}".format(account_username, account_password))

        url = self.API_PREFIX_EXTERNAL + '/auth/user/'
        response = self.app.get(url, headers=request_headers)

        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_auth))

        response_json = json.loads(response.data)
        account_api_key = response_json["Api-Key-User"]
        account_id = response_json["account_id"]

        return account_api_key, account_id, account_username, account_password

    ##########
    ##########
    def test_account_fetch(self):
        """
        Fetch Account entry
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_authentication()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_get))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_delete(self):
        """
        Test user deletion
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_authentication()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/"

        response = self.app.delete(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 204, msg=response.data)

        return account_api_key, account_id, account_username, account_password

    ##########
    ##########
    def test_account_authentication_with_deleted_account(self):
        """
        Test user authentication
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_delete()

        request_headers = default_headers
        request_headers['Authorization'] = 'Basic ' + b64encode("{0}:{1}".format(account_username, account_password))

        url = self.API_PREFIX_EXTERNAL + '/auth/user/'
        response = self.app.get(url, headers=request_headers)

        unittest.TestCase.assertEqual(self, response.status_code, 401, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_api_key, account_id, account_username, account_password

    ##########
    ##########
    def test_account_fetch_with_deleted_account(self):
        """
        Fetch Account entry
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_delete()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 401, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_dict))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_fetch_listing(self):
        """
        Fetch AccountInfo listing
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_authentication()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info_listing))
        account_info_id = json.loads(response.data)['data'][0]['id']

        return account_api_key, account_id, account_info_id

    ##########
    ##########
    def test_account_info_fetch_listing_wrong_account_id(self):
        """
        Fetch AccountInfo listing - Wrong account_id
        :return:
        """

        account_api_key, account_id, account_username, account_password = self.test_account_authentication()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(45864586) + "/info/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 403, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_fetch_one(self):
        """
        Fetch AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id = self.test_account_info_fetch_listing()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))
        account_avatar = json.loads(response.data)['data']['attributes']['avatar']

        return account_api_key, account_id, account_info_id, account_avatar

    ##########
    ##########
    def test_account_info_fetch_one_wrong_account_id(self):
        """
        Fetch AccountInfo entry by ID - Wrong ID
        :return:
        """

        account_api_key, account_id, account_info_id = self.test_account_info_fetch_listing()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(456464984) + "/info/" + str(account_info_id) + "/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 403, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_fetch_one_wrong_info_id(self):
        """
        Fetch AccountInfo entry by ID - Wrong ID
        :return:
        """

        account_api_key, account_id, account_info_id = self.test_account_info_fetch_listing()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_api_key) + "/"

        response = self.app.get(url, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 404, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_all(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update(object_id=account_info_id, firstname=generate_string(n=10), lastname=generate_string(n=10), avatar=account_avatar)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload,headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_first_name(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update(object_id=account_info_id, firstname=generate_string(n=10))

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload,headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_last_name(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update(object_id=account_info_id, lastname=generate_string(n=10))

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload,headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_avatar(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update(object_id=account_info_id, avatar=account_avatar)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload,headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_without_modifications(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update(object_id=account_info_id)

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 200, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_account_info))

        return account_api_key, account_id

    ##########
    ##########
    def test_account_info_update_with_wrong_id(self):
        """
        Update AccountInfo entry by ID
        :return:
        """

        account_api_key, account_id, account_info_id, account_avatar = self.test_account_info_fetch_one()

        request_headers = default_headers
        request_headers['Api-Key-User'] = str(account_api_key)

        payload = account_info_update()

        url = self.API_PREFIX_EXTERNAL + "/accounts/" + str(account_id) + "/info/" + str(account_info_id) + "/"

        response = self.app.patch(url, data=payload, headers=request_headers)
        unittest.TestCase.assertEqual(self, response.status_code, 400, msg=response.data)
        unittest.TestCase.assertTrue(self, is_json(json_object=response.data), msg=response.data)
        unittest.TestCase.assertTrue(self, validate_json(response.data, schema_request_error_detail_as_str))

        return account_api_key, account_id

    ##########
    ##########


if __name__ == '__main__':
    unittest.main()
