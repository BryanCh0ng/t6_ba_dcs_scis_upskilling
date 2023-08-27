from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('registration', description='Registration related operations')

retrieve_reg_count = api.parser()
retrieve_reg_count.add_argument("course_id", help="Enter course id")
@api.route("/retrieve_reg_count")
@api.doc(description="Get Course Reg Count")
class RetrieveRegCount(Resource):
  @api.expect(retrieve_reg_count)
  def get(self):
    arg = retrieve_reg_count.parse_args().get("course_id")
    course_id = arg if arg else ""
    reg_count = Registration.query.filter(Registration.rcourse_ID.contains(course_id)).count()

    db.session.close()
    if reg_count >= 0:
      return jsonify(
        {
          "code": 200,
          "data": {
            "reg_count": reg_count
          }
        }
      )
    return json.loads(json.dumps({"message": "registration count error", "code": 404}, default=str))
