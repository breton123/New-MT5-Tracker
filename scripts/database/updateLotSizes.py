import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateLotSizes(account, magic, lotSizes):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")

        # Lock the file for reading and writing
        with open(file_path, "r+") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)

                # Load JSON data from file
                set_data = json.load(file)

                # Update daysLive in the loaded data
                set_data["stats"]["minLotSize"] = lotSizes["minLotSize"]
                set_data["stats"]["maxLotSize"] = lotSizes["maxLotSize"]
                set_data["stats"]["avgLotSize"] = lotSizes["avgLotSize"]

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
        errMsg = f"Account: {account}  Task: (Update Lot Size)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    
    except FileNotFoundError:
        errMsg = f"Account: {account}  Task: (Update Lot Size)  File {magic}.json not found"
        print(errMsg)
        log_error(errMsg)
    
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Lot Size)  KeyError: {e} - Error accessing JSON data"
        print(errMsg)
        log_error(errMsg)
    
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Update Lot Size)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)