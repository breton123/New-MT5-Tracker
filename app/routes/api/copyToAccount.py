from flask import Blueprint, jsonify, request

copyToAccount_bp = Blueprint('copyToAccount', __name__)

@copyToAccount_bp.route('/copy-to-account', methods=['POST'])
def copy_to_account():
    data = request.json
    masterAccountID = data.get("masterAccount")
    account = data.get('account')
    magic_numbers = data.get('magicNumbers')
    loader.addCopier(masterAccountID, account, magic_numbers)
    # Process the magic numbers and copy them to the selected account
    # Your logic here

    return jsonify(success=True, message="Magic numbers copied successfully")
