from backend.MLFeatures import *
from backend.nonMLFeatures import *


class Bot:

    @staticmethod
    def talk(say):
        return say

    @staticmethod
    def parse(user_id, query, conv):
        conv+1
        query = query.lower()
        decision = None  # something to mark no value
        words = query.split(" ")
        for word in words:
            if word == "balance":
                return get_balance(user_id)
            elif word == "atm":
                return atm_find()
            elif word == "branch":
                return branch_find()
            elif word == "withdraw":
                if (decision == "make") and (decision is not None):
                    return make_withdraw(user_id, money)
                else:
                    return withdraw_hist()
            elif word == "deposit":
                if decision == "make" and not decision == "Null":
                    return make_deposit()
                else:
                    return deposit_hist()
            elif word == "purchase":
                if decision == "make" and not decision == "Null":
                    return make_purchase()
                else:
                    return purchase_hist()
            elif word == "transfer":
                if conv == 1: #who do we transfer to
                    talk("Who would you like to tansfer to?: ")
                    parse(nextQuery,conv)
                if conv == 2: #what amount
                    talk("What amount would you like to transfer?: ")
                    parse(nextQuery,conv)
                if conv == 3: #confirm?
                    talk("Are you sure you want to make this transfer?")
                    parse(nextQuery,conv)
                if conv == 4:
                    if word == "yes":
                        transfer()
                    else:
                        talk("Canceled Transfer.")
                        return "Ok Cancel"
            elif word == "loan":
                if conv == 1: #what amount
                    talk("What amount would you like to be loaned?: ")
                    parse(nextQuery,conv)
                if conv == 2: #confirm?
                    talk("Are you sure you want this loan?")
                    parse(nextQuery,conv)
                if conv == 3:
                    if word == "yes":
                        loan()
                    else:
                        talk("Canceled loan.")
                        return "Ok Cancel"


