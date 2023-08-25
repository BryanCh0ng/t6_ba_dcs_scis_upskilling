from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('coursecat', description='Course category related operations')

# ==================== COURSE Category FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

retrieve_all_coursecat = api.parser()
retrieve_all_coursecat.add_argument("coursecat_name", help="Enter course category name")
@api.route("/get_all_coursecat")
@api.doc(description="Get all course categories")
class GetAllCoursecat(Resource):
  @api.expect(retrieve_all_coursecat)
  def get(self):
    arg = retrieve_all_coursecat.parse_args().get("coursecat_name")
    coursecat_Name = arg if arg else ""
    coursecatList = CourseCategory.query.filter(CourseCategory.coursecat_Name.contains(coursecat_Name)).all()
    db.session.close()
    if len(coursecatList):
      return jsonify(
        {
          "code": 200,
          "data": {
            "course": [coursecat.json() for coursecat in coursecatList]
          }
        }
      )

    return json.loads(json.dumps({"message": "There is no such course category"}, default=str)), 404


retrieve_coursecat = api.parser()
retrieve_coursecat.add_argument("coursecat_id", help="Enter course category id")
@api.route("/get_coursecat_by_id")
@api.doc(description="Get course category by course category id")
class GetCoursecat(Resource):
    @api.expect(retrieve_coursecat)
    def get(self):
        courseID = retrieve_coursecat.parse_args().get("coursecat_id")
        coursecat = CourseCategory.query.filter_by(coursecat_ID=courseID).first()
        db.session.close()
        if coursecat:
            return json.loads(json.dumps(coursecat.json())), 200

        return json.loads(json.dumps({"message": "There is no such course category", "code": 404}, default=str))

