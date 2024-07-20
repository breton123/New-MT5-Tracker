import os
import portalocker
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def setExist(magic, account):
    account = str(account)
    try:
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        
        # Attempt to open the file for reading
        with open(file_path, "r") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_SH)  # Shared lock for reading
                return True
            finally:
                portalocker.unlock(file)
    except FileNotFoundError:
        # Handle the case where the file does not exist
        return False
    except Exception as e:
        # Log any unexpected errors
        errMsg = f"Account: {account}  Magic: {magic}  Task: (Set Exist)  Error checking if set exists for magic {magic} and account {account}: {e}"
        print(errMsg)
        log_error(errMsg)
        return False