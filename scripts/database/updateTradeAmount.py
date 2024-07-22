import json
import os
import portalocker
from scripts.database.fileController import read, write
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def updateTradeAmount(account, magic, trades):
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        set_data = read(file_path)
        set_data["stats"]["trades"] = trades
        write(file_path, set_data)

    except portalocker.LockException as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Trade Amount)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Trade Amount)  FileNotFoundError: {e} - File {file_path} not found while updating Trade Amount for magic {magic}"
        print(errMsg)
        log_error(errMsg)
    except KeyError as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Trade Amount)  KeyError: {e} - Required key not found in set data while updating Trade Amount for magic {magic}"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Trade Amount)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)