from backend.MLFeatures import *
from backend.nonMLFeatures import *


class Bot:
    """
    Only contains   static methods. Shouldn't be instantiated as an object
    """
    @staticmethod
    def talk(say):
        return say

    @staticmethod
    def parse(user_id, query, conversation_count=1):
        """

        :param user_id: user_id for the current user sending requests
        :param query: String for query = user input
        :param conversation_count: for wizarding process, if count>1 then we are in wizarding process
        :return: {"message": return message for user to see}
        """
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
                # if (decision == "make") and (decision is not None):
                #     return make_withdraw(user_id, money)
                # else:
                #     return withdraw_hist()
                return withdraw_hist()
            elif word == "deposit":
                # if decision == "make" and not decision == "Null":
                #     return make_deposit()
                # else:
                #     return deposit_hist()
                return deposit_hist()
            elif word == "purchase":
                if decision == "make" and not decision == "Null":
                    return make_purchase()
                else:
                    return purchase_hist()
            # Need to figure out a good way to pass parameters conversation_count through server
            elif word == "transfer":
                if conversation_count == 1: #who do we transfer to
                    Bot.talk("Who would you like to tansfer to?: ")
                    Bot.parse(user_id, nextQuery)
                if conversation_count == 2: #what amount
                    Bot.talk("What amount would you like to transfer?: ")
                    Bot.parse(user_id, nextQuery)
                if conversation_count == 3: #confirm?
                    Bot.talk("Are you sure you want to make this transfer?")
                    Bot.parse(user_id, nextQuery)
                if conversation_count == 4:
                    if word == "yes":
                        transfer()
                    else:
                        return Bot.talk({"message": "Transfer is Canceled"})
            elif word == "loan":
                if conversation_count == 1: #what amount
                    Bot.talk("What amount would you like to be loaned?: ")
                    Bot.parse(user_id, nextQuery)
                if conversation_count == 2: #confirm?
                    Bot.talk("Are you sure you want this loan?")
                    Bot.parse(user_id, nextQuery)
                if conversation_count == 3:
                    if word == "yes":
                        loan()
                    else:
                        Bot.talk("Canceled loan.")
                        return "Ok Cancel"


