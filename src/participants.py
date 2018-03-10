
# src/participants.py
# Authors:
#   Alex
#


from src.account_types import AccountType
import requests


class Participants():
    def __init__(self,hyperledger):
        self.url = hyperledger
        key = ""
    def add_user(self,username:str, account_type:AccountType):
        new_url = self.url
        if account_type.value == 1:
            new_url += "voters"
            key = "voterId"
        else:
            new_url += "organizers"
            key = "organizerId"

        data = {
            key: username
            }

        result = requests.post(new_url,data)
        if result.status_code == 200:
            return True
        

