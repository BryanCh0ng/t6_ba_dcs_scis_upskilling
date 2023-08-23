from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('proposedcourse', description='Proposed Course related operations')

# ==================== PROPOSED COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

retrieve_all_proposedcourses = api.parser()
retrieve_all_proposedcourses.add_argument("course_id", help="Enter course id")
@api.route("/get_all_proposedcourses")
@api.doc(description="Get all proposed courses")
class GetAllProposedCourses(Resource):
    @api.expect(retrieve_all_proposedcourses)
    def get(self):
        arg = retrieve_all_proposedcourses.parse_args().get("course_id")
        course_id = arg if arg else ""
        proposedCourseList = ProposedCourse.query.filter(ProposedCourse.course_ID.like(course_id)).all()
        db.session.close()
        if len(proposedCourseList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in proposedCourseList]
                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course"}, default=str)), 404

