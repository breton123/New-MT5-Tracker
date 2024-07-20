import MetaTrader5 as mt5
import datetime as datetime

def openMt5(accountData):
     if not mt5.initialize(accountData["terminalFilePath"], login=int(accountData["login"]), password=accountData["password"], server=accountData["server"]):
          print("initialize() failed, error code =",mt5.last_error())
          quit()