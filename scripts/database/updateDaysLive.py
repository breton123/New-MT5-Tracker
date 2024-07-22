import json
import os
import portalocker
from scripts.database.fileController import read, write
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.log_error import log_error
from scripts.tracker.getAllMagics import getAllMagics
from scripts.tracker.getDaysLive import getDaysLive

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def updateDaysLive(account):
    accountData = account
    account = accountData["login"]
    try:
        magics = getAllMagics(accountData)
        for magic in magics:
            if str(magic) not in getDeletedSets(account):
                file_path = os.path.join(databaseFolder, account, f"{magic}.json")
                set_data = read(file_path)
                set_data["stats"]["daysLive"] = getDaysLive(magic, accountData)
                write(file_path, set_data)

    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Task: (Update Days Live)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    
    except FileNotFoundError:
        errMsg = f"Account: {account}  Task: (Update Days Live)  File {magic}.json not found"
        print(errMsg)
        log_error(errMsg)
    
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Days Live)  KeyError: {e} - Error accessing JSON data"
        print(errMsg)
        log_error(errMsg)
    
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Update Days Live)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)