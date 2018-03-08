#!/usr/bin/env python3
#
# src/database.py
# Authors:
#     Samuel Vargas
#     Alex Gao

from typing import Optional
from passlib.hash import argon2
from src.account_types import AccountType
import pyodbc

TABLE_NAME = "User"

CREATE_SCHEMA = """

IF NOT EXISTS (SELECT 'X'
                   FROM   INFORMATION_SCHEMA.TABLES
                   WHERE  TABLE_NAME = 'User'
                          AND TABLE_SCHEMA = 'dbo')
BEGIN
    CREATE TABLE "{table_name}"
        (username nvarchar(450) NOT NULL,
        password nvarchar(450) NOT NULL,
        account_type INT NOT NULL,
        PRIMARY KEY(username))
END
""".format(table_name=TABLE_NAME)

FIND_USER = """
SELECT * FROM "{table_name}" WHERE username=?
""".format(table_name=TABLE_NAME)

ADD_USER = """
INSERT "{table_name}" (username, password, account_type)
    VALUES (?, ?, ?)
""".format(table_name=TABLE_NAME)

UseMemory = ":memory:"


class Database:
    def __init__(self, path):
        self.connection = pyodbc.connect(path)
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
        self.connection.commit()
        return True

    def close(self) -> None:
        self.connection.close()
