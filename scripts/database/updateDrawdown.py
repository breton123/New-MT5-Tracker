import json
import os
import statistics
import portalocker
from scripts.database.fileController import read, write
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateDrawdown(magic, drawdown, time, account):
    accountData = account
    account = accountData["login"]
    if str(magic) not in getDeletedSets(account):
        try:
            
            file_path = os.path.join(databaseFolder, account, f"{magic}.json")
            set_data = read(file_path)
            allDrawdown = []
            for setDrawdown in set_data["drawdown"]:
                allDrawdown.append(setDrawdown["drawdown"])
            
            allDrawdown.append(drawdown)
            averageDrawdown = round(statistics.mean(allDrawdown),2)
            
            set_data["stats"]["avgDrawdown"] = averageDrawdown
            set_data["drawdown"].append({
                        "time": time,
                        "drawdown": drawdown
                    })
            write(file_path, set_data)

        except portalocker.LockException as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Drawdown)  LockException: {e} - Failed to acquire lock for file {file_path}"
            print(errMsg)
            log_error(errMsg)
        except FileNotFoundError as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Drawdown)  FileNotFoundError: {e} - File {file_path} not found while updating drawdown for magic {magic}"
            print(errMsg)
            log_error(errMsg)
        except KeyError as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Drawdown)  KeyError: {e} - Required key not found in set data while updating drawdown for magic {magic}"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Drawdown)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)