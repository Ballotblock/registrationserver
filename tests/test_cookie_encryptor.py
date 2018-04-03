#!/usr/bin/env python3
#
# tests/test_cookie_encryptor.py
# Authors:
#   Samuel Vargas
#

from src.account_types import AccountType
from src.server import app
from src.cookie_encryptor import CookieEncryptor
import unittest
import json


class CookieEncryptorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.secret_password = "SECRET_PASSWORD"
        self.cookie_encryptor = CookieEncryptor(self.secret_password)

        # Create an account token
        self.token = json.dumps({
            "username": "Sparky",
            "password": "Student Loans",
            "account_type": AccountType.voter.value
        }).encode('utf-8')

    def test_can_encrypt_decrypt_cookie(self):
        # Encrypt the token
        encrypted = self.cookie_encryptor.encrypt(self.token)
        assert self.token != encrypted

        # Decrypt the token
        decrypted = self.cookie_encryptor.decrypt(encrypted)
        assert self.token == decrypted
