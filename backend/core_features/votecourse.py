from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
from datetime import datetime
import logging
app.logger.setLevel(logging.DEBUG)

api = Namespace('votecourse', description='Vote Course related operations')

promote_to_course_model = api.model("promote_to_course_model", {
    "vote_id" : fields.Integer(description="", required=True),
})
@api.route('/promote_to_course', methods=["POST"])
@api.doc(description="Promote To Course")
class PromoteToCourse(Resource):
  @api.expect(promote_to_course_model)
  def post(self):
    try:
      data = request.get_json()
      print(data)
      vote_course = VoteCourse.query.filter_by(vote_ID = data['vote_id']).first()

      if vote_course:
        vote_course.vote_Status = 'Offered'
        newRunCourse = RunCourse(
          run_Startdate=None,
          run_Enddate=None,
          run_Starttime=None,
          run_Endtime=None,
          instructor_ID=None,
          course_Format=None,
          course_Venue=None,
          runcourse_Status=None,
          course_Size=None,
          course_Minsize=None,
          course_Fee=None,
          class_Duration=None,
          reg_Startdate=None,
          reg_Enddate=None,
          reg_Starttime=None,
          reg_Endtime=None,
          template_ID=None,
          course_ID= vote_course.course_ID,
          course_Status='Active'
        )
        db.session.add(newRunCourse)
        db.session.commit()
        return jsonify({"message": "Vote Course is successfully offered", "code": 200})
      else:
        return jsonify({"message": "Course does not exist", "code": 404})
    except Exception as e:
        return jsonify({"message": "Failed " + str(e), "code": 500})

retrieve_vote_course = api.parser()
retrieve_vote_course.add_argument("course_id", help="Enter course id")
@api.route("/get_vote_course_by_course_id")
@api.doc(description="Get vote course by course id")
class GetVoteCourse(Resource):
    @api.expect(retrieve_vote_course)
    def get(self):
        courseID = retrieve_vote_course.parse_args().get("course_id")
        vote_course = VoteCourse.query.filter_by(course_ID=courseID).first()
        if vote_course:
            course = Course.query.get(vote_course.course_ID)
            course_category = CourseCategory.query.get(course.coursecat_ID)
            
            response_data = {
                "course_ID": course.course_ID,
                "course_Name": course.course_Name,
                "course_Desc": course.course_Desc,
                "coursecat_ID": course.coursecat_ID,
                "coursecat_Name": course_category.coursecat_Name,
                "vote_ID": vote_course.vote_ID
            }
            
            return jsonify(
                {
                    "code": 200,
                    "data": response_data
                }
            )
        return jsonify({"message": "There is no such course", "code": 404})