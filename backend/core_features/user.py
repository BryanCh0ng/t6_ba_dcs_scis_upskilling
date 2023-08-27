from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('user', description='User related operations')

retrieve_all_instructors = api.parser()
@api.route("/get_all_instructors")
@api.doc(description="Get all instructors")
class GetAllInstructors(Resource):
	@api.expect(retrieve_all_instructors)
	def get(self):
		instructorList = User.query.filter(User.role_Name.contains('Instructor')).all()
		db.session.close()
		if len(instructorList):
			return jsonify(
				{
					"code": 200,
					"data": {
						"instructor": [instructor.json() for instructor in instructorList]
					}
				}
			)
		return json.loads(json.dumps({"message": "There is no instructors", "code": 404}, default=str))
	
retrieve_all_trainers = api.parser()
@api.route("/get_all_trainers")
@api.doc(description="Get all trainers")
class GetAllTrainers(Resource):
	@api.expect(retrieve_all_trainers)
	def get(self):
		trainerList = User.query.filter(User.role_Name.contains('Trainer')).all()
		db.session.close()
		if len(trainerList):
			return jsonify(
				{
					"code": 200,
					"data": {
						"trainer": [trainer.json() for trainer in trainerList]
					}
				}
			)
		return json.loads(json.dumps({"message": "There is no trainers", "code": 404}, default=str))
	
retrieve_user = api.parser()
retrieve_user.add_argument("user_id", help="Enter user id")
@api.route("/get_user_by_id")
@api.doc(description="Get user by user id")
class GetUser(Resource):
    @api.expect(retrieve_user)
    def get(self):
        user_ID = retrieve_user.parse_args().get("user_id")
        user = User.query.filter_by(user_ID=user_ID).first()
        db.session.close()
        if user:
          return jsonify(
            {
            "code": 200,
            "data": {
              "user": [user.json()]
            }
          }
        )
        return json.loads(json.dumps({"message": "There is no such user", "code": 404}, default=str))
