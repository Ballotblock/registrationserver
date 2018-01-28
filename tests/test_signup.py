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
            "test_database": True
        }

    def test_sign_up(self):
        result = self.app.post("/api/signup",
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(self.user_data))

        assert result.status_code == httpcode.SIGNUP_OK.code and \
               result.data.decode('utf-8') == httpcode.SIGNUP_OK.message, \
            "Expected {0}, found {1}".format(httpcode.SIGNUP_OK, (result.response, result.status_code))