import os
from flask import Blueprint, json, redirect, render_template, request, url_for

config_bp = Blueprint('config', __name__)
user_profile = os.environ['USERPROFILE']
configFile = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase', 'config.json')

@config_bp.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        powName = request.form['powName']
        powAPIKey = request.form['powAPIKey']
        symbolSuffix = request.form['symbolSuffix']
        config = {"powName": powName, "powAPIKey": powAPIKey,  "symbolSuffix": symbolSuffix}
        save_config(config)
        return redirect(url_for('config.config'))

    config = load_config()
    return render_template('config.html', config=config)

def save_config(config):
    with open(configFile, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(configFile):
        with open(configFile, 'r') as f:
            return json.load(f)
    return {"powName": "", "powAPIKey": "", "symbolSuffix": ""}