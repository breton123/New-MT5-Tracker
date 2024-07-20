import os
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def createAccountFolder(account):
    account = str(account)
    try:
        folder_path = f"{databaseFolder}\\{account}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except FileNotFoundError as e:
        errMsg = f"Account: {account}  Task: (Create Accounts Folder)  FileNotFoundError: {e} - Unable to create account folder '{folder_path}', parent directory not found"
        print(errMsg)
        log_error(errMsg)
    except PermissionError as e:
        errMsg = f"Account: {account}  Task: (Create Accounts Folder)  PermissionError: {e} - Unable to create account folder '{folder_path}', permission denied"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Create Accounts Folder)  Unexpected error: {e} occurred while creating account folder '{folder_path}'"
        print(errMsg)
        log_error(errMsg)