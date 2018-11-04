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
    r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    print(status)
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


def atm_find():
    my_loc = geocoder.ip('me').latlng
    print(my_loc)
    r = requests.get(f"http://api.reimaginebanking.com/atms?lat={my_loc[0]}&lng={my_loc[1]}&rad=100&key={CAPITAL_ONE_API_KEY}")
    status = r.status_code
    print(status)
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
    print(status)
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


def transfer(user_id, payee_id, amount):
    r = requests.get(f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
    if r.status_code != 200:
        return {'message': ErrorMessages.NO_ACCOUNT_ERROR}

    print(user_id, CAPITAL_ONE_API_KEY)
    print(r.json())
    print(r.status_code)
    ### TODO seems to be failing here
    r = requests.post(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['id']}/transfers?key={CAPITAL_ONE_API_KEY}",
                      data={
                          "medium": "balance",
                          "payee_id": payee_id,
                          "amount": amount
                      })
    status = r.status_code
    print(status)
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


def deposit_hist(user_id):
    r = requests.get(
        f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
    if r.status_code != 200:
        return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/deposit?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []
    visited = False

    if today.day > 10: #same month same year
        visited = True

        for i in range(11):     #in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                #check if in info.append(r.json()['description'])


    elif today.day <= 10 and not visited: #Same year, different month
        visited = True

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
        return {'message': "I'm sorry, who are you?"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "You've gotta be really far out there to get this one."}


def withdraw_hist(user_id):
    r = requests.get(
        f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
    if r.status_code != 200:
        return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/withdrawals?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []
    visited = False #I use this to stop us from going into two of the same loops due to
                    #The value of today.day being modified by one loop, which can affect the next

    if today.day > 10:  # same month same year
        visited = True
        for i in range(11):  # in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

    elif today.day <= 10 and not visited:  # Same year, different month
        visited = True

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

            daysOfLastMonth = monthrange(today.year, (today.month - 1))[1] #days in the month we're changing to
            daysLeft = 10 - cnt     #how many more days we need to get
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
        return {'message': "I don't know you, back up"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "Like I said before, don't know how you get here"}


def payment_hist(user_id):
    r = requests.get(
        f"http://api.reimaginebanking.com/customers/{user_id}/accounts?key={CAPITAL_ONE_API_KEY}")
    if r.status_code != 200:
        return {'message': ErrorMessages.NO_ACCOUNT_ERROR}
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{r.json()[0]['_id']}/purchases?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code

    today = datetime.date.today()
    cnt = 0
    info = []
    visited = False

    if today.day > 10:  # same month same year
        visited = True

        for i in range(11):  # in theory, this should work
            today = today.replace(today.day - 1)

            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])

    elif today.day <= 10 and not visited:  # Same year, different month
        visited = True
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

            while today.day > 0:  # go through until we get to the beginning of the month
                cnt = cnt + 1
                today = today.replace(today.day - 1)

                if r.json()['purchase_date'] == today:
                    info.append(r.json()['purchase_date'])
                    info.append(r.json()['status'])
                    info.append(r.json()['medium'])
                    info.append(r.json()['amount'])
                    # check if in info.append(r.json()['description'])
            daysOfLastMonth = monthrange(today.year, (today.month - 1))[1] #gives you the number of days in the month
            daysLeft = 10 - cnt #Calculate the days left after taking away the days we've already went through

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
        return {'message': "Hey man, I found your payment from the past 10 days:",
                'arguments': info}  # maybe find a better way to feed arguments

    elif statusC == 404:  # invalid user id
        return {'message': "And you are? (I don't know who you are)"}

    elif statusC == 401:  # Invalid api key
        return {'message': r.json()['message']}

    else:  # some other failures
        return {'message': "Unknown Error"}