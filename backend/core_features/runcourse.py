from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
from core_features import common
import json
from sqlalchemy import distinct
from datetime import datetime, timedelta

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
            course.feedback_Starttime = course.feedback_Starttime.strftime('%H:%M:%S')
            course.feedback_Endtime = course.feedback_Endtime.strftime('%H:%M:%S')

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
            return {
                "message": "Unathorized Access, Failed to create run course"
            }, 404

        data = request.get_json()

        try:
            rcourseID = data["rcourse_ID"]
            rcourse = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            course = Course.query.filter_by(course_ID=rcourse.course_ID).first()
            message = ''            

            current_datetime = datetime.now()
            current_date = current_datetime.strftime('%Y-%m-%d')
            close_date = (current_datetime + timedelta(days=5)).strftime('%Y-%m-%d')

            rcourse_run_startdate_str = rcourse.run_Startdate.strftime('%Y-%m-%d')
            # print(rcourse_run_startdate_str)
            if rcourse_run_startdate_str <= close_date:
                close_date = (rcourse.run_Startdate - timedelta(days=1)).strftime('%Y-%m-%d')
            
            current_time = current_datetime.strftime('%H:%M:%S')

            if(rcourse):
                if rcourse.runcourse_Status == "Closed":
                    setattr(rcourse, "runcourse_Status", "Ongoing")
                    setattr(course, "course_Status", "Active")
                    setattr(rcourse, "reg_Startdate", current_date)
                    setattr(rcourse, "reg_Starttime", current_time)
                    setattr(rcourse, "reg_Enddate", close_date)
                    setattr(rcourse, "reg_Endtime", "10:00:00")
                    message = 'Run Course registration Opened'
                else:
                    setattr(rcourse, "runcourse_Status", "Closed")
                    setattr(course, "course_Status", "Inactive")
                    message = 'Run Course registration Closed'

                db.session.commit()

                return json.loads(json.dumps({"message": message, "code": 200}, default=str))

            return json.loads(json.dumps({"message": "There is no such runcourse", "code": 404}, default=str))

        except Exception as e:
            db.session.rollback()
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
                return {
                    "message": "Unathorized Access, Failed to edit run course"
                }, 404
    
            #Get the updated data from the request body 
            updated_data = request.json
        
            runcourse = RunCourse.query.filter_by(rcourse_ID=runcourse_id).first()

            if not runcourse:
                return {
                    'message': "There is no such runcourse"
                }, 404

             # Get instructor availability data from the updated data
            start_date = datetime.strptime(updated_data.get('run_Startdate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(updated_data.get('run_Enddate'), '%Y-%m-%d').date()
            start_time = datetime.strptime(updated_data.get('run_Starttime'), '%H:%M:%S').time()
            end_time = datetime.strptime(updated_data.get('run_Endtime'), '%H:%M:%S').time()
            instructor_id = updated_data.get('instructor_ID')

            # Query existing run courses for the given instructor
            #runs = RunCourse.query.filter_by(instructor_ID=instructor_id).all()

            # Query existing run courses for the given instructor excluding the current record being edited
            runs = RunCourse.query.filter(RunCourse.instructor_ID == instructor_id, RunCourse.rcourse_ID != runcourse_id).all()
            
            # Check instructor availability
            if runs:
                for run in runs:
                    if run.run_Startdate <= end_date and run.run_Enddate >= start_date:
                        if run.run_Endtime >= start_time and run.run_Starttime <= end_time:
                            return {
                                'message': 'Instructor is already occupied at the chosen date and time'
                            }, 400

    
            # Update the fields based on updated_data
            for field, value in updated_data.items():
                #print(f"Updating {field} to {value}")
                setattr(runcourse, field, value)

            #Commit the changes to the database 
            db.session.commit()
            # db.session.close()

           # Convert dates and times to formatted strings
            runcourse.run_Startdate = start_date.strftime('%Y-%m-%d')
            runcourse.run_Enddate = end_date.strftime('%Y-%m-%d')
            runcourse.run_Starttime = start_time.strftime('%H:%M:%S')
            runcourse.run_Endtime = end_time.strftime('%H:%M:%S')

            runcourse.reg_Startdate = runcourse.reg_Startdate.strftime('%Y-%m-%d')
            runcourse.reg_Enddate = runcourse.reg_Enddate.strftime('%Y-%m-%d')
            runcourse.reg_Starttime = runcourse.reg_Starttime.strftime('%H:%M:%S')
            runcourse.reg_Endtime = runcourse.reg_Endtime.strftime('%H:%M:%S')

            runcourse.feedback_Startdate = runcourse.feedback_Startdate.strftime('%Y-%m-%d')
            runcourse.feedback_Enddate = runcourse.feedback_Enddate.strftime('%Y-%m-%d')
            runcourse.feedback_Starttime = runcourse.feedback_Starttime.strftime('%H:%M:%S')
            runcourse.feedback_Endtime = runcourse.feedback_Endtime.strftime('%H:%M:%S')

            return {
                'message': 'Run course updated successfully',
                'data': runcourse.json()
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                "message": "Failed to update run course: " + str(e)
            }, 500

@api.route("/create_runcourse/<int:course_id>", methods=["POST"])
@api.doc(description="Create run course")
class CreateRunCourse(Resource):
    def post(self, course_id):
        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to create run course"
                }, 404

            # Get the data for creating a new run course from the request body
            new_run_course_data = request.json

            start_date = datetime.strptime(new_run_course_data.get('run_Startdate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(new_run_course_data.get('run_Enddate'), '%Y-%m-%d').date()
            start_time = datetime.strptime(new_run_course_data.get('run_Starttime'), '%H:%M:%S').time()
            end_time = datetime.strptime(new_run_course_data.get('run_Endtime'), '%H:%M:%S').time()
            instructor_id = new_run_course_data.get('instructor_ID')

            runs = RunCourse.query.filter_by(instructor_ID=instructor_id).all()

            if runs:
                for run in runs:
                    if run.run_Startdate <= end_date and run.run_Enddate >= start_date:
                        if run.run_Endtime >= start_time and run.run_Starttime <= end_time:
                            return {
                                'message': 'Instructor is already occupied at the chosen date and time'
                            }, 400
                
            #print(new_run_course_data)

            # Create a new run course object with the data
            new_run_course = RunCourse(**new_run_course_data)

            # Add the new course to the database
            db.session.add(new_run_course)

            # Commit the changes to the database
            db.session.commit()

            # Inside the create_proposed_course route
            #print("Data before returning:", new_proposed_course.json())

            # Return the newly created course as JSON response
            #return json.loads(json.dumps(new_run_course.json(), default=str)), 201

            # Convert dates and times to formatted strings
            new_run_course.run_Startdate = start_date.strftime('%Y-%m-%d')
            new_run_course.run_Enddate = end_date.strftime('%Y-%m-%d')
            new_run_course.run_Starttime = start_time.strftime('%H:%M:%S')
            new_run_course.run_Endtime = end_time.strftime('%H:%M:%S')

            new_run_course.reg_Startdate = new_run_course.reg_Startdate.strftime('%Y-%m-%d')
            new_run_course.reg_Enddate = new_run_course.reg_Enddate.strftime('%Y-%m-%d')
            new_run_course.reg_Starttime = new_run_course.reg_Starttime.strftime('%H:%M:%S')
            new_run_course.reg_Endtime = new_run_course.reg_Endtime.strftime('%H:%M:%S')

            new_run_course.feedback_Startdate = new_run_course.feedback_Startdate.strftime('%Y-%m-%d')
            new_run_course.feedback_Enddate = new_run_course.feedback_Enddate.strftime('%Y-%m-%d')
            new_run_course.feedback_Starttime = new_run_course.feedback_Starttime.strftime('%H:%M:%S')
            new_run_course.feedback_Endtime = new_run_course.feedback_Endtime.strftime('%H:%M:%S')

            return {
                'message': 'Run course created successfully',
                'data': new_run_course.json()  # Assuming new_run_course.json() returns the required data as a dictionary
            }, 201

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {
                "message": "Failed to create a new run course: " + str(e)
            }, 500
        
# Apply Feedback Template to Course
course_apply_feedback_template = api.parser()
course_apply_feedback_template.add_argument("rcourse_id", help="Enter course id")
course_apply_feedback_template.add_argument("template_id", help="Enter template id")
@api.route("/course_apply_feedback_template")
@api.doc(description="Apply feedback template to a course")
class CourseApplyFeedbackTemplate(Resource):
    @api.expect(course_apply_feedback_template)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unauthorized Access, Failed to apply feedback template to run course"}, 404

            args = course_apply_feedback_template.parse_args()
            rcourseID = args.get("rcourse_id")
            templateID = args.get("template_id")
            
            course = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            print(course)
            print(templateID)

            # check if template id is valid
            if course is None:
                return jsonify({"message": "run course course not found", "code": 404}), 404

            if datetime.now().date() > course.run_Startdate: #TO CHANGE TO FEEDBACK DATE
                return jsonify({"message": "run course in ongoing feedback period", "code": 404}), 404
            elif datetime.now().date() > course.run_Enddate:  #TO CHANGE TO FEEDBACK DATE
                return jsonify({"message": "run course in past feedback period", "code": 404}), 404

            course.template_ID = templateID
            db.session.commit()
            return jsonify({"code": 200, "message": "Run course assign feedback template success"})

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({"code": 500, "message": "Failed. " + str(e)})

get_course_formats = api.parser()
@api.route("/get_course_formats")
@api.doc(description="Get course formats")
class GetCourseFormats(Resource):
    @api.expect(get_course_formats)
    def get(self):
        distinct_course_formats = db.session.query(distinct(RunCourse.course_Format)).all()
        db.session.close()

        if distinct_course_formats:
            return json.loads(json.dumps(distinct_course_formats, default=str)), 200

        return json.loads(json.dumps({"message": "No course formats found."})), 404

# Modify the parser name to avoid overlap
retrieve_run_course_count = api.parser()
retrieve_run_course_count.add_argument("course_id", help="Enter course id")
@api.route("/get_run_course_count_by_course_id")
@api.doc(description="Get run course count by course id")
class GetRunCourseCount(Resource):
    @api.expect(retrieve_run_course_count)
    def get(self):
        courseID = retrieve_run_course_count.parse_args().get("course_id")
        
        run_course_count = RunCourse.query.filter_by(course_ID=courseID).count()

        course = Course.query.filter_by(course_ID=courseID).first()

        db.session.close()

        if run_course_count >= 0:

            course_name = course.course_Name

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "run_course_count": run_course_count,
                        "course_name": course_name
                    }
                }
            )
        
        return json.loads(json.dumps({"message": "There are no run courses for this course ID", "code": 404}, default=str))
