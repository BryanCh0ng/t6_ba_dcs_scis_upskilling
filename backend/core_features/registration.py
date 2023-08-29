from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('registration', description='Registration related operations')

# ==================== REGISTRATION FUNCTIONS ====================#
# get_all_registrations()
# create_new_registration()
# update_registration()

# get_all_registrations()
get_all_registrations = api.parser()
get_all_registrations.add_argument("reg_ID", help="Enter registration ID")
@api.route("/get_all_registrations")
@api.doc(description="Gets all registrations")
class GetAllRegistrations(Resource):
    @api.expect(get_all_registrations)
    def get(self):
        arg = get_all_registrations.parse_args().get("reg_ID")
        reg_ID = arg if arg else ""
        regList = Registration.query.filter(Registration.reg_ID.contains(reg_ID)).all()
        db.session.close()

        if len(regList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reg_list": [reg.json() for reg in regList]
                    }
                }
            )
        
        return jsonify(
            {
                "code": 404,
                "message": "No such registration record exists"
            }
        )

# create_new_registration()
create_registration_model = api.model("create_registration_model", {
    "rcourse_ID" : fields.Integer(description="Run Course ID", required=True),
    "user_ID" : fields.Integer(description="User ID", required=True),
    "reg_Status" : fields.String(description="Registration status", required=True)
})

@api.route("/create_new_registration", methods=["POST"])
@api.doc(description="Creates new registration")
class CreateNewRegistration(Resource):
    @api.expect(create_registration_model)
    def post(self):
        data = request.get_json()
        registration = Registration(**data)

        try:
            db.session.add(registration)
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": registration.json(),
                    "message": "Registration has been successfully created!"
                }
            )
        
        
        except Exception as e:
            return "Failed" + str(e), 500

#update_registration()
update_registration_model = api.model("update_registration_model", {
    "reg_ID": fields.Integer(description="Registration ID", required=True),
    "rcourse_ID" : fields.Integer(description="Run Course ID", required=True),
    "user_ID" : fields.Integer(description="User ID", required=True),
    "reg_Status" : fields.String(description="Registration status", required=True)
})

@api.route("/update_registration", methods=["PUT"])
@api.doc(description="Update registration record")
class UpdateRegistration(Resource):
    @api.expect(update_registration_model)
    def put(self):
        data = request.get_json()
        reg_ID = data["reg_ID"]
        registration = Registration.query.filter_by(reg_ID=reg_ID).first()

        if not registration:
            return jsonify(
                {
                    "code": 404,
                    "message": "No such registration record exists"
                }
            )
        
        try:
            for key, value in data.items():
                setattr(registration, key, value)

            db.session.commit()

            return jsonify(
                {
                    "code": 201,
                    "data": registration.json(),
                    "message": "Registration has been successfully updated!"
                }
            )
        
        except Exception as e:
            return "Failed" + str(e), 500