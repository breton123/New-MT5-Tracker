
from datetime import datetime
import time
from scripts.database.log_error import log_error
from scripts.database.resetErrorLog import resetErrorLog
from scripts.database.updateAccountStatus import updateAccountStatus
from scripts.database.updateDaysLive import updateDaysLive
from scripts.database.updateLotSizes import updateLotSizes
from scripts.database.updateTradeAmount import updateTradeAmount
from scripts.database.updateTradeTimes import updateTradeTimes
from scripts.database.updateWinRate import updateWinRate
from scripts.tracker.getAllMagics import getAllMagics
from scripts.tracker.getDrawdown import getDrawdown
from scripts.tracker.getLotSizes import getLotSizes
from scripts.tracker.getTradeAmount import getTradeAmount
from scripts.tracker.getTradeTimes import getTradeTimes
from scripts.tracker.getWinRate import getWinRate
from scripts.tracker.onOpen import onOpen
from scripts.tracker.openMt5 import openMt5
from scripts.tracker.terminalController import isTerminalOpen
from scripts.tracker.updateHistoricalTrades import updateHistoricalTrades

def trackData(accountData):
    while True:
        try:
            try:
                openMt5(accountData)
                resetErrorLog()
                account = accountData["login"]
            except Exception as e:
                errMsg = f"Account: {account}  Task: (Track Data)  Error opening MT5 terminal: {e}"
                print(errMsg)
                log_error(errMsg)
                return

            try:
                onOpen(accountData)
            except Exception as e:
                errMsg = f"Account: {account}  Task: (Track Data)  Error executing onOpen function: {e}"
                print(errMsg)
                log_error(errMsg)
                return
            time.sleep(5)
            updateAccountStatus(account, "tracking")
            while True:
                try:
                    updateTime = getDrawdown(accountData)
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error in getDrawdown: {e}"
                    print(errMsg)
                    log_error(errMsg)

                try:
                    updateHistoricalTrades(accountData)
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error in updateHistoricalTrades: {e}"
                    print(errMsg)
                    log_error(errMsg)

                try:
                    updateDaysLive(accountData)
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating days live: {e}"
                    print(errMsg)
                    log_error(errMsg)

                try:
                    for magic in getAllMagics(accountData):
                        trades = getTradeAmount(magic, accountData)
                        updateTradeAmount(account, magic, trades)
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating lot sizes: {e}"
                    print(errMsg)
                    log_error(errMsg)

                    
                try:
                    for magic in getAllMagics(accountData):
                        updateLotSizes(account, magic, getLotSizes(magic, accountData))
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating lot sizes: {e}"
                    print(errMsg)
                    log_error(errMsg)
                    
                try:
                    for magic in getAllMagics(accountData):
                        updateWinRate(account, magic, getWinRate(magic, accountData))
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating win rate: {e}"
                    print(errMsg)
                    log_error(errMsg)
                    
                try:
                    for magic in getAllMagics(accountData):
                        updateTradeTimes(account, magic, getTradeTimes(magic, accountData))
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating trade times: {e}"
                    print(errMsg)
                    log_error(errMsg)

                try:
                    if not isTerminalOpen(accountData["terminalFilePath"]):
                        openMt5(accountData)
                except Exception as e:
                    errMsg = f"Account: {account}  Task: (Track Data)  Error updating days live: {e}"
                    print(errMsg)
                    log_error(errMsg)
                updateTime = datetime.fromtimestamp(updateTime)
                print(f"Latest Update: {updateTime}")
                time.sleep(10)
        except Exception as e:
            errMsg = f"Account: {account}  Task: (Track Data)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)
