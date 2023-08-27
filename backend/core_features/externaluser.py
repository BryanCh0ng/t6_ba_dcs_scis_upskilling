from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('externaluser', description='External User related operations')


get_external_user_by_user_id = api.parser()
get_external_user_by_user_id.add_argument("user_id", help="Enter user id")
@api.route("/get_external_user_by_user_id")
@api.doc(description="Get External User by user id")
class GetExternalUserByUserId(Resource):
  @api.expect(get_external_user_by_user_id)
  def get(self):
    userID = get_external_user_by_user_id.parse_args().get("user_id")
    externalUser = ExternalUser.query.filter_by(user_ID=userID).first()
    db.session.close()
    if externalUser:
      return jsonify(
      {
        "code": 200,
        "data": {
          "externalUser": [externalUser.json()]
        }
      }
    )
    return json.loads(json.dumps({"message": "There is no such external user", "code": 404}, default=str))
