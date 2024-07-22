import json
import os
import portalocker
from scripts.database.fileController import read
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getTerminalFolder(account):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, "Accounts", f"{account}.json")
        if os.path.exists(file_path):
            config = read(file_path)
            return config.get("terminalFilePath", "")  
        else:
            errMsg = f"Task: (Get Terminal Path)  File {file_path} not found while getting terminal path for account {account}"
            print(errMsg)
            log_error(errMsg)
            return 0  # Return a default value
            

    except portalocker.LockException as e:
        errMsg = f"Task: (Get Terminal Path)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except FileNotFoundError:
        errMsg = f"Task: (Get Terminal Path)  File {file_path} not found while getting terminal path for account {account}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except KeyError as e:
        errMsg = f"Task: (Get Terminal Path)  KeyError: {e} - 'terminalPath' key not found in account configuration for account {account}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except Exception as e:
        errMsg = f"Task: (Get Terminal Path)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value