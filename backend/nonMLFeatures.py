'''
Functions that run each feature on the backend
This file exclusively contains features that require no Machine Learning Capability
'''

import requests
import geocoder
import datetime
from backend.EnvironmentConfigurations import CAPITAL_ONE_API_KEY
from backend.Useful import great_circle_distance, get_address, ErrorMessages


def get_balance(user_id):
    # GET requests to for balance
    r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}accounts?key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    # print("HTTP RESPONSE: ", status)  # print out status code for debugging
    if status == 200:
        message = \
            {
                "message": "Here is a summary of your balances of all your accounts",
                "rich_content": {
                    "card_type": "balance-sheet",
                    "arguments": []
                }
            }
        for account in r.json():
            message["rich_content"]["arguments"].append(
                {
                    "account_name": account["nickname"],
                    "balance": account["balance"]
                }
            )
        return message
    elif status == 404:  # invalid user id
        return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
    elif status == 401:  # Invalid api key
        return {'message': ErrorMessages.API_KEY_ERROR}
    else:  # some other failures
        return {'message': ErrorMessages.UNKNOWN_ERROR}

# Can't really withdraw or deposit $ , maybe connect to a debit card or venmo? but can't really do that here
# # TODO
# def make_withdraw(user_id, money):
#     r = requests.post(f"http://api.reimaginebanking.com/accounts/{user_id}/withdrawals?key={CAPITAL_ONE_API_KEY}", json.dumps(??))
#     status = r.status_code
#
#
# # TODO
# def make_deposit(user_id, money):
#
#     r = requests.post(f"http://api.reimaginebanking.com/accounts/{user_id}/deposits?key={CAPITAL_ONE_API_KEY}", json.dumps(??))
#     status = r.status_code


def atm_find():
    my_loc = geocoder.ip('me').latlng
    r = requests.get(f"http://api.reimaginebanking.com/atm?lat={my_loc[0]}&lng={my_loc[1]}&rad=1&key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    if status == 200:
        if not r.json()["data"]:
            return {"messsage": "Sorry, there are no Capital One ATMs near you :("}
        else:
            message = \
                {
                    "message": "We found some Capital One ATMs near you!",
                    "rich_content": {
                        "card_type": "atm-locations",
                        "arguments": []
                    }
                }
            for atm in r.json()["data"]:
                message["rich_content"]["arguments"].append(
                    {
                        "address": get_address(atm["address"]),
                        "hours": atm["hours"][0]
                    }
                )
            return message
    elif status == 404:  # invalid latitude, longitude pair
        return {'message': ErrorMessages.LOCATION_ERROR}
    elif status == 401:  # Invalid api key
        return {'message': ErrorMessages.API_KEY_ERROR}
    else:  # some other failures
        return {'message': ErrorMessages.UNKNOWN_ERROR}


def branch_find():
    # uses geocode library to find my location
    my_loc = geocoder.ip('me').latlng
    r = requests.get(f"http://api.reimaginebanking.com/branches?key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    if status == 200:
        # find minimum distance
        min_distance = float("inf")
        closest_branch = dict()
        for branch in r.json():  # find minimum distance branch
            loc = branch['geocode']
            loc = (loc['lat'], loc['lng'])
            distance = great_circle_distance(my_loc, loc)
            if min_distance > distance:
                min_distance = distance
                closest_branch = branch
        # Create message
        message = \
            {
                "message": f"Awesome! We found a Capital One branch near you {min_distance} miles away.",
                "rich_content": {
                    "card_type": "closest-branch",
                    "arguments": {
                        "distance": min_distance,
                        "branch_name": closest_branch["name"],
                        "phone_number": closest_branch["phone_number"],
                        "address": get_address(closest_branch["address"]),
                        "hours": closest_branch["hours"][(datetime.datetime.today().weekday() + 1) % 7],
                        "notes": closest_branch["notes"]
                    }
                }
            }
        return message
    elif status == 401:  # Invalid api key
        return {'message': ErrorMessages.API_KEY_ERROR}
    else:  # some other failures
        return {'message': ErrorMessages.UNKNOWN_ERROR}
