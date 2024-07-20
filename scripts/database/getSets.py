import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

 
def getSets(account):
    account = str(account)
    sets = []
    try:
        folder_path = os.path.join(databaseFolder, account)
        
        # Check if the account folder exists and has files
        if os.path.exists(folder_path) and len(os.listdir(folder_path)) > 0:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                
                # Attempt to load JSON data from each file
                with open(file_path, 'r') as jsonFile:
                    try:
                        portalocker.lock(jsonFile, portalocker.LOCK_SH)  # Shared lock for reading
                        data = json.load(jsonFile)
                        sets.append(data)
                    finally:
                        portalocker.unlock(jsonFile)
    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Task: (Get Sets)  LockException: {e} - Failed to acquire lock for file"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Task: (Get Sets)  FileNotFoundError: {e} - Account folder '{folder_path}' not found"
        print(errMsg)
        log_error(errMsg)
    except json.JSONDecodeError as e:
        errMsg = f"Account: {account}  Task: (Get Sets)  JSONDecodeError: {e} - Error decoding JSON data from file '{file_path}'"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Get Sets)  Unexpected error: {e} occurred while loading sets for account '{account}'"
        print(errMsg)
        log_error(errMsg)
    
    return sets
