from flask import Blueprint, render_template
from scripts.database.getAccounts import getAccounts
from scripts.database.getDrawdownGraphData import getDrawdownGraphData
from scripts.database.getEquityGraphData import getEquityGraphData
from scripts.database.getFilterData import getFilterData
from scripts.database.getFrontendSets import getFrontendSets

account_bp = Blueprint('account', __name__)

@account_bp.route('/<account_id>')
def account(account_id):
    sets = getFrontendSets(account_id)
    slaveAccounts = []
    accounts = getAccounts()
    accountProfit = 0
    accountMaxDrawdown = 0
    accountAverageDrawdown = 0
    testSets = len(sets)
    daysLive = 0
    for set in sets:
        accountProfit += set["stats"]["profit"]
        try:
            accountMaxDrawdown += set["stats"]["maxDrawdown"]
            accountAverageDrawdown+= set["stats"]["avgDrawdown"]
        except:
            pass
        if set["stats"]["daysLive"] > daysLive:
            daysLive = set["stats"]["daysLive"]
    for account in accounts:
        if account["type"] == "slave":
            slaveAccounts.append(account["login"])
    if len(sets) != 0:
        return render_template('account.html', account_id = {"account_id": account_id}, sets=sets, drawdownData = getDrawdownGraphData(account_id, "15m"), equityData = getDrawdownGraphData(account_id, "1h"), filterData = getFilterData(account_id), accounts=slaveAccounts, accountProfit=round(accountProfit,2), accountDrawdown=round(accountMaxDrawdown,2), testSets=testSets, accountAverageDrawdown=round(accountAverageDrawdown, 2))
    else:
        return render_template('empty_account.html')