'''
Functions that run each feature on the backend
This file exclusively contains features that require no Machine Learning Capability
'''

import requests
import json
from backend.EnvironmentConfigurations import CAPITAL_ONE_API_KEY


def get_balance(user_id):
    # GET requests to for balance
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{user_id}?key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    print("HTTP RESPONSE: ", status)  # print out status code for debugging
    if status == 200:
        return {'message': "Your current Balance is " + r.json()['balance']}
    elif status == 404:  # invalid user id
        return {'message': "User ID not found"}
    elif status == 401:  # Invalid api key
        return {'message': r.json()['message']}


def withdraw(user_id, money):
    r = requests.post(f"http://api.reimaginebanking.com/accounts/{user_id}/withdrawals?key={CAPITAL_ONE_API_KEY}", json.dumps(money))
    status = r.status_code


def deposit(user_id, money):
    r = requests.post(f"http://api.reimaginebanking.com/accounts/{user_id}/deposits?key={CAPITAL_ONE_API_KEY}", json.dumps(money))
    status = r.status_code


