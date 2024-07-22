import json
import os
import portalocker
from scripts.database.fileController import read, write
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.log_error import log_error
from scripts.database.getDeposit import getDeposit
from scripts.tracker.getHistoricalProfit import getHistoricalProfit

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateEquity(magic, profit, time, account):
    accountData = account
    account = accountData["login"]
    if str(magic) not in getDeletedSets(account):
        try:
            deposit = getDeposit(account)
            historicalProfit = getHistoricalProfit(magic, accountData)
            equity = float(deposit) + float(historicalProfit) + float(profit)
            
            file_path = os.path.join(databaseFolder, account, f"{magic}.json")
            set_data = read(file_path)
            set_data["equity"].append({
                        "time": time,
                        "equity": equity,
                        "profit": profit,
                    })
            write(file_path, set_data)

        except portalocker.LockException as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Equity)  LockException: {e} - Failed to acquire lock for file {file_path}"
            print(errMsg)
            log_error(errMsg)
        
        except FileNotFoundError as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Equity)  FileNotFoundError: {e} - File {file_path} not found while updating equity for magic {magic}"
            print(errMsg)
            log_error(errMsg)
        
        except KeyError as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Equity)  KeyError: {e} - Required key not found in set data while updating equity for magic {magic}"
            print(errMsg)
            log_error(errMsg)
        
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Update Equity)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)
