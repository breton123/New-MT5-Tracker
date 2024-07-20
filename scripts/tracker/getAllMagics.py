import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def getAllMagics(accountData):
    openMt5(accountData)
    magics = []
    
    try:
        orders = mt5.history_deals_get(0, datetime.now())
        for order in orders:
            if order[6] not in magics:
                if str(order[6]) != "0":
                    magics.append(order[6])
    except Exception as e:
        errMsg = f"Task: (Get All Magics - History Deals)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return magics

    try:
        positions = mt5.positions_get()
        for position in positions:
            if position[6] not in magics:
                if str(position[6]) != "0":
                    magics.append(position[6])
    except Exception as e:
        errMsg = f"Task: (Get All Magics - Positions)  Error retrieving positions: {e}"
        print(errMsg)
        log_error(errMsg)
        return magics

    return magics