from datetime import datetime
import os
from scripts.database.log_error import log_error
from scripts.database.getFrontendSets import getFrontendSets

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getEquityGraphData(account):
    try:
        allSets = getFrontendSets(account)
        data = []
        
        for set_data in allSets:
            name = set_data["stats"]["setName"]
            new_trace = {"x": [], "y": [], "mode": "lines", "name": name}
            
            for item in set_data["equity"]:
                datetime_obj = datetime.fromtimestamp(item["time"])
                formatted_date_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                new_trace["x"].append(formatted_date_time)
                new_trace["y"].append(item["equity"])
            
            data.append(new_trace)
        
        return data
    
    except KeyError as e:
        errMsg = f"Account: {account}  Task: (Get Equity Graph Data)  KeyError: {e} - Required key not found in set data"
        print(errMsg)
        log_error(errMsg)
        return None
    
    except Exception as e:
        errMsg = f"Account: {account}  Task: (Get Equity Graph Data)  Unexpected error: {e}"
        print(errMsg)
        log_error(errMsg)
        return None
