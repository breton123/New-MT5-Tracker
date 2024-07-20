import os
from scripts.database.log_error import log_error
from scripts.database.getFrontendSets import getFrontendSets

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

 
def getFilterData(account):
    try:
        allSets = getFrontendSets(account)
        
        # Initialize data with large initial values for min and small for max
        data = {
            "minProfit": float('inf'),
            "maxProfit": 0,
            "minTrades": float('inf'),
            "maxTrades": 0,
            "minDrawdown": float('inf'),
            "maxDrawdown": 0,
            "minProfitFactor": float('inf'),
            "maxProfitFactor": 0,
            "minReturnOnDrawdown": float('inf'),
            "maxReturnOnDrawdown": 0,
            "minDaysLive": float('inf'),
            "maxDaysLive": 0,
            "minAvgDrawdown": float('inf'),
            "maxAvgDrawdown": 0,
            "minWinRate": float('inf'),
            "maxWinRate": 0
            
        }
        
        for set_data in allSets:
            profit = set_data["stats"]["profit"]
            trades = set_data["stats"]["trades"]
            maxDrawdown = set_data["stats"]["maxDrawdown"]
            profitFactor = set_data["stats"]["profitFactor"]
            returnOnDrawdown = set_data["stats"]["returnOnDrawdown"]
            daysLive = set_data["stats"]["daysLive"]
            avgDrawdown = set_data["stats"]["avgDrawdown"]
            winRate = set_data["stats"]["winRate"]
            
            try:
                winRate = int(winRate.replace("%",""))
            except:
                winRate = 0
            
            if winRate == "":
                winRate = 0
            
            # Handle cases where maxDrawdown, returnOnDrawdown, or daysLive may be "-"
            if maxDrawdown == "-":
                maxDrawdown = 0
            if avgDrawdown == "-":
                avgDrawdown = 0
            if returnOnDrawdown == "-":
                returnOnDrawdown = 0
            if not daysLive:
                daysLive = 0
            
            # Update minimum and maximum values
            try:
                data["minProfit"] = min(data["minProfit"], profit)
                try:
                    if float(data["minProfit"]) < 0:
                        data["minProfit"] = 0
                except:
                    data["minProfit"] = 0
                data["maxProfit"] = max(data["maxProfit"], profit)
                data["minTrades"] = min(data["minTrades"], trades)
                data["maxTrades"] = max(data["maxTrades"], trades)
                data["minDrawdown"] = min(data["minDrawdown"], maxDrawdown)
                data["maxDrawdown"] = max(data["maxDrawdown"], maxDrawdown)
                data["minProfitFactor"] = min(data["minProfitFactor"], profitFactor)
                data["maxProfitFactor"] = max(data["maxProfitFactor"], profitFactor)
                data["minReturnOnDrawdown"] = min(data["minReturnOnDrawdown"], returnOnDrawdown)
                data["maxReturnOnDrawdown"] = max(data["maxReturnOnDrawdown"], returnOnDrawdown)
                data["minDaysLive"] = min(data["minDaysLive"], daysLive)
                data["maxDaysLive"] = max(data["maxDaysLive"], daysLive)
                data["minAvgDrawdown"] = min(data["minAvgDrawdown"], avgDrawdown)
                data["maxAvgDrawdown"] = max(data["maxAvgDrawdown"], avgDrawdown)
                data["minWinRate"] = min(data["minWinRate"], winRate)
                data["maxWinRate"] = max(data["maxWinRate"], winRate)
            except:
                data["minProfit"] = 0
                data["maxProfit"] = 0
                data["minTrades"] = 0
                data["maxTrades"] = 0
                data["minDrawdown"] = 0
                data["maxDrawdown"] = 0
                data["minProfitFactor"] = 0
                data["maxProfitFactor"] = 0
                data["minReturnOnDrawdown"] = 0
                data["maxReturnOnDrawdown"] = 0
                data["minDaysLive"] = 0
                data["maxDaysLive"] = 0
                data["minAvgDrawdown"] = 0
                data["maxAvgDrawdown"] = 0
                data["minWinRate"] = 0
                data["maxWinRate"] = 0
        return data
    
    except Exception as e:
        errMsg = f"Error in getFilterData for account '{account}': {e}"
        print(errMsg)
        log_error(errMsg)
        data = {}
        data["minProfit"] = 0
        data["maxProfit"] = 0
        data["minTrades"] = 0
        data["maxTrades"] = 0
        data["minDrawdown"] = 0
        data["maxDrawdown"] = 0
        data["minProfitFactor"] = 0
        data["maxProfitFactor"] = 0
        data["minReturnOnDrawdown"] = 0
        data["maxReturnOnDrawdown"] = 0
        data["minDaysLive"] = 0
        data["maxDaysLive"] = 0
        data["minAvgDrawdown"] = 0
        data["maxAvgDrawdown"] = 0
        data["minWinRate"] = 0
        data["maxWinRate"] = 0
        return data
