
import os
from pathlib import Path

from scripts.database.getAccounts import getAccounts
from scripts.database.getConfig import getConfig
from scripts.database.getDataPath import getDataPath
from scripts.tracker.getPreviousProfile import getPreviousProfile
from scripts.tracker.parseCopierFile import parseCopierFile
from scripts.tracker.read_ini_file import read_ini_file
from scripts.tracker.terminalController import closeTerminal
from scripts.tracker.writeCopierFile import writeCopierFile


def addCopier(masterAccountID, slaveAccountID, magicNumbers):
    user_profile = os.environ['USERPROFILE']
    databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')
    config = getConfig()
    
    masterTerminalPath = ""
    slaveTerminalPath = ""
    
    accounts = getAccounts()
    for account in accounts:
        if account["login"] == masterAccountID:
            masterTerminalPath = account["terminalFilePath"]
        if account["login"] == slaveAccountID:
            slaveTerminalPath = account["terminalFilePath"]
    

    masterTerminalConfigPath = os.path.join(getDataPath(masterAccountID), "config", "common.ini")
    slaveTerminalConfigPath = os.path.join(getDataPath(slaveAccountID), "config", "common.ini")
    masterProfileName = getPreviousProfile(masterTerminalConfigPath)
    slaveProfileName = getPreviousProfile(slaveTerminalConfigPath)

    directory = os.getcwd()
    
    masterDataPath = getDataPath(masterAccountID)
    slaveDataPath = getDataPath(slaveAccountID)

    
    masterChartPath = f"{directory}\\tradeSender.chr"
    slaveChartPath = f"{directory}\\tradeReceiver.chr"


    masterConfig = parseCopierFile(masterChartPath)
    print(masterConfig)
    masterConfig["chart"]["symbol"] = "XAUUSD" + config["symbolSuffix"]
    masterConfig["chart"]["symbol"] = "XAUUSD" + config["symbolSuffix"]
    masterConfig["chart"]["expert"]["inputs"]["Channel"] = f"{masterAccountID}-{slaveAccountID}"
    masterConfig["chart"]["expert"]["inputs"]["IncludeMagicNumbers"] = str(magicNumbers).replace("[","").replace("]","")
    masterConfig["chart"]["description"] = "Trade Sender"
    masterConfig["chart"]["expert"]["name"] = "Trade Sender"
    

    slaveConfig = parseCopierFile(slaveChartPath)
    slaveConfig["chart"]["symbol"] = "XAUUSD" + config["symbolSuffix"]
    slaveConfig["chart"]["expert"]["inputs"]["Channel"] = f"{masterAccountID}-{slaveAccountID}"
    slaveConfig["chart"]["description"] = "Trade Receiver"
    slaveConfig["chart"]["expert"]["name"] = "Trade Receiver"

    masterProfilePath = os.path.join(masterDataPath, "MQL5", "Profiles", "Charts", masterProfileName)
    Path(masterProfilePath).mkdir(parents=True, exist_ok=True)
    masterChartNumber = len([f for f in os.listdir(masterProfilePath) if os.path.isfile(os.path.join(masterProfilePath, f))]) + 1
    masterChrFilePath = os.path.join(masterProfilePath, f"chart0{masterChartNumber}.chr")
    writeCopierFile(masterChrFilePath, masterConfig)
    writeCopierFile("testMaster.chr", masterConfig)

    slaveProfilePath = os.path.join(slaveDataPath, "MQL5", "Profiles", "Charts", slaveProfileName)
    Path(slaveProfilePath).mkdir(parents=True, exist_ok=True)
    slaveChartNumber = len([f for f in os.listdir(slaveProfilePath) if os.path.isfile(os.path.join(slaveProfilePath, f))]) + 1
    slaveChrFilePath = os.path.join(slaveProfilePath, f"chart0{slaveChartNumber}.chr")
    writeCopierFile(slaveChrFilePath, slaveConfig)
    writeCopierFile("testSlave.chr", slaveConfig)
    
    masterTerminalConfigPath = os.path.join(getDataPath(masterAccountID), "config", "common.ini")
    closeTerminal(masterTerminalPath)
    masterTerminalConfig = read_ini_file(masterTerminalConfigPath)
    masterTerminalConfig["Charts"]["ProfileLast"] = masterProfileName
    masterTerminalConfig["Experts"]["enabled"] = "1"
    masterTerminalConfig["Experts"]["allowdllimport"] = "1"
    with open(masterTerminalConfigPath, 'w') as configfile:
        masterTerminalConfig.write(configfile)
        
    slaveTerminalConfigPath = os.path.join(getDataPath(slaveAccountID), "config", "common.ini")
    closeTerminal(slaveTerminalPath)
    slaveTerminalConfig = read_ini_file(slaveTerminalConfigPath)
    slaveTerminalConfig["Charts"]["ProfileLast"] = slaveProfileName
    slaveTerminalConfig["Experts"]["enabled"] = "1"
    slaveTerminalConfig["Experts"]["allowdllimport"] = "1"
    with open(slaveTerminalConfigPath, 'w') as configfile:
        slaveTerminalConfig.write(configfile)
