import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.getSet import getSet
from scripts.database.insertTrade import insertTrade
from scripts.database.isTradeExists import isTradeExists
from scripts.database.log_error import log_error
from scripts.database.updateProfit import updateProfit
from scripts.database.updateProfitFactor import updateProfitFactor
from scripts.tracker.getHistoricalProfit import getHistoricalProfit
from scripts.tracker.openMt5 import openMt5

tickets = []

def updateHistoricalTrades(account):
    global tickets
    openMt5(account)
    accountData = account
    account = account["login"]
    
    try:
        orders = mt5.history_deals_get(0, datetime.now())
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Update Historical Trades)  Error getting historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return
    
    for order in orders:
        try:
            orderMagic = order[6]
            if order[8] == 4:
                order_id = order[0]
                if order_id not in tickets:
                    if str(orderMagic) not in getDeletedSets(account):
                        try:
                            currentSet = getSet(orderMagic, accountData)
                        except Exception as e:
                            errMsg = f"Account: {account}  Magic: {orderMagic}  Task: (Update Historical Trades)  Error getting current set: {e}"
                            print(errMsg)
                            log_error(errMsg)
                            continue
                        
                        try:
                            currentTrades = currentSet["trades"]
                        except KeyError as e:
                            errMsg = f"Account: {account}  Magic: {orderMagic}  Task: (Update Historical Trades)  KeyError: {e} - 'trades' key not found in current set"
                            print(errMsg)
                            log_error(errMsg)
                            continue
                        
                        try:
                            if not isTradeExists(currentTrades, order_id):
                                orderTime = order[2]
                                volume = order[9]
                                price = order[10]
                                profit = round(order[13], 2)
                                symbol = order[15]
                                newTrade = {
                                    "id": order_id,
                                    "time": orderTime,
                                    "volume": volume,
                                    "price": price,
                                    "profit": profit,
                                    "symbol": symbol
                                }
                                insertTrade(orderMagic, newTrade, account)
                                updateProfitFactor(orderMagic, accountData)
                                updateProfit(orderMagic, getHistoricalProfit(orderMagic, accountData), account)
                                tickets.append(order_id)
                                print(f"New historical trade for {orderMagic}")
                            else:
                                tickets.append(order_id)
                        except Exception as e:
                            errMsg = f"Account: {account}  Magic: {orderMagic}  Task: (Update Historical Trades)  Error processing trade: {e}"
                            print(errMsg)
                            log_error(errMsg)
        except KeyError as e:
            errMsg = f"Account: {account}  Task: (Update Historical Trades)  KeyError: {e} - Error accessing order details"
            print(errMsg)
            log_error(errMsg)
        except Exception as e:
            errMsg = f"Account: {account}  Task: (Update Historical Trades)  Unexpected error: {e}"
            print(errMsg)
            log_error(errMsg)