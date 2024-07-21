import datetime as datetime
import os
from scripts.database.log_error import log_error
from scripts.database.getDataPath import getDataPath
from scripts.tracker.findChartPath import findChartPath
from scripts.tracker.getDaysLive import getDaysLive
from scripts.tracker.getHistoricalProfit import getHistoricalProfit
from scripts.tracker.getLotSizes import getLotSizes
from scripts.tracker.getPreviousProfile import getPreviousProfile
from scripts.tracker.getProfitFactor import getProfitFactor
from scripts.tracker.getSetName import getSetName
from scripts.tracker.getTradeAmount import getTradeAmount
from scripts.tracker.openMt5 import openMt5
from scripts.tracker.addHistoricalTrades import addHistoricalTrades
from scripts.tracker.getTradeTimes import getTradeTimes
from scripts.tracker.getWinRate import getWinRate
from scripts.tracker.parseCopierFile import parseCopierFile
from scripts.tracker.read_ini_file import read_ini_file
from scripts.tracker.terminalController import closeTerminal

def deleteSet(magic, accountData):
     openMt5(accountData)
     try:
          account = accountData["login"]
          terminalPath = accountData["terminalFilePath"]
          configPath = os.path.join(getDataPath(account), "config", "common.ini")
          profile = getPreviousProfile(configPath)
          profilePath = os.path.join(getDataPath(account), "MQL5", "Profiles", "Charts", profile)
          chartFiles = findChartPath(profilePath, magic)
          try:
               for path in chartFiles:
                    os.remove(path)
               closeTerminal(terminalPath)
               print(f"Deleted set {magic}")
          except:
               print(f"Could not find chart or {magic} in the current profile. Maybe the profile has not been saved?")
     except Exception as e:
          err = f"Failed to delete set Error: {e}"
          print(err)
          log_error(err)
     