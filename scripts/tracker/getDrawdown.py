import time
import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime, timedelta

from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.getReturnOnDrawdown import getReturnOnDrawdown
from scripts.database.getSet import getSet
from scripts.database.log_error import log_error
from scripts.database.updateDrawdown import updateDrawdown
from scripts.database.updateEquity import updateEquity
from scripts.database.updateMaxDrawdown import updateMaxDrawdown
from scripts.database.updateReturnOnDrawdown import updateReturnOnDrawdown
from scripts.tracker.getHistoricalProfit import getHistoricalProfit
from scripts.tracker.openMt5 import openMt5

def getDrawdown(account):
    openMt5(account)
    accountData = account
    account = account["login"]
    try:
        positions = mt5.positions_get()
    except Exception as e:
        errMsg = f"Task: (Get Drawdown)  Error getting positions: {e}"
        print(errMsg)
        log_error(errMsg)
        return
    except Exception as e:
        print(e)

    drawdown = {}
    profitList = {}
    currentTime = round(time.time())
    
    for position in positions:
        try:
            tradeid = position[7]
            tradeTime = position[1]
            magic = position[6]
            volume = position[9]
            profit = position[15]
            symbol = position[16]
            
            if magic not in profitList:
                profitList[magic] = profit
            else:
                profitList[magic] += profit
            
        except KeyError as e:
            errMsg = f"Account: {account}  Task: (Get Drawdown)  KeyError: {e} - Error accessing position details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Account: {account}  Task: (Get Drawdown)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)
    
    for magic in profitList:
        if str(magic) not in getDeletedSets(account):
            try:
                currentDrawdown = round(profitList[magic], 2)
                currentProfit = round(profitList[magic], 2)
                if float(currentDrawdown) > 0:
                    currentDrawdown = 0
                
                print(f"Magic: {magic}  Drawdown: {currentDrawdown}  Profit: {currentProfit}")
                updateDrawdown(magic, currentDrawdown, currentTime, accountData)
                updateEquity(magic, currentProfit, currentTime, accountData)
                
                try:
                    setFile = getSet(magic, accountData)
                except Exception as e:
                    errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Drawdown)  Error getting set file: {e}"
                    print(errMsg)
                    log_error(errMsg)
                    continue
                
                try:
                    maxD = setFile["stats"]["maxDrawdown"]
                except KeyError as e:
                    errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Drawdown)  KeyError: {e} - 'maxDrawdown' key not found in set file"
                    print(errMsg)
                    log_error(errMsg)
                    continue
                
                if maxD == "-":
                    print(f"New Max Drawdown for {magic}")
                    historicalProfit = getHistoricalProfit(magic, accountData)
                    try:
                        returnOnDrawdown = getReturnOnDrawdown(magic, currentDrawdown, account, historicalProfit)
                        updateMaxDrawdown(magic, currentDrawdown, account)
                        updateReturnOnDrawdown(magic, returnOnDrawdown, account)
                    except Exception as e:
                        errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Drawdown)  Error updating max drawdown or return on drawdown: {e}"
                        print(errMsg)
                        log_error(errMsg)
                elif currentDrawdown < float(maxD):
                    print(f"New Max Drawdown for {magic}")
                    historicalProfit = getHistoricalProfit(magic, accountData)
                    try:
                        returnOnDrawdown = getReturnOnDrawdown(magic, currentDrawdown, account, historicalProfit)
                        updateMaxDrawdown(magic, currentDrawdown, account)
                        updateReturnOnDrawdown(magic, returnOnDrawdown, account)
                    except Exception as e:
                        errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Drawdown)  Error updating max drawdown or return on drawdown: {e}"
                        print(errMsg)
                        log_error(errMsg)
            except Exception as e:
                errMsg = f"Account: {account}  Magic: {magic}  Task: (Get Drawdown)  Unexpected error: {e}"
                print(errMsg)
                log_error(errMsg)
    return currentTime