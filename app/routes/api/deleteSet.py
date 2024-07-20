from flask import Blueprint, jsonify, request

deleteSet_bp = Blueprint('deleteSet', __name__)

@deleteSet_bp.route('/delete-set', methods=['POST'])
def delete_set():
    data = request.json
    account = data.get('account')
    magic_numbers = data.get('magicNumbers')
    # Process the magic numbers and copy them to the selected account
    # Your logic here

    return jsonify(success=True, message="Magic numbers copied successfully")
