import json
import os
import portalocker
from scripts.database.log_error import log_error
from scripts.tracker.getProfitFactor import getProfitFactor

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateProfitFactor(magic, account):
    accountData = account
    account = accountData["login"]
    try:
        newProfitFactor = getProfitFactor(magic, accountData)
        
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        
        # Lock the file for reading and writing
        with open(file_path, "r+") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)

                # Read existing data from JSON file
                set_data = json.load(file)

                # Update profit factor in the loaded data
                set_data["stats"]["profitFactor"] = newProfitFactor

                # Move the file pointer to the beginning of the file to overwrite it
                file.seek(0)
                file.truncate()

                # Write updated data back to JSON file
                json.dump(set_data, file, indent=4)
                
                file.flush()  # Ensure all data is written to disk
                os.fsync(file.fileno())

            finally:
                portalocker.unlock(file)

    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit Factor)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit Factor)  FileNotFoundError: {e} - File {file_path} not found while updating profit factor for magic {magic}"
        print(errMsg)
        log_error(errMsg)
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit Factor)  KeyError: {e} - Required key not found in set data while updating profit factor for magic {magic}"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit Factor)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)