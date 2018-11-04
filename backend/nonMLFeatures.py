'''
Functions that run each feature on the backend
This file exclusively contains features that require no Machine Learning Capability
'''

import requests
import geocoder
import datetime
from calendar import monthrange
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
    r = requests.get(f"http://api.reimaginebanking.com/atm?lat={my_loc[0]}&lng={my_loc[1]}&rad=5&key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    if status == 200:
        if not r.json()["data"]:
            return {"messsage": f"Sorry, there are no Capital One ATMs within 5 miles :("}
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


def transfer(user_id ,payee_id, amount):
    r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key=d3647dccce6ddbbb8366ddbc5f747710")
    r = requests.post(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/transfers?key=d3647dccce6ddbbb8366ddbc5f747710",
                      data={
                          "medium": "balance",
                          "payee_id": payee_id,
                          "amount": amount
                      })
    status = r.status_code
    if status == 201:
        message = \
            {
                "message": f"Your money will be transferred to account # {payee_id} within an hour!.",
                "rich_content": {
                    "card_type": "transfer",
                    "arguments": {
                        "payee_id": payee_id,
                        "payer_id": r.json()['payer_id'],
                        "amount": amount,
                        "status": r.json()['status']
                    }
                }
            }
        return message
    elif status == 401:  # Invalid api key
        return {'message': ErrorMessages.API_KEY_ERROR}
    else:  # some other failures
        return {'message': ErrorMessages.UNKNOWN_ERROR}

def deposit_hist():

    r = requests.get(f"http://api.reimaginebanking.com/accounts/{user_id}/deposit?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []

    if today.day > 10: #same month same year

        for i in range(11):     #in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                #check if in info.append(r.json()['description'])

    ##might be a problem here sense we change day in loop above
    elif today.day <= 10: #Same year, different month

        while today.day > 0: #go through until we get to the begining of the month
            cnt = cnt + 1
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

        daysOfLastMonth = monthrange(today.year, (today.month-1))[1]
        daysLeft = 10 - cnt

        for i in range(daysLeft):
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

        if today.month < 2: #we go back a year

            while today.day > 0:  # go through until we get to the begining of the month
                cnt = cnt + 1
                today = today.replace(today.day - 1)

                if r.json()['transaction_date'] == today:
                    info.append(r.json()['transaction_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description'])
            daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
            daysLeft = 10 - cnt

            for i in range(daysLeft):
                new = datetime.date((today.year - 1) , (today.month-1), daysOfLastMonth)
                new = new.replace(new.day - 1)

                if r.json()['transaction_date'] == new:
                    info.append(r.json()['transaction_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description']da12, ((today.day - 10) + daysOfLastMonth))
    else:
        return "I really don't know what year you're in?"

    if statusC == 200:
        return {'message': "Here is your deposits from the past 10 days:",
                'arguments': info} #maybe find a better way to feed arguments

    elif statusC == 404:  # invalid user id
        return {'message': "User ID not found"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "Unknown Error Occurred"}

def withdraw_hist():
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{user_id}/withdrawals?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []

    if today.day > 10:  # same month same year

        for i in range(11):  # in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

    ##might be a problem here sense we change day in loop above
    elif today.day <= 10:  # Same year, different month

        while today.day > 0:  # go through until we get to the begining of the month
            cnt = cnt + 1
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
        daysLeft = 10 - cnt

        for i in range(daysLeft):
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

        if today.month < 2:  # we go back a year

            while today.day > 0:  # go through until we get to the begining of the month
                cnt = cnt + 1
                today = today.replace(today.day - 1)

                if r.json()['transaction_date'] == today:
                    info.append(r.json()['transaction_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description'])

            daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
            daysLeft = 10 - cnt
            for i in range(daysLeft):
                new = datetime.date((today.year - 1), (today.month - 1), daysOfLastMonth)
                new = new.replace(new.day - 1)

                if r.json()['transaction_date'] == new:
                    info.append(r.json()['transaction_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description']da12, ((today.day - 10) + daysOfLastMonth))

    else:
        return "I really don't know what year you're in?"

    if statusC == 200:
        return {'message': "Here is your withdrawals from the past 10 days:",
                'arguments': info}  # maybe find a better way to feed arguments

    elif statusC == 404:  # invalid user id
        return {'message': "User ID not found"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "Unknown Error Occurred"}

def payment_hist():
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{user_id}/purchases?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []

    if today.day > 10:  # same month same year

        for i in range(11):  # in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
    ##might be a problem here sense we change day in loop above

    elif today.day <= 10:  # Same year, different month

        while today.day > 0:  # go through until we get to the begining of the month
            cnt = cnt + 1
            today = today.replace(today.day - 1)

            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
        daysLeft = 10 - cnt

        for i in range(daysLeft):
            today = today.replace(today.day - 1)

            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

        if today.month < 2:  # we go back a year

            while today.day > 0:  # go through until we get to the begining of the month
                cnt = cnt + 1
                today = today.replace(today.day - 1)

                if r.json()['purchase_date'] == today:
                    info.append(r.json()['purchase_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description'])
            daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
            daysLeft = 10 - cnt

            for i in range(daysLeft):
                new = datetime.date((today.year - 1), (today.month - 1), daysOfLastMonth)
                new = new.replace(new.day - 1)

                if r.json()['purchase_date'] == new:
                    info.append(r.json()['purchase_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description']da12, ((today.day - 10) + daysOfLastMonth))

    else:
        return "I really don't know what year you're in?"

    if statusC == 200:
        return {'message': "Here is your payment from the past 10 days:",
                'arguments': info}  # maybe find a better way to feed arguments

    elif statusC == 404:  # invalid user id
        return {'message': "User ID not found"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "Unknown Error Occurred"}