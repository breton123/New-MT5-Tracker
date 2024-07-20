import json
import os

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getConfig():
    user_profile = os.environ['USERPROFILE']
    configFile = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'config.json')
    if os.path.exists(configFile):
        with open(configFile, 'r') as f:
            return json.load(f)
    return {"powName": "", "powAPIKey": "", "symbolSuffix": ""}
