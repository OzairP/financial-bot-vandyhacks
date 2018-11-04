import numpy as np
import pandas as pd
from backend.EnvironmentConfigurations import CAPITAL_ONE_API_KEY
import requests

"""
Fills up accounts. Not part of the backend architecture. Independent script
"""
# MM: lots of deposits, lots of withdrawals
# AE: Some deposit some withdrawal
# RZ: lots of deposits, some withdrawals
# WB: lots of deposits, no withdrawals
# GP: No nothing

first_names = ["Michael", "Albert", "Robert", "Warren", "Grigori"]
last_names = ["Milken", "Einstein", "Zimmermann", "Buffett", "Perelman"]

customer_ids = ["5bde5ff33bdbba398b44289d", "5bde60363bdbba398b44289f", "5bde605a3bdbba398b4428a0", "5bde601c3bdbba398b44289e", "5bde606d3bdbba398b4428a1"]
account_ids = {"5bde71563bdbba398b4428a2", "5bde71763bdbba398b4428a3", "5bde71d33bdbba398b4428a4", "5bde71ee3bdbba398b4428a5", "5bde72163bdbba398b4428a6"}


class Person:
    def __init__(self, account_id):
        self._account_id = account_id
        self._deposits = []
        self._withdrawals = []
        self._purchases = []

    @property
    def deposits(self):
        return self._deposits

    @property
    def withdrawals(self):
        return self._withdrawals

    @property
    def purchases(self):
        return self._purchases

    def deposit(self, date, range):
        r = requests.post(f"http://api.reimaginebanking.com/accounts/{self._account_id}/deposits?key={CAPITAL_ONE_API_KEY}", json =
        {
            "medium": "balance",
            "transaction_date": date,
            "amount": round(np.random.uniform(range[0], range[1]),2)
        })
        print(r.json())
        # print(int(np.random.uniform(range[0], range[1])))
        if r.status_code == 201:
            self._deposits.append(r.json()["objectCreated"]["amount"])

    def withdraw(self, date, range):
        r = requests.post(f"http://api.reimaginebanking.com/accounts/{self._account_id}/withdrawals?key={CAPITAL_ONE_API_KEY}", json =
        {
            "medium": "balance",
            "transaction_date": date,
            "amount": round(np.random.uniform(range[0], range[1]),2)
        })
        print(r.json())
        # print(int(np.random.uniform(range[0], range[1])))
        self._withdrawals.append(r.json()["objectCreated"]["amount"])

    def purchase(self, date, range):

        merchants = requests.get(f"http://api.reimaginebanking.com/merchants?lat=33.906904&lng=-84.739134&rad=10&key={CAPITAL_ONE_API_KEY}").json()
        for merchant in merchants:
            r = requests.post(f"http://api.reimaginebanking.com/accounts/{self._account_id}/purchases?key={CAPITAL_ONE_API_KEY}", json =
            {
                "merchant_id": merchant["_id"],
                "medium": "balance",
                "purchase_date": date,
                "amount": int(np.random.uniform(range[0], range[1]))
            })
            print(r.json())
            # print(int(np.random.uniform(range[0], range[1])))
            if r.status_code == 200:
                self._deposits.append(r.json()["objectCreated"]["amount"])

Persons = []
for id in account_ids:
    Persons.append(Person(id))

for person in Persons:
    for i in range(1, 32):
        if i < 10:
            date = f"2018-10-0{i}"
        else:
            date = f"2018-10-{i}"

        if i%2 ==0:
            person.deposit(date, (10000, 20000))
            person.purchase(date, (500, 1000))
        elif i%2 ==1:
            person.withdraw(date, (500, 1000))
            person.purchase(date, (100, 200))


