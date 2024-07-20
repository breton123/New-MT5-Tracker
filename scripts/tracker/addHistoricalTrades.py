import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime

from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5

def addHistoricalTrades(magic, accountData):
    openMt5(accountData)
    trades = []
    
    try:
        magic = int(magic)
    except ValueError as e:
        errMsg = f"Task: (Add Historical Trades)  ValueError: {e} - Invalid magic number: {magic}"
        print(errMsg)
        log_error(errMsg)
        return trades

    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Magic: {magic}  Task: (Add Historical Trades)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return trades

    for order in orders:
        try:
            orderMagic = order[6]
            if orderMagic == magic and order[8] == 4:
                orderTime = order[2]
                volume = order[9]
                price = order[10]
                profit = round(order[13], 2)
                symbol = order[15]
                newTrade = {
                     "id": order[0],
                    "time": orderTime,
                    "volume": volume,
                    "price": price,
                    "profit": profit,
                    "symbol": symbol,
                    "magic": magic
                }
                trades.append(newTrade)
                print(newTrade)
        except KeyError as e:
            errMsg = f"Magic: {magic}  Task: (Add Historical Trades)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Magic: {magic}  Task: (Add Historical Trades)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)

    return trades