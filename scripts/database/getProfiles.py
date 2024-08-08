import os
from scripts.database.log_error import log_error
from scripts.database.getDataPath import getDataPath

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getProfiles(account):
    profiles = []
    for terminal in account["terminalFilePath"]:
        dataPath = getDataPath(terminal)
        print(terminal, dataPath)
        profilesPath = os.path.join(dataPath, "MQL5", "Profiles", "Charts")
        for d in os.listdir(profilesPath):
            if os.path.isdir(os.path.join(profilesPath, d)):
                profiles.append(d)
    return profiles