#!/usr/bin/env python3
#
# tests/signup.py
# Authors:
#   Samuel Vargas
#

import unittest
import json
from src import server
from src import httpcode


class SignupTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = server.app.test_client()
        self.user_data = {
            "username": "Robert');DROP TABLE Users",
            "password": "https://xkcd.com/327/",
            "account_type": "voter",
        }

    def test_sign_up(self):
        result = self.app.post("/api/signup",
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(self.user_data))

        # User is allowed to register to vote as a voter.
        expectedCode = httpcode.SIGNUP_OK.code
        expectedMessage = httpcode.SIGNUP_OK.message
        actualCode = result.status_code
        actualMessage = result.data.decode('utf-8')

        assert actualCode == expectedCode and \
               actualMessage == expectedMessage, \
            "Expected ({0}, {1}) got ({2}, {3})".format(
                expectedMessage, expectedCode, actualMessage, actualCode
            )

    def test_sign_up_no_json(self):
        # Sign up with 0 json parameters -> get rejected
        result = self.app.post("/api/signup",
                               headers={'Content-Type': 'application/json'},
                               data=None)

        expectedCode = httpcode.MISSING_OR_MALFORMED_JSON.code
        expectedMessage = httpcode.MISSING_OR_MALFORMED_JSON.message
        actualCode = result.status_code
        actualMessage = result.data.decode('utf-8')

    def test_sign_up_dupe_name_rejected(self):
        # Signup again with the same user, -> get rejected
        result = self.app.post("/api/signup",
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(self.user_data))

        # Duplicate signups are rejected
        expectedCode = httpcode.USER_ALREADY_EXISTS.code
        expectedMessage = httpcode.USER_ALREADY_EXISTS.message
        actualCode = result.status_code
        actualMessage = result.data.decode('utf-8')

    def test_sign_up_missing_parameters(self):
        user_missing_password = {
            "username": "Sam",
            "account_type": "election_creator"
        }

        user_missing_username = {
            "password": "password",
            "account_type": "election_creator"
        }

        user_missing_account_type = {
            "username": "Sam",
            "password": "password",
        }

        # Sign up with missing password -> get rejected
        user_missing_password = self.app.post("/api/signup",
                                              headers={'Content-Type': 'application/json'},
                                              data=json.dumps(user_missing_password))

        # Sign up with missing username -> get rejected
        user_missing_username = self.app.post("/api/signup",
                                              headers={'Content-Type': 'application/json'},
                                              data=json.dumps(user_missing_username))

        # Sign up with missing account_type -> get rejected
        user_missing_account_type = self.app.post("/api/signup",
                                                  headers={'Content-Type': 'application/json'},
                                                  data=json.dumps(user_missing_account_type))

        for result in [user_missing_password, user_missing_username, user_missing_account_type]:
            expectedCode = httpcode.SIGNUP_MISSING_PARAMETERS.code
            expectedMessage = httpcode.SIGNUP_MISSING_PARAMETERS.message
            actualCode = result.status_code
            actualMessage = result.data.decode('utf-8')

            assert actualCode == expectedCode and \
                   actualMessage == expectedMessage, \
                "Expected ({0}, {1}) got ({2}, {3})".format(
                    expectedMessage, expectedCode, actualMessage, actualCode
                )

    def test_signup_invalid_account_type(self):
        user_invalid_account_type = {
            "username": "Sam",
            "password": "password",
            "account_type": "foobar",
        }

        result = self.app.post("/api/signup",
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(user_invalid_account_type))

        expectedCode = httpcode.SIGNUP_INVALID_ACCOUNT_TYPE.code
        expectedMessage = httpcode.SIGNUP_INVALID_ACCOUNT_TYPE.message
        actualCode = result.status_code
        actualMessage = result.data.decode('utf-8')

        assert actualCode == expectedCode and \
               actualMessage == expectedMessage, \
            "Expected ({0}, {1}) got ({2}, {3})".format(
                expectedMessage, expectedCode, actualMessage, actualCode
            )
