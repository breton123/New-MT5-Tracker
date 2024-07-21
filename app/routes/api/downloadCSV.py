import csv
import io
from flask import Blueprint, jsonify, make_response, redirect, request, url_for
from scripts.database.getAccounts import getAccounts
from scripts.database.getSet import getSet
from scripts.tracker.getAllMagics import getAllMagics

downloadCSV_bp = Blueprint('downloadCSV', __name__)

@downloadCSV_bp.route('/downloadCSV', methods=['POST'])
def downloadCSV():
     data = request.json
     accountID = data.get('account')
     magic_numbers = data.get('magicNumbers')
     output = io.StringIO()
     data = []
     for account in getAccounts():
          if account["login"] == accountID:
               if len(magic_numbers) == 0:
                    magic_numbers = getAllMagics(account)
               for magic in magic_numbers:
                    try:
                         data.append(getSet(str(magic),account)["stats"])
                    except:
                         pass

     csv_writer = csv.DictWriter(output, fieldnames=data[0].keys())
     csv_writer.writeheader()
     csv_writer.writerows(data)
     output.seek(0)

     response = make_response(output.getvalue())
     response.headers["Content-Disposition"] = "attachment; filename=data.csv"
     response.headers["Content-Type"] = "text/csv"
     return response


    
