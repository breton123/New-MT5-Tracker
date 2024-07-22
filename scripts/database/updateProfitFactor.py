import json
import os
import portalocker
from scripts.database.fileController import read, write
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
        set_data = read(file_path)
        set_data["stats"]["profitFactor"] = newProfitFactor
        write(file_path, set_data)

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