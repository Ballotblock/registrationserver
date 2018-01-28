#!/usr/bin/env python3
#
# src/server.py
# Authors:
#     Samuel Vargas
#

from typing import NamedTuple

from flask import request
from flask import Flask

from src.database import Database
from src.database import UseMemory
from src import httpcode

URL = "0.0.0.0"
DEBUG_URL = "127.0.0.1"
NAME = "BallotBlock Registration API"
PORT = 8080
GREET = "<h1>BallotBlock Registration API WIP</h1>"

db = Database(UseMemory)
app = Flask(__name__)


@app.route("/api/signup", methods=["GET", "POST"])
def signup() -> httpcode.HttpCode:
    """
    Accepts a POST request with the following expected JSON Schema:
    Extraneous keys are ignored.

    {
        "username": "User",
        "password": "Password",
    }
    :return An HttpCode with the message + status of the request
    """
    content = request.get_json(silent=True, force=True)
    if content is None:
        return httpcode.MISSING_OR_MALFORMED_JSON

    if "username" not in content or "password" not in content:
        return httpcode.SIGNUP_MISSING_PARAMETERS

    if not db.add_user(content['username'], content['password']):
        return httpcode.USER_ALREADY_EXISTS

    return httpcode.SIGNUP_OK
