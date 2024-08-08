from flask import Blueprint, render_template
from scripts.database.getAccounts import getAccounts
from scripts.database.getProfiles import getProfiles

setLoader_bp = Blueprint('setLoader', __name__)

@setLoader_bp.route('/set_loader')
def set_loader():
    accounts = getAccounts()
    accountIDs = []
    profiles = {}
    for account in accounts:
        accountIDs.append(account["login"])
        profiles[account["login"]] = getProfiles(account)
    return render_template('uploadSets.html', sets=[], accounts=accountIDs, profiles=profiles)
