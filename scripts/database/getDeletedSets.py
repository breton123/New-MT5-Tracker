import os

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')
deletedFolder = os.path.join(databaseFolder, "deletedSets")

def getDeletedSets(account):
     try:
          deletedSetsFolder = os.path.join(deletedFolder,account)
          magics = []
          for file in os.listdir(deletedSetsFolder):
               magics.append(file.replace(".json", ""))
          return magics
     except:
          return []
