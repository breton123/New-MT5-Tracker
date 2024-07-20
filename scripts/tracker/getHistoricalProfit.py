import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime

from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def getHistoricalProfit(magic, accountData):
    openMt5(accountData)
    totalProfit = 0
    
    try:
        magic = int(magic)
    except ValueError as e:
        errMsg = f"Task: (Get Historical Profit)  ValueError: {e} - Invalid magic number: {magic}"
        print(errMsg)
        log_error(errMsg)
        return round(totalProfit, 2)

    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Get Historical Profit)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return round(totalProfit, 2)

    for order in orders:
        try:
            orderMagic = order[6]
            if orderMagic == magic:
                profit = order[13]
                totalProfit += profit
        except KeyError as e:
            errMsg = f"Magic: {magic}  Task: (Get Historical Profit)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Magic: {magic}  Task: (Get Historical Profit)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)

    return round(totalProfit, 2)