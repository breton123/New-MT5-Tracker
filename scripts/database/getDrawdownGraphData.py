from datetime import datetime
import os
from scripts.database.log_error import log_error
from scripts.database.getFrontendSets import getFrontendSets

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def getDrawdownGraphData(account, timeframe):
    try:
        if timeframe == "10s":
            timeframe = 1
        elif timeframe == "30s":
            timeframe = 3
        elif timeframe == "1m":
            timeframe = 6
        elif timeframe == "5m":
            timeframe = 30
        elif timeframe == "10m":
            timeframe = 60
        elif timeframe == "15m":
            timeframe = 90
        elif timeframe == "30m":
            timeframe = 180
        elif timeframe == "45m":
            timeframe = 270
        elif timeframe == "1h":
            timeframe = 360
        elif timeframe == "2h":
            timeframe = 720
        elif timeframe == "4h":
            timeframe = 1440
        elif timeframe == "1D":
            timeframe = 8640

        allSets = getFrontendSets(account)
        data = []

        for set_data in allSets:
            name = set_data["stats"]["setName"]
            new_trace = {"x": [], "y": [], "mode": "lines", "name": name}
            counter = 0
            biggest = 0
            biggestTime = 0
            for item in set_data["drawdown"]:
                if counter < timeframe:
                    if item["drawdown"] < biggest:
                        biggest = item["drawdown"]
                        datetime_obj = datetime.fromtimestamp(item["time"])
                        formatted_date_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                        biggestTime = formatted_date_time
                    counter += 1
                else:
                    if biggestTime != 0:
                        datetime_obj = datetime.fromtimestamp(item["time"])
                        formatted_date_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                        new_trace["x"].append(formatted_date_time)
                        new_trace["y"].append(biggest)
                        counter = 0
                        biggest = 0
                        biggestTime = 0
            if biggest != 0:
                new_trace["x"].append(biggestTime)
                new_trace["y"].append(biggest)

            data.append(new_trace)

        return data

    except KeyError as e:
        errMsg = f"Account: {account}  Task: (Get Drawdown Graph Data)  KeyError: {e} - Required key not found in set data"
        print(errMsg)
        log_error(errMsg)
        return None
    except Exception as e:
        errMsg = f"Account: {account} Task: (Get Drawdown Graph Data)   Error in getDrawdownGraphData for account '{account}': {e}"
        print(errMsg)
        log_error(errMsg)
        return None
