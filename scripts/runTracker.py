
import threading
from scripts.database.getAccounts import getAccounts
from scripts.tracker.trackData import trackData
trackingAccounts = []

def run():
    global trackingAccounts
    for account in getAccounts():
        if account["login"] not in trackingAccounts:
            if account["type"] == "master":
                trackerThread = threading.Thread(target=trackData, args=(account,)).start()
                trackingAccounts.append(account["login"])
            elif account["type"] == "slave":
                trackerThread = threading.Thread(target=trackData, args=(account,)).start()
                trackingAccounts.append(account["login"])

