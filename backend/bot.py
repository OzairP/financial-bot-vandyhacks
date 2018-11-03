import MLFeatures from backend      #These import
import nonMLFeatures from backend   #statements need to be fixed
class bot():
    @staticmethod
    def talk(say):
        return(say)
    @staticmethod
    def parse(query, conv):
        conv+1;
        query.lower()
        decision = "Null" #something to mark no value
        words = query.split(" ")
        for i in words:
            if i == "balance":
                return balance()
            elif i == "atm":
                return atmFind()
            elif i == "branch":
                return branchFind()
            elif i == "withdraw":
                if decision == "make" and not decision == "Null":
                    return makeWithdraw()
                else:
                    return withdrawHist()
            elif i == "deposit":
                if decision == "make" and not decision == "Null":
                    return makeDeposit()
                else:
                    return depositHist()
            elif i == "purchase":
                if decision == "make" and not decision == "Null":
                    return makePurchase()
                else:
                    return purchaseHist()
            elif i == "transfer":
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
                    if i == "yes":
                        transfer()
                    else:
                        talk("Canceled Transfer.")
                        return "Ok Cancel"
            elif i == "loan":
                if conv == 1: #what amount
                    talk("What amount would you like to be loaned?: ")
                    parse(nextQuery,conv)
                if conv == 2: #confirm?
                    talk("Are you sure you want this loan?")
                    parse(nextQuery,conv)
                if conv == 3:
                    if i == "yes":
                        loan()
                    else:
                        talk("Canceled loan.")
                        return "Ok Cancel"


