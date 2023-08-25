from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('runcourse', description='Run Course related operations')

# ==================== Run COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

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
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in runCourseList]
                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course"}, default=str)), 404

