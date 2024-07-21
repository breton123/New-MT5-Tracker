import json
import os
import portalocker
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

                # Lock the file for reading and writing
                with open(file_path, "r+") as file:
                    try:
                        portalocker.lock(file, portalocker.LOCK_EX)

                        # Load JSON data from file
                        set_data = json.load(file)

                        # Update daysLive in the loaded data
                        set_data["stats"]["daysLive"] = getDaysLive(magic, accountData)

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