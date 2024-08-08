
import os
import random
from scripts.database.getAccounts import getAccounts
from scripts.database.getConfig import getConfig
from scripts.database.getDataPath import getDataPath
from scripts.database.getSets import getSets
from scripts.database.insertSet import insertSet
from scripts.tracker.parseSetFile import parseSetFile
from scripts.tracker.parse_chr_file import parse_chr_file
from scripts.tracker.terminalController import closeTerminal
from scripts.tracker.update_ini_file import update_ini_file
from scripts.tracker.write_chr_file import write_chr_file


def loadSets(account_id, profileName):
    user_profile = os.environ['USERPROFILE']
    databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')
    setsFolder = os.path.join(databaseFolder, "Sets", str(account_id), profileName)
    config = getConfig()
    terminalPath = ""
    terminalIndex = 0
    accounts = getAccounts()
    for account in accounts:
        if account["login"] == account_id:
            terminals = account["terminalFilePath"]

    directory = os.getcwd()

    powName = config["powName"]
    defaultChartPath = f"{directory}\\scripts\\tracker\\packages\\chart01.chr"
    chartNumber = 1

    terminalPath = terminals[terminalIndex]
    dataPath = getDataPath(terminalPath)
    chartsPath = os.path.join(dataPath, 'MQL5', 'Profiles', 'Charts', profileName)

    if os.path.isdir(chartsPath):
        chartNumber = len([f for f in os.listdir(chartsPath) if os.path.isfile(os.path.join(chartsPath, f))])
    else:
        os.makedirs(chartsPath)
        chartNumber = 1

    currentSets = getSets(account_id)
    currentMagics = []
    for set in currentSets:
        try:
            currentMagics.append(set["magic"])
        except:
            pass

    for setFile in os.listdir(setsFolder):
        if chartNumber > 90:
            terminalIndex += 1
            try:
                terminalPath = terminals[terminalIndex]
                dataPath = getDataPath(terminalPath)
                chartsPath = os.path.join(dataPath, 'MQL5', 'Profiles', 'Charts', profileName)

                if os.path.isdir(chartsPath):
                    chartNumber = len([f for f in os.listdir(chartsPath) if os.path.isfile(os.path.join(chartsPath, f))])
                else:
                    os.makedirs(chartsPath)
                    chartNumber = 1
            except:
                pass

        defaultConfig = parse_chr_file(defaultChartPath)
        magicNumber = setFile.split("_")[-1].replace(".set","")
        symbol = setFile.split(" ")[0] + config["symbolSuffix"]

        if magicNumber not in currentMagics:
            newSet = {
                "stats": {
                    "setName": setFile.replace(".set",""),
                    "strategy": "",
                    "magic": magicNumber,
                    "profit": 0,
                    "trades": 0,
                    "maxDrawdown": "-",
                    "profitFactor": 0,
                    "returnOnDrawdown": "-",
                    "daysLive": 0
                },
                "trades": [],
                "drawdown": [],
                "equity": []
            }
            insertSet(newSet, account_id)

        setConfig = parseSetFile(f"{setsFolder}\\{setFile}")
        defaultConfig["chart"]["description"] = setFile.replace(".set","")
        defaultConfig["chart"]["expert"]["inputs"] = setConfig
        defaultConfig["chart"]["id"] = random.randint(100000000000000000, 999999999999999999)
        defaultConfig["chart"]["symbol"] = symbol
        defaultConfig["chart"]["expert"]["inputs"]["apiKey"] = config["powAPIKey"]
        defaultConfig["chart"]["expert"]["inputs"]["MAGIC_NUMBER"] = str(magicNumber)
        defaultConfig["chart"]["expert"]["inputs"]["StrategyDescription"] = setFile.replace(".set","")
        defaultConfig["chart"]["expert"]["inputs"]["TradeComment"] = setFile.replace(".set","")
        defaultConfig["chart"]["expert"]["name"] = config["powName"].replace(".ex5","")
        defaultConfig["chart"]["expert"]["path"] = f"Experts\\{powName}"
        defaultConfig["chart"]["expert"]["expertmode"] = 1

        output_chr_file_path = f'{dataPath}\\MQL5\\Profiles\\Charts\\{profileName}\\chart0{chartNumber}.chr'
        write_chr_file(output_chr_file_path, defaultConfig)
        chartNumber += 1

    terminalConfigPath = os.path.join(getDataPath(terminalPath), "config", "common.ini")
    closeTerminal(terminalPath)
    update_ini_file(terminalConfigPath, profileName)
