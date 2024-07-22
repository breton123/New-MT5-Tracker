import json
import os
import portalocker
from scripts.database.fileController import read
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.log_error import log_error
from scripts.tracker.createSet import createSet

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

    
def getSet(magic, account):
    accountData = account
    account = accountData["login"]
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        
        # Lock the file for reading
        data = read(file_path)
        
        return data

    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Set)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
        return {}
    
    except FileNotFoundError:
        if str(magic) not in getDeletedSets(account):
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Set)  File {magic}.json not found"
            createSet(magic, accountData)
            print(errMsg)
            log_error(errMsg)
        return {}
    
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Set)  KeyError: {e} - Error accessing JSON data"
        print(errMsg)
        log_error(errMsg)
        return {}
    
    except Exception as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Set)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)
        return {}