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
    try:
        # GET requests to for balance
        r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
        status = r.status_code
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
    except Exception as e:
        raise e


def atm_find():
    try:
        my_loc = geocoder.ip('me').latlng
        r = requests.get(f"http://api.reimaginebanking.com/atms?lat={my_loc[0]}&lng={my_loc[1]}&rad=100&key={CAPITAL_ONE_API_KEY}")
        status = r.status_code
        if status == 200:
            if not r.json()["data"]:
                return {"message": f"Sorry, I could not find any Capital One ATMs within 5 miles"}
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
    except Exception as e:
        raise e


def branch_find():
    try:
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
                    "message": f"I found a Capital One branch near you {min_distance} miles away.",
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
    except Exception as e:
        raise e


def transfer(user_id, payee_id, amount):
    try:
        r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
        if r.status_code != 200:
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}

        r = requests.post(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/transfers?key={CAPITAL_ONE_API_KEY}", json={
            "medium": "balance",
            "payee_id": payee_id,
            "amount": amount
        })
        status = r.status_code
        if status == 201:
            message = \
                {
                    "message": f"Your money will be transferred to account #{payee_id} within an hour!",
                    "rich_content": {
                        "card_type": "transfer",
                        "arguments": {
                            "payee_id": payee_id,
                            "payer_id": r.json()["objectCreated"]['payer_id'],
                            "amount": amount,
                            "status": r.json()["objectCreated"]['status']
                        }
                    }
                }
            return message
        elif status == 401:  # Invalid api key
            return {'message': ErrorMessages.API_KEY_ERROR}
        else:  # some other failures
            return {'message': ErrorMessages.UNKNOWN_ERROR}

    except Exception as e:
        raise e


def deposit_hist(user_id):
    try:
        r = requests.get(
            f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
        if r.status_code != 200:
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
        r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/deposits?key={CAPITAL_ONE_API_KEY}")
        status = r.status_code

        payer = r.json()[0]['payee_id']
        if status == 200:
            info = {'transaction_date': [], 'amount': []}
            for record in r.json():
                info['transaction_date'].append(record['transaction_date'])
                info['amount'].append(record['amount'])
            message = \
                {
                    "message": "Here's your recent deposit history",
                    "rich_content": {
                        "card_type": "deposit-history",
                        "arguments": {
                            "data": info,
                            "payer_id": payer
                        }
                    }
                }
            return message  # maybe find a better way to feed arguments

        elif status == 404:  # invalid user id
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}

        elif status == 401:  # Invalid api key
            return {'message': ErrorMessages.API_KEY_ERROR}

        else:  # some other failures
            return {'message': ErrorMessages.UNKNOWN_ERROR}
    except Exception as e:
        raise e


def withdraw_hist(user_id):
    try:
        r = requests.get(
            f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
        if r.status_code != 200:
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
        r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/withdrawals?key={CAPITAL_ONE_API_KEY}")
        status = r.status_code

        payer = r.json()[0]['payer_id']
        if status == 200:
            info = {'transaction_date': [], 'amount': []}
            for record in r.json():
                info['transaction_date'].append(record['transaction_date'])
                info['amount'].append(record['amount'])
            message = \
                {
                    "message": "Here's your recent withdrawal history",
                    "rich_content": {
                        "card_type": "withdrawal-history",
                        "arguments": {
                            "data": info,
                            "payer_id": payer
                        }
                    }
                }
            return message  # maybe find a better way to feed arguments

        elif status == 404:  # invalid user id
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}

        elif status == 401:  # Invalid api key
            return {'message': ErrorMessages.API_KEY_ERROR}

        else:  # some other failures
            return {'message': ErrorMessages.UNKNOWN_ERROR}
    except Exception as e:
        raise e


def purchase_hist(user_id):
    try:
        r = requests.get(
            f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
        if r.status_code != 200:
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
        r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/purchases?key={CAPITAL_ONE_API_KEY}")
        status = r.status_code

        payer = r.json()[0]['payer_id']
        if status == 200:
            info = {'purchase_date': [], 'amount': []}
            for record in r.json():
                info['purchase_date'].append(record['purchase_date'])
                info['amount'].append(record['amount'])

            message = \
                {
                    "message": "Here's your recent purchase history",
                    "rich_content": {
                        "card_type": "purchase-history",
                        "arguments": {
                            "data": info,
                            "payer_id": payer
                        }
                    }
                }
            return message  # maybe find a better way to feed arguments

        elif status == 404:  # invalid user id
            return {'message': ErrorMessages.NO_ACCOUNT_ERROR}

        elif status == 401:  # Invalid api key
            return {'message': ErrorMessages.API_KEY_ERROR}

        else:  # some other failures
            return {'message': ErrorMessages.UNKNOWN_ERROR}
    except Exception as e:
        raise e
