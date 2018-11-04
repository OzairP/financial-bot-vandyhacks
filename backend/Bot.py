from backend.MLFeatures import *
from backend.nonMLFeatures import *
from backend.Useful import keywords
import re

class Bot:
    """
    Only contains static methods. Shouldn't be instantiated as an object
    """
    # Singleton Pattern
    def __init__(self):
        self.__conversation_count = 1
        self.__temporary_aux = []  # any temporary variable to hold

    @property
    def conversation_count(self):
        return self.__conversation_count

    def __conversation_increment(self):
        self.__conversation_count += 1

    def __new_conversation(self):
        self.__conversation_count = 1

    @staticmethod
    def talk(say, suffix=None):
        if suffix is None:
            return {"message": say}
        else:
            return {
                "message": say,
                "suffix": suffix
            }

    def parse(self, user_id, query):
        """
        :param user_id: user_id for the current user sending requests
        :param query: String for query = user input
        :return: return messages that the user will see
        """
        query = query.lower()
        query = ''.join([i for i in query if i.isalpha() or i == ' ' or ('0' <= i <= '9')])
        print(query)
        words = query.split(" ")
        parsed_query = set()
        # Input: given a list of strings, arr. & List of strings reference
        # Objective, find whether each reference element exists in the list
        for word in words:
            if word in keywords:
                parsed_query.add(word)
        print(parsed_query)
        if "balance" in parsed_query:
            self.__new_conversation()
            self.__temporary_aux = None
            return get_balance(user_id)
        elif "atm" in parsed_query:
            self.__new_conversation()
            self.__temporary_aux = None
            return atm_find()
        elif "branch" in parsed_query: # TODO may be more keywords
            self.__new_conversation()
            self.__temporary_aux = None
            return branch_find()
        elif "withdraw" in parsed_query:
            self.__new_conversation()
            self.__temporary_aux = None
            return withdraw_hist(user_id)
        elif "deposit" in parsed_query:
            self.__new_conversation()
            self.__temporary_aux = None
            return deposit_hist(user_id)
        # elif "purchase" in parsed_query:
        #     self.__new_conversation()
        #     self.__temporary_aux = None
        #     if "make" in parsed_query:
        #         return make_purchase()
        #     else:
        #         return purchase_hist()
        # Need to figure out a good way to pass parameters conversation_count through server
        elif "transfer" in parsed_query:
            if self.__conversation_count == 1:  # who do we transfer to
                self.__conversation_increment()
                print(user_id)
                return Bot.talk("Who would you like to transfer to?", "transfer, account_number")
            if self.__conversation_count == 2:  # what amount
                self.__conversation_increment()
                self.__temporary_aux.append(words[len(words)-1])  # contains account number info
                print(user_id)
                return Bot.talk("What amount would you like to transfer to ?", "transfer, amount of transfer")
            if self.__conversation_count == 3:  # confirm?
                self.__conversation_increment()
                self.__temporary_aux.append(float(words[len(words) - 1]))  # contains amount of transfer
                print(user_id)
                return Bot.talk("Are you sure you want to make this transfer?", "transfer, yes/no")
            if self.__conversation_count == 4:
                self.__new_conversation()
                payee_id = self.__temporary_aux[0]
                amount = self.__temporary_aux[1]
                self.__temporary_aux = None
                if "yes" in parsed_query:
                    print(user_id)
                    return transfer(user_id, payee_id, amount)
                else:
                    return Bot.talk({"message": "Transfer is Canceled"})
        # elif "loan" in parsed_query:
        #     if self.__conversation_count == 1:  # what amount
        #         self.__conversation_increment()
        #         return Bot.talk("What amount would you like to be loaned?", "loan, account_number")
        #     if self.__conversation_count == 2:  # confirm?
        #         self.__temporary_aux.append(words[len(words) - 1])  # contains account number for the loan
        #         self.__conversation_increment()
        #         return Bot.talk("What amount would you like to be loaned?", "loan, amount of loan")
        #     if self.__conversation_count == 3:
        #         self.__temporary_aux.append(float(words[len(words) - 1]))  # contains amount of loan
        #         return Bot.talk("Are you sure you want this loan?", "loan, yes/no")
        #     if self.__conversation_count == 4:
        #         self.__new_conversation()
        #         self.__temporary_aux = None
        #         if "yes" in parsed_query:
        #             return loan(self.__temporary_aux[0], self.__temporary_aux[0])
        #         else:
        #             return Bot.talk("Canceled loan.")
