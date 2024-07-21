from flask import Blueprint, jsonify, redirect, request, url_for
from scripts.database.deleteSetFiles import deleteSetFiles
from scripts.database.getAccounts import getAccounts
from scripts.tracker.deleteSet import deleteSet

deleteSet_bp = Blueprint('deleteSet', __name__)

@deleteSet_bp.route('/delete-set', methods=['POST'])
def delete_set():
    data = request.json
    accountID = data.get('account')
    print(accountID)
    magic_numbers = data.get('magicNumbers')
    print(magic_numbers)
    for account in getAccounts():
        if account["login"] == accountID:
            for magic in magic_numbers:
                deleteSet(magic, account)
                deleteSetFiles(account, magic_numbers)


    
