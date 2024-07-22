import json
import os
import portalocker
from scripts.database.fileController import write
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def createAccount(account):
    try:
        account_login = account['login']
        accounts_folder = os.path.join(databaseFolder, "Accounts")
        
        # Check if the 'Accounts' folder exists, create it if it doesn't
        if not os.path.exists(accounts_folder):
            os.makedirs(accounts_folder)
        
        file_path = os.path.join(accounts_folder, f"{account_login}.json")

        write(file_path, account)

    except portalocker.LockException as e:
        errMsg = f"Task: (Create Account)  LockException: {e} - Failed to acquire lock for file {file_path}"
        print(errMsg)
        log_error(errMsg)
    
    except FileNotFoundError:
        errMsg = f"Task: (Create Account)  Folder {file_path} not found"
        print(errMsg)
        log_error(errMsg)
    
    except Exception as e:
        errMsg = f"Task: (Create Account)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)
