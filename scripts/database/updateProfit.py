import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')



def updateProfit(magic, profit, account):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")

        # Lock the file for reading and writing
        with open(file_path, "r+") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)

                # Read existing data from JSON file
                set_data = json.load(file)

                # Update profit in the loaded JSON data
                set_data["stats"]["profit"] = profit

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
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit)  FileNotFoundError: {e} - Unable to update profit for magic {magic}, file not found at {file_path}"
        print(errMsg)
        log_error(errMsg)
    except json.JSONDecodeError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit)  JSONDecodeError: {e} - Error decoding JSON data from file at {file_path}"
        print(errMsg)
        log_error(errMsg)
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit)  KeyError: {e} - 'stats' or 'profit' key not found in JSON data for magic {magic}"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Profit)  Unexpected error: {e} occurred while updating profit for magic {magic}"
        print(errMsg)
        log_error(errMsg)