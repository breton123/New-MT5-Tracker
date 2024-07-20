from flask import Blueprint, jsonify
from scripts.database.getProfileSets import getProfileSets

getProfileSets_bp = Blueprint('getProfileSets', __name__)

@getProfileSets_bp.route('/api/getProfileSets/<account_id>/<profile_id>', methods=['GET'])
def getProfileSetsAPI(account_id, profile_id):
    profile_id = profile_id.replace("%20", " ")
    if profile_id != "New Profile":
        profiles = getProfileSets(account_id, profile_id)
    else:
        profiles = []
    return jsonify(profiles)