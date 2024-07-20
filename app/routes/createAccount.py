from flask import Blueprint, redirect, render_template, request, url_for
from scripts.database.createAccount import createAccount

createAccount_bp = Blueprint('createAccount', __name__)

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
            'name': request.form['name'],
            'login': request.form['login'],
            'password': request.form['password'],
            'server': request.form['server'],
            'deposit': request.form['deposit'],
            'dataPath': request.form['dataPath'],
            'terminalFilePath': request.form['terminalFilePath'],
            'type': request.form['type'],
            'status': "initializing"
        }
        createAccount(account_data)
        return redirect(url_for('index'))
    return render_template('createAccount.html')