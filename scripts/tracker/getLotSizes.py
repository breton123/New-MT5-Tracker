import statistics
import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def getLotSizes(magic, account):
    lotSizes = []
    openMt5(account)
    account = account["login"]
    try:
        orders = mt5.history_deals_get(0, datetime.now())
        for order in orders:
            order = order._asdict()
            if order["magic"] == magic:
                lotSizes.append(order["volume"])
    except Exception as e:
        errMsg = f"Task: (Get All Magics - History Deals)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return {
            "minLotSize": 0,
            "maxLotSize": 0,
            "avgLotSize": 0
        }

    try:
        positions = mt5.positions_get()
        for position in positions:
            position = position._asdict()
            if position["magic"] == magic:
                lotSizes.append(position["volume"])
    except Exception as e:
        errMsg = f"Task: (Get All Magics - Positions)  Error retrieving positions: {e}"
        print(errMsg)
        log_error(errMsg)
        return {
            "minLotSize": round(min(lotSizes),2),
            "maxLotSize": round(max(lotSizes),2),
            "avgLotSize": round(statistics.mean(lotSizes), 2)
        }

    try:
        return {
                "minLotSize": round(min(lotSizes),2),
                "maxLotSize": round(max(lotSizes),2),
                "avgLotSize": round(statistics.mean(lotSizes), 2)
            }
    except:
        return {
                "minLotSize": 0,
                "maxLotSize": 0,
                "avgLotSize": 0
            }