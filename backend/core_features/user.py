from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('user', description='User related operations')

# ==================== USER FUNCTIONS ====================#
# get_instructors()

get_instructors = api.parser()
@api.route("/get_instructors")
@api.doc(description="Get all instructors")
class GetInstructors(Resource):
    @api.expect(get_instructors)
    def get(self):
        instructors = User.query.filter_by(role_Name='Instructor').all()
        db.session.close()
        
        if instructors:
            instructors_json = [instructor.json() for instructor in instructors]
            return {"code": 200, "data": {"instructors": instructors_json}}, 200

        return {"code": 404, "message": "No instructors found"}, 404