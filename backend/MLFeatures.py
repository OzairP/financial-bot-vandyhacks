#Purchase pattern

#spending too much
    #get deposit/purchase history
    #considering a list of deposit history& puchase hist
    #we can compare each point to determine if
    #the amount of money is more than being deposited
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
