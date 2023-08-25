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
