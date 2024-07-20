import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5


def getTradeAmount(magic, account):
    openMt5(account)
    account = account["login"]
    amount = 0
    try:
        orders = mt5.history_deals_get(0, datetime.now())
        for order in orders:
            order = order._asdict()
            if order["magic"] == magic:
                if order["reason"] == 4:
                    amount += 1  
        return amount     
    
    except Exception as e:
        errMsg = f"Task: (Get Trade Amount)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return amount