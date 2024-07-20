from flask import Blueprint, render_template
from scripts.database.getAccounts import getAccounts
from scripts import runTracker

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    runTracker.run()
    return render_template('index.html', accounts=getAccounts())