import datetime as datetime
from scripts.database.getDeletedSets import getDeletedSets
from scripts.database.insertSet import insertSet
from scripts.database.log_error import log_error
from scripts.tracker.getDaysLive import getDaysLive
from scripts.tracker.getHistoricalProfit import getHistoricalProfit
from scripts.tracker.getLotSizes import getLotSizes
from scripts.tracker.getProfitFactor import getProfitFactor
from scripts.tracker.getSetName import getSetName
from scripts.tracker.getTradeAmount import getTradeAmount
from scripts.tracker.openMt5 import openMt5
from scripts.tracker.addHistoricalTrades import addHistoricalTrades
from scripts.tracker.getTradeTimes import getTradeTimes
from scripts.tracker.getWinRate import getWinRate

def createSet(magic, accountData):
    openMt5(accountData)
    account = accountData["login"]
    if str(magic) not in getDeletedSets(account):
        try:
            setName = getSetName(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving set name: {e}"
            print(errMsg)
            log_error(errMsg)
            return

        try:
            historicalProfit = round(getHistoricalProfit(magic, accountData), 2)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving historical profit: {e}"
            print(errMsg)
            log_error(errMsg)
            historicalProfit = 0

        try:
            tradeAmount = getTradeAmount(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving trade amount: {e}"
            print(errMsg)
            log_error(errMsg)
            tradeAmount = 0

        try:
            profitFactor = getProfitFactor(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving profit factor: {e}"
            print(errMsg)
            log_error(errMsg)
            profitFactor = 0

        try:
            daysLive = getDaysLive(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving days live: {e}"
            print(errMsg)
            log_error(errMsg)
            daysLive = 0

        try:
            lotSizes = getLotSizes(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving lot sizes: {e}"
            print(errMsg)
            log_error(errMsg)
            lotSizes = {
                "minLotSize": 0,
                "maxLotSize": 0,
                "avgLotSize": 0
            }

        try:
            winRate = getWinRate(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving win rate: {e}"
            print(errMsg)
            log_error(errMsg)
            winRate = {
                "winRate": "0%",
                "wins": 0,
                "losses": 0
            }
            
        try:
            tradeTimes = getTradeTimes(magic, accountData)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error retrieving trade times: {e}"
            print(errMsg)
            log_error(errMsg)
            tradeTimes = {
                "minTradeTime": 0,
                "maxTradeTime": 0,
                "avgTradeTime": 0
            }
            
        setData = {
            "stats": {
                "setName": setName,
                "strategy": "",
                "magic": magic,
                "profit": historicalProfit,
                "trades": tradeAmount,
                "maxDrawdown": "-",
                "avgDrawdown": "-",
                "profitFactor": profitFactor,
                "returnOnDrawdown": "-",
                "minLotSize": lotSizes["minLotSize"],
                "maxLotSize": lotSizes["maxLotSize"],
                "avgLotSize": lotSizes["avgLotSize"],
                "winRate": winRate["winRate"],
                "wins": winRate["wins"],
                "losses": winRate["losses"],
                "minTradeTime": tradeTimes["minTradeTime"],
                "maxTradeTime": tradeTimes["maxTradeTime"],
                "avgTradeTime": tradeTimes["avgTradeTime"],
                "daysLive": daysLive
            },
            "trades": [],
            "drawdown": [],
            "equity": []
        }

        try:
            historicalTrades = addHistoricalTrades(magic, accountData)
            setData["trades"] = historicalTrades
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error adding historical trades: {e}"
            print(errMsg)
            log_error(errMsg)
            setData["trades"] = []

        try:
            insertSet(setData, account)
        except Exception as e:
            errMsg = f"Account: {account}  Magic: {magic}  Task: (Create Set)  Error inserting set into database: {e}"
            print(errMsg)
            log_error(errMsg)
