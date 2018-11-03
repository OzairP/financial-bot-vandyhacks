'''
Functions that run each feature on the backend
This file exclusively contains features that require no Machine Learning Capability
'''

import requests
import json
import geocoder
import datetime
from calendar import monthrange
from backend.EnvironmentConfigurations import CAPITAL_ONE_API_KEY
from backend.UsefulFunctions import great_circle_distance


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
    else: # some other failures
        return {'message': "Unknown Error Occurred"}

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
        for atm in r["data"]:
            atm["address"]
            atm["hours"]
        return {"message": "Here are list of Capital One ATMs near you:\n"
                           ""}


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
        notes = str()
        for note in closest_branch["notes"]:  #
            notes = notes + ", " + note
        address = closest_branch["address"]
        address = address["street_number"] + " " + address["street_name"] + " " + address["city"] + " " \
                  + address["state"] + " " + address["zip"]

        message = f"The closest Capital One branch is {min_distance} miles away.\nBranch Name: " \
                  + closest_branch["name"] + ".\nPhone: " + closest_branch["phone_number"] + "\n Address: " \
                  + address + "\nHours Today: " \
                  + closest_branch["hours"][(datetime.datetime.today().weekday() + 1) % 7] + f"\nNotes: {notes}"
        del notes
        return {"message": message}
    elif status == 404:  # invalid user id
        return {'message': "User ID not found"}
    elif status == 401:  # Invalid api key
        return {'message': r.json()['message']}
    else:  # some other failures
        return {'message': "Unknown Error Occurred"}

def deposit_hist():
    r = requests.get(f"http://api.reimaginebanking.com/accounts/{user_id}/deposit?key={CAPITAL_ONE_API_KEY}")
    statusC = r.status_code
    today = datetime.date.today()
    cnt = 0
    info = []
    if today.day > 10: #same month same year
        for i in range(11):     #in theory, this should work
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                #check if in info.append(r.json()['description'])
    ##might be a problem here sense we change day in loop above
    elif today.day <= 10: #Same year, different month
        while today.day > 0: #go through until we get to the begining of the month
            cnt + 1
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        daysOfLastMonth = monthrange(today.year, (today.month-1))[1]
        daysLeft = 10 - cnt
        for i in range(daysLeft):
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        if today.month < 2: #we go back a year
            while today.day > 0:  # go through until we get to the begining of the month
                cnt + 1
                today.day = today.day - 1
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
                new.day = new.day - 1
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
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
    ##might be a problem here sense we change day in loop above
    elif today.day <= 10:  # Same year, different month
        while today.day > 0:  # go through until we get to the begining of the month
            cnt + 1
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
        daysLeft = 10 - cnt
        for i in range(daysLeft):
            today.day = today.day - 1
            if r.json()['transaction_date'] == today:
                info.append(r.json()['transaction_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        if today.month < 2:  # we go back a year
            while today.day > 0:  # go through until we get to the begining of the month
                cnt + 1
                today.day = today.day - 1
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
                new.day = new.day - 1
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
            today.day = today.day - 1
            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
    ##might be a problem here sense we change day in loop above
    elif today.day <= 10:  # Same year, different month
        while today.day > 0:  # go through until we get to the begining of the month
            cnt + 1
            today.day = today.day - 1
            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        daysOfLastMonth = monthrange(today.year, (today.month - 1))[1]
        daysLeft = 10 - cnt
        for i in range(daysLeft):
            today.day = today.day - 1
            if r.json()['purchase_date'] == today:
                info.append(r.json()['purchase_date'])
                info.append(r.json()['status'])
                info.append(r.json()['medium'])
                info.append(r.json()['amount'])
                # check if in info.append(r.json()['description'])
        if today.month < 2:  # we go back a year
            while today.day > 0:  # go through until we get to the begining of the month
                cnt + 1
                today.day = today.day - 1
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
                new.day = new.day - 1
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
