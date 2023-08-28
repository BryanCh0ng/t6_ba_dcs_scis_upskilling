from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('course', description='Course related operations')

# ==================== COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

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


create_course_model = api.model("create_course_model", {
    "course_ID" : fields.Integer(description="Course ID", required=True),
    "cousre_Name" : fields.String(description="Course Name", required=True),
    "course_Desc" : fields.String(description="Course Description", required=True),
    "coursecat_ID" : fields.Integer(description="Course Category ID", required=True)
})

# @api.route("/create_new_course", methods=["POST"])
# @api.doc(description="Create new course. This is used for testing only. Records will come from LMS in a .csv format")
# class CreateNewCourses(Resource):
#     @api.expect(create_course_model)
#     def post(self):
#         data = request.get_json()
#         newCourse = Course(**data)

#         try:
#             courseID = data["course_ID"]
#             if(Course.query.filter_by(course_ID=courseID).first()):
#                 return json.loads(json.dumps({"Message": "Course ID already exist"}, default=str)), 400

#             db.session.add(newCourse)
#             db.session.commit()
#             return json.loads(json.dumps(newCourse.json(), default=str)), 200

#         except Exception as e:
#             return "Failed" + str(e), 500





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



