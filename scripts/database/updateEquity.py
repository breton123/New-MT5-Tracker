import json
import os
import portalocker
from scripts.database.log_error import log_error
from scripts.database.getDeposit import getDeposit
from scripts.tracker.getHistoricalProfit import getHistoricalProfit

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def updateEquity(magic, profit, time, account):
    accountData = account
    account = accountData["login"]
    try:
        # Calculate profit percentage based on absolute profit and deposit
        deposit = getDeposit(account)
        # Calculate new equity including historical profit and current profit
        historicalProfit = getHistoricalProfit(magic, accountData)
        equity = float(deposit) + float(historicalProfit) + float(profit)
        
        # Lock the file for reading and writing
        file_path = os.path.join(databaseFolder, account, f"{magic}.json")
        with open(file_path, "r+") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)

                # Load the set JSON from file
                set_data = json.load(file)

                # Append new equity data to the "equity" list in the JSON
                set_data["equity"].append({
                    "time": time,
                    "equity": equity,
                    "profit": profit,
                })

                # Move the file pointer to the beginning of the file to overwrite it
                file.seek(0)
                file.truncate()

                # Write back the updated set JSON to file
                json.dump(set_data, file, indent=4)
                file.flush()  # Ensure all data is written to disk
                os.fsync(file.fileno())
            finally:
                portalocker.unlock(file)

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
