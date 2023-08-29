from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('course', description='Course related operations')

# ==================== COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_course()

retrieve_all_courses = api.parser()
retrieve_all_courses.add_argument("course_name", help="Enter course name")
@api.route("/get_all_courses")
@api.doc(description="Get all courses")
class GetAllCourses(Resource):
    @api.expect(retrieve_all_courses)
    def get(self):
        arg = retrieve_all_courses.parse_args().get("course_name")
        course_Name = arg if arg else ""
        courseList = Course.query.filter(Course.course_Name.contains(course_Name)).all()
        db.session.close()
        if len(courseList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in courseList]
                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course"}, default=str)), 404

retrieve_all_courses_hr = api.parser()
@api.route("/get_all_courses_admin")
@api.doc(description="Get all courses (Admin)")
class GetAllCoursesHR(Resource):
    @api.expect(retrieve_all_courses_hr)
    def get(self):
        courseList = Course.query.all()
        db.session.close()
        if len(courseList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in courseList]
                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course"}, default=str)), 404

retrieve_all_courses_filter_search = api.parser()
retrieve_all_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_all_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
@api.route("/retrieve_all_courses_filter_search")
@api.doc(description="Get all courses filter + search")
class GetAllCoursesFilterSearch(Resource):
    @api.expect(retrieve_all_courses_filter_search)
    def get(self):
        arg = retrieve_all_courses.parse_args().get("course_name")
        course_Name = arg if arg else ""
        arg2 = retrieve_all_courses_filter_search.parse_args().get("coursecat_id")
        coursecat_ID = arg2 if arg2 else ""
        courseList = Course.query.filter(Course.course_Name.contains(course_Name), Course.coursecat_ID.contains(coursecat_ID)).all()
        db.session.close()
        if len(courseList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in courseList]

                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course" }, default=str)), 404

delete_course = api.parser()
delete_course.add_argument("course_id", help="Enter course id")
@api.route("/delete_course")
@api.doc(description="Delete course")
class DeleteCourse(Resource):
    @api.expect(delete_course)
    def put(self):    
        try:
            courseID = delete_course.parse_args().get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()            
            if(course):
                    db.session.delete(course)
                    db.session.commit()
                    return json.loads(json.dumps({"message":"Course successfully deleted"})), 200

            return json.loads(json.dumps({"Message": "There is no such course"}, default=str)), 404



        except Exception as e:
            return "Failed" + str(e), 500



retrieve_course = api.parser()
retrieve_course.add_argument("course_id", help="Enter course id")
@api.route("/get_course_by_id")
@api.doc(description="Get course by course id")
class GetCourse(Resource):
    @api.expect(retrieve_course)
    def get(self):
        courseID = retrieve_course.parse_args().get("course_id")
        course = Course.query.filter_by(course_ID=courseID).first()
        db.session.close()
        if course:
            return json.loads(json.dumps(course.json())), 200

        return json.loads(json.dumps({"message": "There is no such course"})), 404


# ==================== Create Course ====================#
create_course_model = api.model("create_course_model", {
    "courseName" : fields.String(description="", required=True),
    "selectedCategory" : fields.Integer(description="", required=True),
    "courseDescription" : fields.String(description="", required=True),
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

@api.route("/create_course", methods=["POST"])
@api.doc(description = "Create a new course")
class CreateCourse(Resource):
    @api.expect(create_course_model)
    def post(self):
        data = request.get_json()
        coursecat_ID = CourseCategory.query.filter_by(coursecat_Name=data['selectedCategory']).first().coursecat_ID
        
        # check if course already exists, else create course
        if not Course.query.filter_by(course_Name=data['courseName']).first():
            newCourse = Course(course_Name=data['courseName'], course_Desc=data['courseDescription'], coursecat_ID=coursecat_ID)
            db.session.add(newCourse)

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


edit_course_model = api.model("edit_course_model", {
    "course_ID": fields.Integer(description="Course ID", required=True),
    "course_Name": fields.String(description="Course Name", required=True),
    "course_Desc": fields.String(description="Course Description", required=True),
    "coursecat_ID": fields.Integer(description="Course Category ID", required=True),

})

@api.route("/edit_course", methods=["PUT"])
@api.doc(description="Edit course")
class EditCourse(Resource):
    @api.expect(edit_course_model)
    def put(self):
        data = request.get_json()
        

        try:
            courseID = data["course_ID"]
            course = Course.query.filter_by(course_ID=courseID).first()            
            if(course):
                for key, value in data.items():
                    setattr(course, key, value)

                db.session.commit()
                return json.loads(json.dumps(course.json(), default=str)), 200

            return json.loads(json.dumps({"Message": "There is no such course"}, default=str)), 404

        except Exception as e:
            return "Failed" + str(e), 500




