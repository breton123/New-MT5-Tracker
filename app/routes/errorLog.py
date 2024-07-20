from flask import Blueprint, render_template
from scripts.database.getErrorLog import getErrorLog

errorLog_bp = Blueprint('errorLog', __name__)

@errorLog_bp.route('/error_log')
def error_log():
    return render_template('error_log.html', errors=getErrorLog())