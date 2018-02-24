#!/usr/bin/env python3
#
# src/httpcode.py
# Authors:
#     Samuel Vargas
#     

from src.account_types import AccountType
from typing import NamedTuple
from collections import namedtuple
from flask_api import status

HttpCode = NamedTuple("httpcode", [("message", str), ("code", int)])
_httpcode = namedtuple("httpcode", ("message", "code"))

# Successful (2xx)
SIGNUP_OK = \
    _httpcode("Signup successfully completed.", status.HTTP_201_CREATED)

# Client Errors (4xx)
MISSING_OR_MALFORMED_JSON = \
    _httpcode("JSON was not provided or is non parseable", status.HTTP_400_BAD_REQUEST)

SIGNUP_MISSING_PARAMETERS = \
    _httpcode("Missing 'username', 'password', or 'account_type'", status.HTTP_400_BAD_REQUEST)

SIGNUP_INVALID_ACCOUNT_TYPE = \
    _httpcode("'account_type' was sent but was invalid, valid options are: {0}"
              .format(AccountType.getEnumsAsList()), status.HTTP_400_BAD_REQUEST)

USER_ALREADY_EXISTS = \
    _httpcode("Cannot signup, username already exists.", status.HTTP_409_CONFLICT)

USER_DOESNT_EXISTS = \
    _httpcode("Cannot login, username does not exists.", status.HTTP_404_NOT_FOUND)

WRONG_PASSWORD = \
    _httpcode("Cannot login, password does not match username.", status.HTTP_403_FORBIDDEN)

