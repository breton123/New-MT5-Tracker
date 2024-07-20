import os


def doesProfileExist(dataPath, profileName):
    try:
        profilePath = os.path.join(dataPath, 'MQL5', 'Profiles', 'Charts', profileName)
        amountOfCharts = len([f for f in os.listdir(profilePath) if os.path.isfile(os.path.join(profilePath, f))])
        return amountOfCharts
    except:
        return False