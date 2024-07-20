import MetaTrader5 as mt5
import datetime as datetime

def getAccount():
     account_info=mt5.account_info()
     number = account_info[0]
     return number