import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getFrontendSets(account):
    account = str(account)
    sets = []
    try:
        folder_path = os.path.join(databaseFolder, account)
        if len(os.listdir(folder_path)) > 0:
            for file in os.listdir(folder_path):
                print(file)
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r') as jsonFile:
                    try:
                        portalocker.lock(jsonFile, portalocker.LOCK_SH)
                        data = json.load(jsonFile)
                        sets.append(data)
                    finally:
                        portalocker.unlock(jsonFile)
    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Task: (Get Frontend Sets)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        if folder_path != "C:\\Users\\Server\\AppData\\Local\\Mt5TrackerDatabase\\favicon.ico":
            errMsg = f"Account: {account}  Task: (Get Frontend Sets)  FileNotFoundError: {e} - Account folder '{folder_path}' not found"
            print(errMsg)
            log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Get Frontend Sets)  Unexpected error: {e} occurred while loading frontend sets for account '{account}'"
        print(errMsg)
        log_error(errMsg)

    return sets