import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime

from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def getDaysLive(magic, accountData):
    openMt5(accountData)
    try:
        magic = int(magic)
    except ValueError as e:
        errMsg = f"Task: (Get Days Live)  ValueError: {e} - Invalid magic number: {magic}"
        print(errMsg)
        log_error(errMsg)
        return 0

    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Get Days Live)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return 0

    for order in orders:
        try:
            orderMagic = order[6]
            if orderMagic == magic:
                orderTime = order[2]
                date_time = datetime.fromtimestamp(orderTime)
                current_time = datetime.now()
                time_difference = current_time - date_time
                days_difference = time_difference.days
                return days_difference
        except KeyError as e:
            errMsg = f"Magic: {magic}  Task: (Get Days Live)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Magic: {magic}  Task: (Get Days Live)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)

    return 0