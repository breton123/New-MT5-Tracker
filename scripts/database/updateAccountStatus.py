import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def updateAccountStatus(account, newStatus):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, "Accounts", f"{account}.json")

        # Lock the file for reading and writing
        with open(file_path, "r+") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)

                # Read existing data from JSON file
                accountData = json.load(file)

                # Append new trade to the 'trades' list in the loaded JSON data
                accountData["status"] = newStatus

                # Move the file pointer to the beginning of the file to overwrite it
                file.seek(0)
                file.truncate()

                # Write updated data back to JSON file
                json.dump(accountData, file, indent=4)
                file.flush()  # Ensure all data is written to disk
                os.fsync(file.fileno())
            finally:
                portalocker.unlock(file)

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