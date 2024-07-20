import os
from flask import Blueprint, redirect, request, url_for
from scripts.tracker.loadSets import loadSets

uploadSets_bp = Blueprint('uploadSets', __name__)
ALLOWED_EXTENSIONS = {'set'}

@uploadSets_bp.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')
    account = request.form["account"]
    profile = request.form["profile"]
    if profile == "New Profile":
        profileName = request.form["profileName"]
    else:
        profileName = profile
    #makeNew = bool(request.form["new"])
    user_profile = os.environ['USERPROFILE']
    setsFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'Sets')

    if not os.path.exists(setsFolder):
        os.makedirs(setsFolder)
        
    setsAccountFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'Sets', account)

    if not os.path.exists(setsAccountFolder):
        os.makedirs(setsAccountFolder)
        
    setsProfileFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'Sets', account, profileName)

    if not os.path.exists(setsProfileFolder):
        os.makedirs(setsProfileFolder)

    for file in files:
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(setsProfileFolder, file.filename))

    loadSets(account, profileName)
    
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
