import os
import chardet
from scripts.database.getTerminalFolder import getTerminalFolder
from scripts.database.log_error import log_error

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')
terminalsFolder = os.path.join(user_profile, 'AppData', 'Roaming', 'MetaQuotes', 'Terminal')

def getDataPath(account_id):
    terminalFolder = getTerminalFolder(account_id).replace("\\terminal64.exe", "")
    for folder in os.listdir(terminalsFolder):
        try:
            terminalFolderFilePath = os.path.join(terminalsFolder, folder, "origin.txt")
            with open(terminalFolderFilePath, "r", encoding=detect_encoding(terminalFolderFilePath)) as file:
                if terminalFolder == file.read():
                    dataPath = os.path.join(terminalsFolder, folder)
                    return dataPath
        except:
            pass
    return ""

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']