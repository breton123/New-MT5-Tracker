import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5


def getSetName(magic, accountData):
    openMt5(accountData)
    setName = f"Unnamed set {magic}"

    try:
        magic = int(magic)
    except ValueError as e:
        errMsg = f"Task: (Get Set Name)  ValueError: {e} - Invalid magic number: {magic}"
        print(errMsg)
        log_error(errMsg)
        return setName

    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Get Set Name)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return setName

    for order in orders:
        try:
            orderMagic = order[6]
            if orderMagic == magic:
                if order[16] != "" and "[sl" not in order[16] and "[tp" not in order[16] and len(order[16]) > 5:
                    setName = order[16]
        except KeyError as e:
            errMsg = f"Magic: {magic}  Task: (Get Set Name)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Magic: {magic}  Task: (Get Set Name)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)

    return setName