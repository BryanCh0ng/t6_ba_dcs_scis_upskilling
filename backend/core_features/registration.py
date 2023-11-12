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
        if reg_ID:
            regList = Registration.query.filter(Registration.reg_ID == reg_ID).all()
        else:
            regList = Registration.query.all()
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

update_registration = api.parser()
@api.route("/update_registration/<int:reg_id>", methods=["PUT"])
@api.doc(description="Update registration record by registration id")
class UpdateRegistration(Resource):
    @api.expect(update_registration)
    def put(self, reg_id):
        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to edit registration"
                }, 404

            #Get the update data from the request body
            update_data = request.json

            registration = Registration.query.filter_by(reg_ID=reg_id).first()

            if not registration:
                return jsonify(
                    {
                        "code": 404,
                        "message": "No registration record found"
                    }
                )
            
            for field, value in update_data.items():
                setattr(registration, field, value)

            db.session.commit()

            return jsonify(
                {
                    "code": 201,
                    "data": registration.json(),
                    "message": "Registration has been successfully updated!"
                }
            )
            
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to update registration record: " + str(e)
                }
            )

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

#get_registration_by_rcourseid
get_registration_by_rcourseid = api.parser()
get_registration_by_rcourseid.add_argument("rcourse_ID", help="Enter run course ID")
get_registration_by_rcourseid.add_argument("student_name", help="Enter student name")
get_registration_by_rcourseid.add_argument("reg_status", help="Enter registration status")
@api.route("/get_registration_by_rcourseid")
@api.doc(description="Gets registration by run course ID")    
class GetRegistrationByRCourseID(Resource):
    @api.expect(get_registration_by_rcourseid)
    def get(self):
        try: 
            user_role = common.getUserRole()
            if user_role != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to get registration records"
                }, 404
    
            args = get_registration_by_rcourseid.parse_args()
            rcourse_ID = args.get("rcourse_ID", "")

            query = (
                db.session.query(Registration, User, Blacklist)
                .join(Registration, User.user_ID == Registration.user_ID)
                .outerjoin(Blacklist, User.user_ID == Blacklist.user_ID)
                .filter(Registration.rcourse_ID == rcourse_ID)
            )

            student_name = args.get("student_name", "")
            reg_status = args.get("reg_status", "")

            if student_name: 
                student_name = student_name.lower()
                query = query.filter(User.user_Name.ilike(f"%{student_name}%"))
            
            if reg_status:
                query = query.filter(Registration.reg_Status == reg_status)

            filtered_results = query.all()
            db.session.close()

            if filtered_results:
                data = []

                for registration, user, blacklist in filtered_results:
                    blacklist_status = "Blacklisted" if blacklist else "Not Blacklisted"

                    combined_data = {
                        "user_ID": user.user_ID,
                        "user_Email": user.user_Email,
                        "user_Name": user.user_Name,
                        "reg_ID": registration.reg_ID,
                        "reg_Status": registration.reg_Status,
                        "blacklist_Status": blacklist_status
                    }

                    data.append(combined_data)

                return jsonify(
                    {
                        "code": 200, 
                        "data": data
                    }
                )
            
            return jsonify(
                {
                    "code": 404,
                    "message": "No registration records found for this run course."
                }
            )

        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retrieve run course registration: " + str(e)
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
                return {"message": "Registration record not found for the specified course and user"}, 404

            if user_ID != registration.user_ID:
                return {"message": "Unathorized Access, No rights to update registration"}, 404 
    
            registration.reg_Status = 'Dropped'
            db.session.commit()
            db.session.close()

            return {"message": "The course has been dropped successfully."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to drop the course: " + str(e)}, 500

enroll_student = api.parser()
enroll_student.add_argument("reg_IDs", help="Enter registration ID")
@api.route("/enroll_student", methods=["POST"])
@api.doc(description="Enroll student into a run course")
class EnrollStudent(Resource):
    @api.expect(enroll_student)
    def post(self):
        args = enroll_student.parse_args()
        reg_IDs_json = args.get("reg_IDs", "")
       
        try:
            if reg_IDs_json and reg_IDs_json != '[]':
            
                reg_IDs = json.loads(reg_IDs_json)

                if len(reg_IDs) > 0:
                    total_enrolled = 0
                    invalid_reg_status = 0
                    invalid_regID = 0

                    for regID in reg_IDs:
                        student = Registration.query.filter_by(reg_ID=regID).first()

                        if student:
                            if student.reg_Status == "Pending":
                                student.reg_Status = "Enrolled"
                                db.session.commit()
                                total_enrolled += 1
                            else:
                                invalid_reg_status += 1
                        else:
                            invalid_regID += 1

                    if total_enrolled > 0:
                        return jsonify(
                            {
                                "code": 200,
                                "message": "Student(s) enrolled successfully"
                            }
                        )
                    elif invalid_reg_status > 0:
                        return jsonify(
                            {
                                "code": 400,
                                "message": "Cannot enroll student(s) with status that does not equals to 'Pending'"
                            }
                        )
                    elif invalid_regID > 0:
                        return jsonify(
                            {
                                "code": 404,
                                "message": "Invalid registration ID(s)"
                            }
                        )

            return jsonify(
                {
                    "code": 400,
                    "message": "No student is selected"
                }
            )
  
        except Exception as e:
            
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to enroll student(s): " + str(e)
                }
            )

drop_student = api.parser()
drop_student.add_argument("reg_IDs", help="Enter registration ID")
@api.route("/drop_student", methods=["POST"])
@api.doc(description="Drop enrolled student from a run course")
class DropStudent(Resource):
    @api.expect(drop_student)
    def post(self):
        args = drop_student.parse_args()
        reg_IDs_json = args.get("reg_IDs", "")
       
        try:
            if reg_IDs_json and reg_IDs_json != '[]':
              
                reg_IDs = json.loads(reg_IDs_json)

                if len(reg_IDs) > 0:
                    total_dropped = 0
                    invalid_reg_status = 0
                    invalid_regID = 0

                    for regID in reg_IDs:
                        student = Registration.query.filter_by(reg_ID=regID).first()

                        if student:
                            if student.reg_Status == "Enrolled":
                                student.reg_Status = "Dropped"
                                db.session.commit()
                                total_dropped += 1
                            else:
                                invalid_reg_status += 1
                        else:
                            invalid_regID += 1

                    if total_dropped > 0:
                        return jsonify(
                            {
                                "code": 200,
                                "message": "Dropped enrolled student(s) successfully"
                            }
                        )
                    elif invalid_reg_status > 0:
                        return jsonify(
                            {
                                "code": 400,
                                "message": "Cannot drop student(s) with status that does not equals to 'Enrolled'"
                            }
                        )
                    elif invalid_regID > 0:
                        return jsonify(
                            {
                                "code": 404,
                                "message": "Invalid registration ID(s)"
                            }
                        )

            return jsonify(
                {
                    "code": 400,
                    "message": "No student is selected"
                }
            )
  
        except Exception as e:
            
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to drop enrolled student(s): " + str(e)
                }
            )