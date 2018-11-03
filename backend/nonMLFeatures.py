'''
Functions that run each feature on the backend
This file exclusively contains features that require no Machine Learning Capability
'''


import requests
import EnvironmentConfigurations

def get_balance(user_id, query):
    r = requests.get("http://api.reimaginebanking.com/merchants?key= % s" % api_key)