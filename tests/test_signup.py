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

        expectedCode = httpcode.SIGNUP_OK.code
        expectedMessage = httpcode.SIGNUP_OK.message
        actualCode = result.status_code
        actualMessage = result.data.decode('utf-8')

        assert actualCode == expectedCode and \
               actualMessage == expectedMessage, \
            "Expected ({0}, {1}) got ({2}, {3})".format(expectedMessage, expectedCode, actualMessage, actualCode)
