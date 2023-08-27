from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('votecourse', description='Vote Course related operations')

retrieve_all_votecourses = api.parser()
retrieve_all_votecourses.add_argument("course_id", help="Enter course id")
@api.route("/get_all_votecourses")
@api.doc(description="Get all vote courses")
class GetAllVoteCourses(Resource):
  @api.expect(retrieve_all_votecourses)
  def get(self):
    arg = retrieve_all_votecourses.parse_args().get("course_id")
    course_id = arg if arg else ""
    if course_id == "":
      voteCourseList = VoteCourse.query.filter(VoteCourse.course_ID.contains(course_id)).distinct().all()
    else:
      voteCourseList = VoteCourse.query.filter(VoteCourse.course_ID.like(course_id)).distinct().all()
    
    db.session.close()
    if len(voteCourseList):
      return jsonify(
        {
          "code": 200,
          "data": {
            "course": [votecourse.json() for votecourse in voteCourseList]
          }
        }
      )
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))
  
retrieve_vote_count = api.parser()
retrieve_vote_count.add_argument("course_id", help="Enter course id")
@api.route("/retrieve_vote_count")
@api.doc(description="Get Course Vote Count")
class RetrieveVoteCount(Resource):
  @api.expect(retrieve_vote_count)
  def get(self):
    arg = retrieve_vote_count.parse_args().get("course_id")
    course_id = arg if arg else ""
    vote_count = VoteCourse.query.filter(VoteCourse.course_ID.contains(course_id)).count()

    db.session.close()
    if vote_count:
      return jsonify(
        {
          "code": 200,
          "data": {
            "vote_count": vote_count
          }
        }
      )
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))
