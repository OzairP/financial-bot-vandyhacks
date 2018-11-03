from backend.MLFeatures import *
from backend.nonMLFeatures import *
from backend.Useful import keywords


class Bot:
    """
    Only contains static methods. Shouldn't be instantiated as an object
    """
    # Singleton Pattern
    def __init__(self):
        self.__conversation_count = 1

    @property
    def conversation_count(self):
        return self.__conversation_count

    def __conversation_increment(self):
        self.__conversation_count += 1

    def __new_conversation(self):
        self.__conversation_count = 1

    @staticmethod
    def talk(say):
        return {"message": say}

    def parse(self, user_id, query):
        """
        :param user_id: user_id for the current user sending requests
        :param query: String for query = user input
        :return: return messages that the user will see
        """
        query = query.lower()
        words = query.split(" ")
        parsed_query = set()
        # Input: given a list of strings, arr. & List of strings reference
        # Objective, find whether each reference element exists in the list
        for word in words:
            if word in keywords:
                parsed_query.add(word)

        if "balance" in parsed_query:
            self.__new_conversation()
            return get_balance(user_id)
        elif "atm" in parsed_query:
            self.__new_conversation()
            return atm_find()
        elif "branch" in parsed_query:
            self.__new_conversation()
            return branch_find()
        elif "withdraw" in parsed_query:
            self.__new_conversation()
            return withdraw_hist()
        elif "deposit" in parsed_query:
            self.__new_conversation()
            return deposit_hist()
        elif "purchase" in parsed_query:
            self.__new_conversation()
            if "make" in parsed_query:
                return make_purchase()
            else:
                return purchase_hist()
        # Need to figure out a good way to pass parameters conversation_count through server
        elif "transfer" in parsed_query:
            if self.__conversation_count == 1:  # who do we transfer to
                self.__conversation_increment()
                return Bot.talk("Who would you like to transfer to?: ")
            if self.__conversation_count == 2:  # what amount
                self.__conversation_increment()
                return Bot.talk("What amount would you like to transfer?: ")
            if self.__conversation_count == 3:  # confirm?
                self.__conversation_increment()
                return Bot.talk("Are you sure you want to make this transfer?")
            if self.__conversation_count == 4:
                self.__new_conversation()
                if "yes" in parsed_query:
                    return transfer()
                else:
                    return Bot.talk({"message": "Transfer is Canceled"})
        elif "loan" in parsed_query:
            if self.__conversation_count == 1:  # what amount
                self.__conversation_increment()
                return Bot.talk("What amount would you like to be loaned?")
            if self.__conversation_count == 2:  # confirm?
                self.__conversation_increment()
                return Bot.talk("Are you sure you want this loan?")
            if self.__conversation_count == 3:
                self.__new_conversation()
                if "yes" in parsed_query:
                    return loan()
                else:
                    return Bot.talk("Canceled loan.")


