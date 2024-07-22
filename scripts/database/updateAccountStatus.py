import json
import os
import portalocker
from scripts.database.fileController import read, write
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def updateAccountStatus(account, newStatus):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, "Accounts", f"{account}.json")

        accountData = read(file_path)
        accountData["status"] = newStatus
        write(file_path, accountData)

    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Task: (Insert Trade)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Task: (Insert Trade)  FileNotFoundError: {e} - Unable to update status, file not found at {file_path}"
        print(errMsg)
        log_error(errMsg)
    except json.JSONDecodeError as e:
        errMsg = f"Account: {account}  Task: (Insert Trade)  JSONDecodeError: {e} - Error decoding JSON data from file at {file_path}"
        print(errMsg)
        log_error(errMsg)
    except KeyError as e:
        errMsg = f"Account: {account}  Task: (Insert Trade)  KeyError: {e} - 'status' key not found in JSON data"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Insert Trade)  Unexpected error: {e} occurred while updating status"
        print(errMsg)
        log_error(errMsg)