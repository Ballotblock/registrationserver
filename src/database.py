#!/usr/bin/env python3
#
# src/database.py
# Authors:
#     Samuel Vargas

from typing import Optional
from passlib.hash import argon2
from src.account_types import AccountType
import sqlite3

TABLE_NAME = "User"

CREATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name}
    (username TEXT NOT NULL,
     password TEXT NOT NULL,
     account_type INT NOT NULL,
     PRIMARY KEY(username))
""".format(table_name=TABLE_NAME)

FIND_USER = """
SELECT * FROM {table_name} WHERE username=?
""".format(table_name=TABLE_NAME)

ADD_USER = """
INSERT INTO {table_name}(username, password, account_type)
 VALUES (?, ?, ?)
""".format(table_name=TABLE_NAME)

UseMemory = ":memory:"


class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_SCHEMA)
        self.connection.commit()

    def find_user(self, username: str) -> Optional[tuple]:
        self.cursor.execute(FIND_USER, (username,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def add_user(self, username: str, password: str, account_type: AccountType) -> bool:
        """
        Add a user to the database. Refuses if the username
        is already in the database.
        :param username:
        :param password:
        :param account_type:
        :return: False if username already exists, True otherwise
        """
        if self.find_user(username) is not None:
            return False

        self.cursor.execute(ADD_USER, (username, argon2.hash(password), account_type.value))
        return True

    def close(self) -> None:
        self.connection.close()
