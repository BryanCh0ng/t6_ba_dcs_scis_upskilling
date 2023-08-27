from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('interest', description='Interest related operations')
  
retrieve_interest_count = api.parser()
retrieve_interest_count.add_argument("vote_id", help="Enter vote id")
@api.route("/retrieve_interest_count_by_vote_id")
@api.doc(description="Get Interest Vote Count")
class RetrieveInterestCount(Resource):
  @api.expect(retrieve_interest_count)
  def get(self):
    arg = retrieve_interest_count.parse_args().get("vote_id")
    vote_id = arg if arg else ""
    interest_count = Interest.query.filter(Interest.vote_ID.contains(vote_id)).count()

    db.session.close()
    if interest_count >= 0:
      return jsonify(
        {
          "code": 200,
          "data": {
            "interest_count": interest_count
          }
        }
      )
    return json.loads(json.dumps({"message": "interest count error", "code": 404}, default=str))
