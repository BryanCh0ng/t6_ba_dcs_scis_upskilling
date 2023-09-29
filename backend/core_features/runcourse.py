from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
from core_features import common
import json

api = Namespace('runcourse', description='Run Course related operations')

# ==================== Run COURSE FUNCTIONS ====================#
# get_all_runcourses()
# get_run_course_by_course_id()
# change_registration_status()
# create_runcourse()

# get_all_runcourses() ---------------------------------------------
retrieve_all_runcourses = api.parser()
retrieve_all_runcourses.add_argument("course_id", help="Enter course id")
@api.route("/get_all_runcourses")
@api.doc(description="Get all run courses")
class GetAllRunCourses(Resource):
    @api.expect(retrieve_all_runcourses)
    def get(self):
        arg = retrieve_all_runcourses.parse_args().get("course_id")
        course_id = arg if arg else ""
        if course_id == "":
            runCourseList = RunCourse.query.filter(RunCourse.course_ID.contains(course_id)).all()
        else:
            runCourseList = RunCourse.query.filter(RunCourse.course_ID.like(course_id)).all()
        
        db.session.close()
        if len(runCourseList):
            for course in runCourseList:
                course.run_Starttime = course.run_Starttime.strftime('%H:%M:%S')
                course.run_Endtime = course.run_Endtime.strftime('%H:%M:%S')
                course.reg_Starttime = course.reg_Starttime.strftime('%H:%M:%S')
                course.reg_Endtime = course.reg_Endtime.strftime('%H:%M:%S')  
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [finalcourse.json() for finalcourse in runCourseList]
                    }
                }
            )
        return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

# get_run_course_by_course_id() ------------------------------------
retrieve_run_course = api.parser()
retrieve_run_course.add_argument("course_id", help="Enter course id")
@api.route("/get_run_course_by_course_id")
@api.doc(description="Get run course by course id")
class GetRunCourse(Resource):
    @api.expect(retrieve_run_course)
    def get(self):
        courseID = retrieve_run_course.parse_args().get("course_id")
        course = RunCourse.query.filter_by(course_ID=courseID).first()
        db.session.close()
        if course:
            course.run_Starttime = course.run_Starttime.strftime('%H:%M:%S')
            course.run_Endtime = course.run_Endtime.strftime('%H:%M:%S')
            course.reg_Starttime = course.reg_Starttime.strftime('%H:%M:%S')
            course.reg_Endtime = course.reg_Endtime.strftime('%H:%M:%S')
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json()]
                    }
                }
            )
        return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

# change_registration_status() --------------------------------
change_registration_status_model = api.model("change_registration_status_model", {
    "rcourse_ID": fields.Integer(description="Runcourse ID", required=True),
})

@api.route("/change_registration_status", methods=["POST"])
@api.doc(description="Change registration status between ongoing and closed")
class ChangeRegistrationStatus(Resource):
    @api.expect(change_registration_status_model)
    def post(self):

        user_role = common.getUserRole()
        if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to change registration status for run course"}, 404

        data = request.get_json()

        try:
            rcourseID = data["rcourse_ID"]
            rcourse = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            message = ''            
            if(rcourse):
                if rcourse.runcourse_Status == "Closed":
                    setattr(rcourse, "runcourse_Status", "Ongoing")
                    setattr(rcourse, "course_Status", "Active")
                    message = 'Run Course registration Opened'
                else:
                    setattr(rcourse, "runcourse_Status", "Closed")
                    setattr(rcourse, "course_Status", "Inactive")
                    message = 'Run Course registration Closed'

                db.session.commit()
                return json.loads(json.dumps({"message": message, "code": 200}, default=str))

            return json.loads(json.dumps({"message": "There is no such runcourse", "code": 404}, default=str))

        except Exception as e:
            return "Failed" + str(e), 500

get_runcourse_by_id = api.parser()
get_runcourse_by_id.add_argument("runcourse_id", help="Enter runcourse id")
@api.route("/get_runcourse_by_id")
@api.doc(description="Get run course by runcourse id")
class GetRunCourse(Resource):
    @api.expect(get_runcourse_by_id)
    def get(self):
        rcourse_id = get_runcourse_by_id.parse_args().get("runcourse_id")  # Use "runcourse_id" instead of "rcourse_ID"
        runcourse = RunCourse.query.filter_by(rcourse_ID=rcourse_id).first()  # Use "rcourse_ID" instead of "rcourse_id"
        db.session.close()

        if runcourse:
            return json.loads(json.dumps(runcourse.json(), default=str)), 200

        return json.loads(json.dumps({"message": "There is no such runcourse"})), 404

edit_runcourse = api.parser()
@api.route("/edit_runcourse/<int:runcourse_id>", methods=["PUT"])
class EditRunCourse(Resource):
    @api.expect(edit_runcourse)
    def put(self, runcourse_id):

        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to edit run course"}, 404
    
            #Get the updated data from the request body 
            updated_data = request.json
        
            runcourse = RunCourse.query.filter_by(rcourse_ID=runcourse_id).first()

            if runcourse:
                # Update the fields based on updated_data
                for field, value in updated_data.items():
                    #print(f"Updating {field} to {value}")
                    setattr(runcourse, field, value)

                #Commit the changes to the database 
                db.session.commit()

                return json.loads(json.dumps(runcourse.json(), default=str)), 200

            return json.loads(json.dumps({"message": "There is no such runcourse"})), 404

        except Exception as e:
            print("Error:", str(e))
            return "Failed" + str(e), 500

@api.route("/create_runcourse/<int:course_id>", methods=["POST"])
@api.doc(description="Create run course")
class CreateRunCourse(Resource):
    def post(self, course_id):
        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to create run course"}, 404
            
            # Get the data for creating a new run course from the request body
            new_run_course_data = request.json

            print(new_run_course_data)

            # Create a new run course object with the data
            new_run_course = RunCourse(**new_run_course_data)

            # Add the new course to the database
            db.session.add(new_run_course)

            # Commit the changes to the database
            db.session.commit()

            # Inside the create_proposed_course route
            #print("Data before returning:", new_proposed_course.json())

            # Return the newly created course as JSON response
            return json.loads(json.dumps(new_run_course.json(), default=str)), 201

        except Exception as e:
            print("Error:", str(e))
            return "Failed to create a new course: " + str(e), 500