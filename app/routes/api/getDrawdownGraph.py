import csv
import io
from flask import Blueprint, jsonify, make_response, redirect, request, url_for
from scripts.database.getAccounts import getAccounts
from scripts.database.getDrawdownGraphData import getDrawdownGraphData
from scripts.database.getSet import getSet
from scripts.tracker.getAllMagics import getAllMagics

getDrawdownGraph_bp = Blueprint('getDrawdownGraph', __name__)

@getDrawdownGraph_bp.route('/api/getDrawdownGraph/<account_id>/<timeframe>', methods=['GET'])
def getDrawdownGraph(account_id, timeframe):
     return jsonify(getDrawdownGraphData(account_id, timeframe))



