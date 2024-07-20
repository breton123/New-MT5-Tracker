import os

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def resetErrorLog():
    with open(os.path.join(databaseFolder, 'errorlog.txt'), "w+") as file:
        file.write("")