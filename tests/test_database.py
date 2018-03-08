#!/usr/bin/env python3
#
# tests/test_database.py
# Authors:
#   Samuel Vargas
#

import unittest
from src.database import Database
from src.database import UseMemory
from src.account_types import AccountType


class DatabaseTest(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(self):
        server = 'ballotblock.database.windows.net'
        database = 'BallotBlockUsers'
        username = 'alex'
        password = 'Capstone486'
        driver = '{ODBC Driver 13 for SQL Server}'
        path = 'DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password

        self.db = Database(path)
        self.user = {
            "username": "Robert');DROP TABLE Users",
            "password": "https://xkcd.com/327/",
            "account_type": "voter",
        }

        self.non_existent_user = "Sam"

    def test_add_find_user(self):
        assert self.db.add_user(self.user['username'],
                                self.user['password'],
                                AccountType[self.user['account_type']]),\
            "Adding user to empty database should work."

        assert self.db.find_user(self.user['username']), \
            "Database finds existing user"

        assert not self.db.find_user(self.non_existent_user), \
            "Database does not find non-existing user"

        assert not self.db.add_user(self.user['username'],
                                    self.user['password'],
                                    AccountType[self.user['account_type']]), \
            "Database should return false on request to add an existing user."

    @classmethod
    def tearDownClass(self):
        self.db.close()
