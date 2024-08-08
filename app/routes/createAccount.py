from flask import Blueprint, redirect, render_template, request, url_for
from scripts.database.createAccount import createAccount

createAccount_bp = Blueprint('create_account', __name__)

@createAccount_bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        if request.form['type'] == "master":
            status = "initializing"
        elif request.form['type'] == "slave":
            status = "waiting for master"
        else:
            status = "error"
        account_data = {
            'terminalFilePath': request.form.getlist('terminalFilePath'),
            'status': "initializing"
        }
        for key, val in request.form.items():
            if key == "terminalFilePath":
                pass
            else:
                account_data[key] = val
        print(account_data)
        createAccount(account_data)
        return redirect(url_for('index.index'))
    return render_template('createAccount.html')