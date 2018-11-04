from backend.Features import *
from backend.Useful import keywords


class Bot:
    """
    Should ne only 1 instance running.
    """
    def __init__(self):
        self.__conversation_info = []  # any temporary variable to hold

    def __new_conversation(self): # reset conversation status
        self.__conversation_info = []

    @staticmethod
    def talk(say):
        return {
            "message": say
        }

    def parse(self, user_id, query):
        """
        :param user_id: user_id for the current user sending requests
        :param query: String for query = user input
        :return: return messages that the user will see
        """
        try:
            query = query.lower()
            # get rid of non alphabet, non numeric, non whitespace
            query = ''.join([i for i in query if i.isalpha() or i == ' ' or ('0' <= i <= '9')])
            # print(query)
            words = query.split(" ")
            parsed_query = set()
            # Input: given a list of strings, arr. & List of strings reference
            # Objective, find whether each reference element exists in the list
            for word in words:
                if word in keywords:
                    parsed_query.add(word)
            # print(parsed_query)
            if "balance" in parsed_query:
                self.__new_conversation()
                return get_balance(user_id)
            elif "atm" in parsed_query:
                self.__new_conversation()
                return atm_find()
            elif "branch" in parsed_query or "bank" in parsed_query or "store" in parsed_query: # TODO may be more keywords
                self.__new_conversation()
                return branch_find()
            elif "withdraw" in parsed_query or "withdrawal" in parsed_query:
                self.__new_conversation()
                return withdraw_hist(user_id)
            elif "deposit" in parsed_query or "deposits" in parsed_query:
                self.__new_conversation()
                return deposit_hist(user_id)
            elif "purchase" in parsed_query or "purchases" in parsed_query or "payment" in parsed_query or "payments" in parsed_query:
                self.__new_conversation()
                # if "make" in parsed_query:
                #     return make_purchase()
                # else:
                return purchase_hist(user_id)
            # Wizarding for transferring money
            elif "transfer" in parsed_query and not self.__conversation_info: # no information from conversation yet
                self.__new_conversation()
                self.__conversation_info.append("intent") # intent to transfer
                return Bot.talk("Who would you like to transfer to? Please only type the account number where you'd like to send money to, otherwise we can't help you!")
            elif len(self.__conversation_info) == 1:
                r = requests.get(f"http://api.reimaginebanking.com/accounts/{words[0]}?key={CAPITAL_ONE_API_KEY}")
                if r.status_code == 200:
                    self.__conversation_info.append(words[0])  # actual account has been selected
                    return Bot.talk("Wonderful! How much money are you transferring to this account?")
                else:
                    return Bot.talk("I don't recognize that account. Please type the account number again. Make sure you have the right account number!")
            elif len(self.__conversation_info) == 2:
                if words[0].isdigit(): # Money to transfer has been correctly inputted
                    self.__conversation_info.append(words[0])
                    return Bot.talk("Final check. Are you sure that you want to make this transaction?")
                else:  # repeat
                    return Bot.talk("For clarification, please just type in the number.")
            elif len(self.__conversation_info) == 3:
                if "yes" in parsed_query or "yeah" in parsed_query:
                    return transfer(user_id, self.__conversation_info[1], float(self.__conversation_info[2]))
                elif "no" in parsed_query or "nope" in parsed_query:
                    self.__new_conversation()
                    return Bot.talk("Got ya. I'll cancel the transfer.")
                else:  # repeat step
                    return Bot.talk("Please, just say yes or no")

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
            else:
                self.__new_conversation()
                return Bot.talk("I'm sorry. I haven't learned that yet :( ")
        except Exception as e:
            self.__new_conversation()
            return {"message": "Uh oh. There was a system failure..."}
