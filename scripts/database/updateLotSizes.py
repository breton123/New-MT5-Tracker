import json
import os
import portalocker
from scripts.database.fileController import read, write
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateLotSizes(account, magic, lotSizes):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        set_data = read(file_path)
        set_data["stats"]["minLotSize"] = lotSizes["minLotSize"]
        set_data["stats"]["maxLotSize"] = lotSizes["maxLotSize"]
        set_data["stats"]["avgLotSize"] = lotSizes["avgLotSize"]
        write(file_path, set_data)

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