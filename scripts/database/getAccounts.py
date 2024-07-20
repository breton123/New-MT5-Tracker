import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getAccounts():
    accounts = []
    try:
        for file in os.listdir(os.path.join(databaseFolder, "Accounts")):
            file_path = os.path.join(databaseFolder, "Accounts", file)
            with open(file_path, "r") as f:
                try:
                    portalocker.lock(f, portalocker.LOCK_SH)
                    accounts.append(json.load(f))
                finally:
                    portalocker.unlock(f)
    except portalocker.LockException as e:
        errMsg = f"Task: (Get Accounts)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Task: (Get Accounts)  Error: {e} - Accounts folder not found at {os.path.join(databaseFolder, 'Accounts')}"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Task: (Get Accounts)  Unexpected error: {e} occurred while loading accounts"
        print(errMsg)
        log_error(errMsg)
    return accounts