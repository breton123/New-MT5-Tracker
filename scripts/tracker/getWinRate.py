import MetaTrader5 as mt5
import datetime as datetime
from datetime import datetime
from scripts.database.log_error import log_error
from scripts.tracker.openMt5 import openMt5
from scripts.tracker.getTradeAmount import getTradeAmount

def getWinRate(magic, account):
    openMt5(account)
    accountData = account
    account = account["login"]
    wins = 0
    losses = 0
    trades = getTradeAmount(magic, accountData)
    try:
        orders = mt5.history_deals_get(0, datetime.now())
        for order in orders:
            order = order._asdict()
            if order["magic"] == magic:
                if order["reason"] == 4:
                    if order["profit"] >= 0:
                        wins += 1
                    elif order["profit"] < 0:
                        losses += 1          
    
    except Exception as e:
        errMsg = f"Task: (Get Win Rate - History Deals)  Error retrieving historical deals: {e}"
        print(errMsg)
        log_error(errMsg)
        return {
            "winRate": "0%",
            "wins": 0,
            "losses": 0
        }
        
    try:
        return {
                "winRate": str(round((wins / trades)*100, 0)).replace(".0", "") + "%",
                "wins": wins,
                "losses": losses
            }
    except ZeroDivisionError as e:
        return {
                "winRate": "0%",
                "wins": wins,
                "losses": losses
            }