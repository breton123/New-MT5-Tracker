import os
from scripts.database.getDataPath import getDataPath
from scripts.tracker.parse_chr_file import parse_chr_file

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getProfileSets(account, profile):
    dataPath = getDataPath(account)
    profilePath = os.path.join(dataPath, "MQL5", "Profiles", "Charts", profile)
    profileSets = []
    try:
        for chartFile in os.listdir(profilePath):
            chartPath = os.path.join(dataPath, "MQL5", "Profiles", "Charts", profile, chartFile)
            try:
                chartConfig = parse_chr_file(chartPath)
                chartData = {
                    "setName": chartConfig["chart"]["expert"]["inputs"]["StrategyDescription"],
                    "symbol": chartConfig["chart"]["symbol"],
                    "magic": chartConfig["chart"]["expert"]["inputs"]["MAGIC_NUMBER"]
                }
                profileSets.append(chartData)
            except:
                pass
    except Exception as e:
        print(f"Failed to get profile sets {e}")
        
    return profileSets