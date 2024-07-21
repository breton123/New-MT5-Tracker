import os
import shutil

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')

def deleteSetFiles(account, magics):
     account = account["login"]
     deletedFolder = os.path.join(databaseFolder, "deletedSets")
     deletedSetsFolder = os.path.join(databaseFolder, "deletedSets", account)
     
     if not os.path.exists(deletedFolder):
          os.makedirs(deletedFolder)
     if not os.path.exists(deletedSetsFolder):
          os.makedirs(deletedSetsFolder)

     for magic in magics:
          try:
               magicPath = os.path.join(databaseFolder, account, f"{magic}.json")
               newPath = os.path.join(deletedSetsFolder, f"{magic}.json")
               shutil.move(magicPath, newPath)
          except:
               print("Failed to delete set file")
