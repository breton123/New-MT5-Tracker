import json
import os
from scripts.database.fileController import read

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getConfig():
    user_profile = os.environ['USERPROFILE']
    configFile = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'config.json')
    if os.path.exists(configFile):
        config = read(configFile)
        return config
    return {"powName": "", "powAPIKey": "", "symbolSuffix": ""}
