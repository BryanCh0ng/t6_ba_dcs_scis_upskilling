from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from core_features import common
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
        regList = Registration.query.filter(Registration.reg_ID == reg_ID).all()
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
        print(data)
        rcourse_ID = data.get("rcourse_ID")
        user_ID = data.get("user_ID")
        session_user_ID = common.getUserID()
        if session_user_ID != user_ID:
            return {"message": "Unathorized Access, No rights to create new registration"}, 404 

        # Check if a registration with the given rcourse_ID and user_ID exists
        existing_registration = Registration.query.filter_by(rcourse_ID=rcourse_ID, user_ID=user_ID).first()

        if existing_registration:
            # If the registration exists, update its reg_Status to "pending"
            try:
                existing_registration.reg_Status = "Pending"
                db.session.commit()
                return jsonify(
                    {
                        "code": 200,
                        "data": existing_registration.json(),
                        "message": "You have successfully registered for the course again. Please refer to your profile to find out the status."
                    }
                )
            except Exception as e:
                db.session.rollback()
                return "Failed to update registration status: " + str(e), 500
        else:
            # If the registration does not exist, create a new one
            registration = Registration(**data)
            try:
                db.session.add(registration)
                db.session.commit()
                return jsonify(
                    {
                        "code": 201,
                        "data": registration.json(),
                        "message": "You have successfully registered for the course. Please refer to your profile to find out the status."
                    }
                )
            except Exception as e:
                db.session.rollback()
                return "Failed to create new registration: " + str(e), 500

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
            db.session.close()
            return jsonify(
                {
                    "code": 404,
                    "message": "No such registration record exists"
                }
            )
        
        try:
            if data["user_ID"] != registration.user_ID:
                return {"message": "Unathorized Access, No rights to update registration"}, 404 

            for key, value in data.items():
                setattr(registration, key, value)

            db.session.commit()
            db.session.close()

            return jsonify(
                {
                    "code": 201,
                    "data": registration.json(),
                    "message": "Registration has been successfully updated!"
                }
            )
        
        except Exception as e:
            db.session.rollback()
            return "Failed" + str(e), 500

#get_registration_by_userid()
get_registration_by_userid = api.parser()
get_registration_by_userid.add_argument("user_ID", help="Enter user ID")
@api.route("/get_registration_by_userid")
@api.doc(description="Gets registration by user ID")
class GetRegistrationByUserID(Resource):
    @api.expect(get_registration_by_userid)
    def get(self):
        arg = get_registration_by_userid.parse_args().get("user_ID")
        user_ID = arg if arg else ""
        session_user_ID = common.getUserID()
        if user_ID != session_user_ID:
          return {"message": "Unathorized Access, No rights to view registrations"}, 404
 
        regList = Registration.query.filter(Registration.user_ID == user_ID).all()
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
    
# Drop registered course
drop_registered_course = api.parser()
drop_registered_course.add_argument("rcourse_ID", type=int, help="Run Course ID")
drop_registered_course.add_argument("user_ID", type=int, help="User ID")

@api.route('/drop_registered_course')
@api.doc(description="Update Registration Status to 'Dropped'")
class dropRegisteredCourse(Resource):
    @api.expect(drop_registered_course)
    def put(self):
        try:
            args = drop_registered_course.parse_args()
            rcourse_ID = args.get("rcourse_ID")
            user_ID = args.get("user_ID")

            registration = Registration.query.filter_by(rcourse_ID=rcourse_ID, user_ID=user_ID).first()

            if registration is None:
                db.session.close()
                return {"message": "Registration record not found for the specified course and user"}, 404

            if user_ID != registration.user_ID:
                db.session.close()
                return {"message": "Unathorized Access, No rights to update registration"}, 404 
    
            registration.reg_Status = 'Dropped'
            db.session.commit()
            db.session.close()

            return {"message": "The course has been dropped successfully."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to drop the course: " + str(e)}, 500