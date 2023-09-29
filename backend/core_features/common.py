from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields, reqparse
from allClasses import *
import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
from datetime import datetime, date, time
import logging
app.logger.setLevel(logging.DEBUG)

api = Namespace('common', description='Course related operations')

sort_records = api.parser()
sort_records.add_argument("sort_column", help="Enter sort column")
sort_records.add_argument("sort_direction", help="Enter sort direction")
sort_records.add_argument("records", help="Enter records")
@api.route("/sort_records", methods=["POST"])
@api.doc(description="Sort Records")
class sortRecords(Resource):
    @api.expect(sort_records)
    def post(self):
      args = sort_records.parse_args()
      sort_column = args.get("sort_column", "")
      sort_direction = args.get("sort_direction", "")
      records = request.json.get("records", [])

      records_with_values = [record for record in records if record.get(sort_column) is not None]
      records_with_none_values = [record for record in records if record.get(sort_column) is None]

      if sort_column != "":
          sorted_data = sorted(records_with_values, key=lambda x: x[sort_column], reverse=(sort_direction == "desc"))
      else:
          sorted_data = records

      sorted_data = records_with_none_values + sorted_data

      return jsonify({"code": 200, "data": sorted_data, "sort": sort_column, "direction": sort_direction})
    

def format_date_time(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, time):
        return value.strftime('%H:%M:%S')
    else:
        return None
    
    
def getUserRole(user_ID=None):
    if user_ID is None:
        user_ID = getUserID()

    if user_ID:
        return User.query.filter_by(user_ID=user_ID).first().role_Name
    else:
        return None
    
def getUserID():
    user_ID = session.get('user_ID')
    print(user_ID)
    if user_ID:
        id = User.query.filter_by(user_ID=user_ID).first().user_ID
        db.session.close()
        return id
    else:
        return 'Session not set'