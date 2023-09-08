from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
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

@api.route("/change_registration_status", methods=["PUT"])
@api.doc(description="Change registration status between ongoing and closed")
class ChangeRegistrationStatus(Resource):
    @api.expect(change_registration_status_model)
    def put(self):
        data = request.get_json()

        try:
            rcourseID = data["rcourse_ID"]
            rcourse = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()            
            if(rcourse):
                if rcourse.runcourse_Status == "Closed":
                    setattr(rcourse, "runcourse_Status", "Ongoing")
                else:
                    setattr(rcourse, "runcourse_Status", "Closed")

                db.session.commit()
                return json.loads(json.dumps(rcourse.json(), default=str)), 200

            return json.loads(json.dumps({"Message": "There is no such runcourse"}, default=str)), 404

        except Exception as e:
            return "Failed" + str(e), 500
        
# create_runcourse() --------------------------------------
create_runcourse_model = api.model("create_runcourse_model", {
    "selectedInstructor" : fields.Integer(description="", required=True),
    "startDate" : fields.Date(description="", required=True),
    "endDate" : fields.Date(description="", required=True),
    "startTime" : fields.String(description="", required=True),
    "endTime" : fields.String(description="", required=True),
    "selectedFormat" : fields.Integer(description="", required=True), # Holds the selected course format ID
    "venue" : fields.String(description="", required=True),
    "courseSize" : fields.Integer(description="", required=True),
    "minimumSlots" : fields.Integer(description="", required=True),
    "openingDate" : fields.Date(description="", required=True),
    "openingTime" : fields.String(description="", required=True),
    "closingDate" : fields.Date(description="", required=True),
    "closingTime" : fields.String(description="", required=True),
    "courseFee" : fields.Integer(description="", required=True),
    "selectedTemplate" : fields.Integer(description="", required=True)
})

@api.route("/create_runcourse", methods=["POST"])
@api.doc(description = "Create a new runcourse")
class CreateRuncourse(Resource):
    @api.expect(create_runcourse_model)
    def post(self):
        data = request.get_json()

        # get all the courseID templateID instructorID if input data is name instead of id
        # convert date time fields to sql ready
        # get duration (i assume system auto inserts duration and runcourse status, maybe even course status?)
        try:
            course_ID = Course.query.filter_by(course_Name=data['courseName']).first().course_ID
            # this sections assume coursecat name and template names are unique
            template_ID = FeedbackTemplate.query.filter_by(template_Name=data['selectedTemplate']).first().template_ID
            # assumes that instructors have unique names, may need to change the process including the data input
            instructor_ID = User.query.filter_by(user_Name=data['selectedInstructor'], role_Name="Instructor").first().user_ID

            newRunCourse = RunCourse(
                run_Startdate=self.convertDate(data['startDate']),
                run_Enddate=self.convertDate(data['endDate']),
                run_Starttime=self.convertTime(data['startTime']),
                run_Endtime=self.convertTime(data['endTime']),
                instructor_ID=instructor_ID,
                course_Format=data['selectedFormat'],
                course_Venue=data['venue'],
                runcourse_Status='Ongoing',
                course_Size=data['courseSize'],
                course_Minsize=data['minimumSlots'],
                course_Fee=data['courseFee'],
                class_Duration=self.getDuration(data['startTime'], data['endTime']),
                reg_Startdate=self.convertDate(data['openingDate']),
                reg_Enddate=self.convertDate(data['closingDate']),
                reg_Starttime=self.convertTime(data['openingTime']),
                reg_Endtime=self.convertTime(data['closingTime']),
                template_ID=template_ID,
                course_ID=course_ID,
                course_Status='Active'
            )
            db.session.add(newRunCourse)
            db.session.commit()
            return json.loads(json.dumps(newRunCourse.json(), default=str)), 200

        except Exception as e:
            return "Failed" + str(e), 500

    def convertTime(self, time):
        # input format: {'hours': 0, 'minutes': 57, 'seconds': 0}
        # output to database format: 00:00:00
        res = ""
        if int(time['hours']) < 10:
            res += "0" + str(time['hours']) + ":"
        else:
            res += str(time['hours']) + ":"
        if int(time['minutes']) < 10:
            res += "0" + str(time['minutes']) + ":00"
        else:
            res += str(time['minutes']) + ":00"
        return res

    def convertDate(self, date):
        # input format: 2023-08-31T16:57:00.000Z
        # output to database format: 2023-08-03
        newdate = str(date)
        return newdate.split("T")[0]

    def getDuration(self, start, end):
        # inputs: {'hours': 0, 'minutes': 57, 'seconds': 0}
        # output: integer of minutes
        # assumes end time does not cross midnight and start time is not before midnight
        minutes = 0
        minutes += (end['hours'] - start['hours']) * 60
        minutes += end['minutes'] - start['minutes']
        return minutes
    
# change_registration_status() --------------------------------
change_registration_status_model = api.model("change_registration_status_model", {
    "rcourse_ID": fields.Integer(description="Runcourse ID", required=True),
})
    
