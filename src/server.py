#!/usr/bin/env python3
#
# src/server.py
# Authors:
#     Samuel Vargas
#     Alex Gao
#

from typing import NamedTuple

from flask import request,make_response
from src import app

from src.database import Database
from src.database import UseMemory
from src.account_types import AccountType
from src import httpcode
from passlib.hash import argon2

URL = "0.0.0.0"
DEBUG_URL = "127.0.0.1"
NAME = "BallotBlock Registration API"
PORT = 8080
GREET = "<h1>BallotBlock Registration API WIP</h1>"

db = Database(UseMemory)



# Quick testing to see if server is live
@app.route("/")
def index():
    return "BallotBlock Registration Server"
    


@app.route("/api/account", methods=["POST"])
def signup() -> httpcode.HttpCode:
    """
    Accepts a POST request with the following expected JSON Schema:
    Extraneous keys are ignored.

    {
        "username": "User",
        "password": "Password",
        "account_type": "voter" or "election_creator",
    }
    :return An HttpCode with the message + status of the request
    """

    content = request.get_json(silent=True, force=True)
    if content is None:
        return httpcode.MISSING_OR_MALFORMED_JSON

    if "username" not in content or \
       "password" not in content or \
       "account_type" not in content:
        return httpcode.SIGNUP_MISSING_PARAMETERS

    if not AccountType.isValidType(content['account_type']):
        return httpcode.SIGNUP_INVALID_ACCOUNT_TYPE

    if not db.add_user(content['username'],
                       content['password'],
                       AccountType[content['account_type']]):
        return httpcode.USER_ALREADY_EXISTS

    return httpcode.SIGNUP_OK


@app.route("/api/token", methods=["POST"])
def login() -> httpcode.HttpCode:
    """
    Accepts a POST request with the following expected JSON Schema:
    Extraneous keys are ignored.

    {
        "username": "User",
        "password": "Password",
    }

    If username/password combo is valid, an access token is returned, set via as a cookie in the browser. 

    """
    content = request.get_json(silent=True, force=True)
    if content is None:
        return httpcode.MISSING_OR_MALFORMED_JSON

    if "username" not in content or \
       "password" not in content:
        return httpcode.SIGNUP_MISSING_PARAMETERS

    user = db.find_user(content['username'])

    # check user exists
    if user == None:
        return httpcode.USER_DOESNT_EXISTS

    # check password matches
    if not argon2.verify(content['password'],user[1]):
        return httpcode.WRONG_PASSWORD

    # return access token
    # Note that the access token is not yet encrypted from a secret , most likely use PyJWT encode or another library based on preference
    # Will need to implemented in the future, so clients cannot generate there own tokens and plug into their browsers
    # Also note that the secret used to encrypt here also needs to be the same secret used to decerypt on the BallotBlock-API server (intermediary server)
    # Expires is set to never right now, can be changed in the future to 15 mins or something
    token = {
        'username': content['username'],
        'expires' : 'never'  
        }
    response = make_response(str(token))
    response.set_cookie('token',str(token))
    response.status_code = 202
    return response


