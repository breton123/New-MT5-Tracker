import json
import os
import portalocker
from scripts.database.fileController import write
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def insertSet(newSet, account):
    account = str(account)
    try:
        # Attempt to retrieve the magic value
        magic = newSet["stats"]["magic"]
    except KeyError as e:
        errMsg = f"Account: {account}  Task: (Insert Set)  KeyError: {e} - 'stats' or 'magic' key not found in new set"
        print(errMsg)
        log_error(errMsg)
        magic = None

    if magic:
        # Construct the file path
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")

        # Check if the file already exists
        if os.path.exists(file_path):
            ## This error is fine
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Insert Set)  Set file already exists at {file_path}"
            #print(errMsg)
            #log_error(errMsg)
        else:
            try:
                write(file_path, newSet)
            except portalocker.LockException as e:
                errMsg = f"Account: {account}  Magic: {magic}  Task: (Insert Set)  LockException: {e} - Failed to acquire lock for file {file_path}"
                print(errMsg)
                log_error(errMsg)
            except IOError as e:
                errMsg = f"Account: {account}  Magic: {magic}  Task: (Insert Set)  IOError: {e} - An error occurred while accessing the file system"
                print(errMsg)
                log_error(errMsg)
            except Exception as e:
                errMsg = f"Account: {account}  Magic: {magic}  Task: (Insert Set)  Unexpected error: {e}"
                print(errMsg)
                log_error(errMsg)
    else:
        errMsg = f"Account: {account}  Task: (Insert Set)  The magic key could not be retrieved, skipping file operations"
        print(errMsg)
        log_error(errMsg)