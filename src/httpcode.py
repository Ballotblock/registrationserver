#!/usr/bin/env python3
#
# src/httpcode.py
# Authors:
#     Samuel Vargas
#

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
    _httpcode("Missing 'Username' or 'Password'", status.HTTP_400_BAD_REQUEST)

USER_ALREADY_EXISTS = \
    _httpcode("Cannot signup, username already exists.", status.HTTP_409_CONFLICT)
