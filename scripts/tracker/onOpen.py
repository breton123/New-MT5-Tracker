import datetime as datetime
from scripts.database.createAccountFolder import createAccountFolder
from scripts.database.findSet import findSet
from scripts.database.getSets import getSets
from scripts.database.log_error import log_error
from scripts.tracker.createSet import createSet
from scripts.tracker.getAllMagics import getAllMagics
from scripts.tracker.openMt5 import openMt5

def onOpen(account):
    openMt5(account)
    accountData = account
    account = account["login"]
    try:
        createAccountFolder(account)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (On Open)  Error creating account folder: {e}"
        print(errMsg)
        log_error(errMsg)
        return

    try:
        magics = getAllMagics(accountData)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (On Open)  Error retrieving magic numbers: {e}"
        print(errMsg)
        log_error(errMsg)
        return

    try:
        sets = getSets(account)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (On Open)  Error retrieving sets from database: {e}"
        print(errMsg)
        log_error(errMsg)
        sets = []

    for magic in magics:
        try:
            foundSet = findSet(sets, magic)
            if not foundSet:
                print(f"Creating set {magic}")
                createSet(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (On Open)  Error creating set: {e}"
            print(errMsg)
            log_error(errMsg)