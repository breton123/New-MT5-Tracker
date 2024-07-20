import json
import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getDeposit(account):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, "Accounts", f"{account}.json")
        if os.path.exists(file_path):
        # Lock the file for reading
            with open(file_path, "r") as file:
                try:
                    portalocker.lock(file, portalocker.LOCK_SH)  # Shared lock for reading
                        # Load account configuration
                    config = json.load(file)
                    return config.get("deposit", 0)  
                finally:
                    portalocker.unlock(file)
        else:
            errMsg = f"Task: (Get Deposit)  File {file_path} not found while getting deposit for account {account}"
            print(errMsg)
            log_error(errMsg)
            return 0  # Return a default value
            

    except portalocker.LockException as e:
        errMsg = f"Task: (Get Deposit)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except FileNotFoundError:
        errMsg = f"Task: (Get Deposit)  File {file_path} not found while getting deposit for account {account}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except KeyError as e:
        errMsg = f"Task: (Get Deposit)  KeyError: {e} - 'deposit' key not found in account configuration for account {account}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value
    
    except Exception as e:
        errMsg = f"Task: (Get Deposit)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)
        return 0  # Return a default value