@api.route("/change_registration_status", methods=["POST"])
@api.doc(description="Change registration status between ongoing and closed")
class ChangeRegistrationStatus(Resource):
    @api.expect(change_registration_status_model)
    def post(self):
        data = request.get_json()

        try:
            rcourseID = data["rcourse_ID"]
            rcourse = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            message = ''            
            if(rcourse):
                if rcourse.runcourse_Status == "Closed":
                    setattr(rcourse, "runcourse_Status", "Ongoing")
                    setattr(rcourse, "course_Status", "Active")
                    message = 'Run Course registration closed'
                else:
                    setattr(rcourse, "runcourse_Status", "Closed")
                    setattr(rcourse, "course_Status", "Inactive")
                    message = 'Run Course registration Open'

                db.session.commit()
                return json.loads(json.dumps({"message": message, "code": 200}, default=str))

            return json.loads(json.dumps({"message": "There is no such runcourse", "code": 404}, default=str))

        except Exception as e:
            return "Failed" + str(e), 500
        
# create_runcourse() --------------------------------------
create_runcourse_model = api.model("create_runcourse_model", {
    "selectedInstructor" : fields.Integer(description="", required=True),
    "startDate" : fields.Date(description="", required=True),
    "endDate" : fields.Date(description="", required=True),
    "startTime" : fields.String(description="", required=True),
    "endTime" : fields.String(description="", required=True),
    "selectedFormat" : fields.Integer(description="", required=True), # Holds the selected course format ID
    "venue" : fields.String(description="", required=True),
    "courseSize" : fields.Integer(description="", required=True),
    "minimumSlots" : fields.Integer(description="", required=True),
    "openingDate" : fields.Date(description="", required=True),
    "openingTime" : fields.String(description="", required=True),
    "closingDate" : fields.Date(description="", required=True),
    "closingTime" : fields.String(description="", required=True),
    "courseFee" : fields.Integer(description="", required=True),
    "selectedTemplate" : fields.Integer(description="", required=True)
})

@api.route("/create_runcourse", methods=["POST"])
@api.doc(description = "Create a new runcourse")
class CreateRuncourse(Resource):
    @api.expect(create_runcourse_model)
    def post(self):
        data = request.get_json()

        # get all the courseID templateID instructorID if input data is name instead of id
        # convert date time fields to sql ready
        # get duration (i assume system auto inserts duration and runcourse status, maybe even course status?)
        try:
            course_ID = Course.query.filter_by(course_Name=data['courseName']).first().course_ID
            # this sections assume coursecat name and template names are unique
            template_ID = FeedbackTemplate.query.filter_by(template_Name=data['selectedTemplate']).first().template_ID
            # assumes that instructors have unique names, may need to change the process including the data input
            instructor_ID = User.query.filter_by(user_Name=data['selectedInstructor'], role_Name="Instructor").first().user_ID

            newRunCourse = RunCourse(
                run_Startdate=self.convertDate(data['startDate']),
                run_Enddate=self.convertDate(data['endDate']),
                run_Starttime=self.convertTime(data['startTime']),
                run_Endtime=self.convertTime(data['endTime']),
                instructor_ID=instructor_ID,
                course_Format=data['selectedFormat'],
                course_Venue=data['venue'],
                runcourse_Status='Ongoing',
                course_Size=data['courseSize'],
                course_Minsize=data['minimumSlots'],
                course_Fee=data['courseFee'],
                class_Duration=self.getDuration(data['startTime'], data['endTime']),
                reg_Startdate=self.convertDate(data['openingDate']),
                reg_Enddate=self.convertDate(data['closingDate']),
                reg_Starttime=self.convertTime(data['openingTime']),
                reg_Endtime=self.convertTime(data['closingTime']),
                template_ID=template_ID,
                course_ID=course_ID,
                course_Status='Active'
            )
            db.session.add(newRunCourse)
            db.session.commit()
            return json.loads(json.dumps(newRunCourse.json(), default=str)), 200

        except Exception as e:
            return "Failed" + str(e), 500

    def convertTime(self, time):
        # input format: {'hours': 0, 'minutes': 57, 'seconds': 0}
        # output to database format: 00:00:00
        res = ""
        if int(time['hours']) < 10:
            res += "0" + str(time['hours']) + ":"
        else:
            res += str(time['hours']) + ":"
        if int(time['minutes']) < 10:
            res += "0" + str(time['minutes']) + ":00"
        else:
            res += str(time['minutes']) + ":00"
        return res

    def convertDate(self, date):
        # input format: 2023-08-31T16:57:00.000Z
        # output to database format: 2023-08-03
        newdate = str(date)
        return newdate.split("T")[0]

    def getDuration(self, start, end):
        # inputs: {'hours': 0, 'minutes': 57, 'seconds': 0}
        # output: integer of minutes
        # assumes end time does not cross midnight and start time is not before midnight
        minutes = 0
        minutes += (end['hours'] - start['hours']) * 60
        minutes += end['minutes'] - start['minutes']
        return minutes