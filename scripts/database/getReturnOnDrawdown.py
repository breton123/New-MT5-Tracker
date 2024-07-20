import os

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def getReturnOnDrawdown(magic, drawdown, account, profit):
    try:
        returnOnDrawdown = round(profit / abs(float(drawdown)), 2)
    except:
            returnOnDrawdown = "-"
    return returnOnDrawdown

