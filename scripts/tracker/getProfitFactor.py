import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def getProfitFactor(magic, accountData):
    openMt5(accountData)
    try:
        magic = int(magic)
    except ValueError as e:
        errMsg = f"Task: (Get Profit Factor)  ValueError: {e} - Invalid magic number: {magic}"
        print(errMsg)
        log_error(errMsg)
        return None

    totalProfit = 0
    totalLoss = 0

    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Get Profit Factor)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return None

    for order in orders:
        try:
            orderMagic = order[6]
            if orderMagic == magic:
                profit = order[13]
                if profit >= 0:
                    totalProfit += profit
                else:
                    totalLoss += profit
        except KeyError as e:
            errMsg = f"Magic: {magic}  Task: (Get Profit Factor)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Magic: {magic}  Task: (Get Profit Factor)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)

    try:
        if totalLoss == 0:
            return round(totalProfit, 2)
        else:
            return round(totalProfit / totalLoss, 2)
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Get Profit Factor)  Error calculating profit factor: {e}"
        print(errMsg)
        log_error(errMsg)
        return None
