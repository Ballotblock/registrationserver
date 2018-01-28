#!/usr/bin/env python3
#
# tests/test_database.py
# Authors:
#   Samuel Vargas
#

import unittest
from src.database import Database
from src.database import UseMemory


class DatabaseTest(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(self):
        self.db = Database(UseMemory)
        self.user = {
            "username": "Robert');DROP TABLE Users",
            "password": "https://xkcd.com/327/",
            "test_database": True
        }

        self.non_existent_user = "Sam"

    def test_add_find_user(self):
        assert self.db.add_user(self.user['username'], self.user['password']), \
            "Adding user to empty database should work."

        assert self.db.find_user(self.user['username']), \
            "Database finds existing user"

        assert not self.db.find_user(self.non_existent_user), \
            "Database does not find non-existing user"

        assert not self.db.add_user(self.user['username'], self.user['password']), \
            "Database should return false on request to add an existing user."

    @classmethod
    def tearDownClass(self):
        self.db.close()
