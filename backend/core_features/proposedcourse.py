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
    if course_id == "":
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.course_ID.contains(course_id)).all()
    else:
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
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

retrieve_proposed_course = api.parser()
retrieve_proposed_course.add_argument("course_id", help="Enter course id")
@api.route("/get_proposed_course_by_course_id")
@api.doc(description="Get proposed course by course id")
class GetProposedCourse(Resource):
  @api.expect(retrieve_proposed_course)
  def get(self):
    courseID = retrieve_proposed_course.parse_args().get("course_id")
    course = ProposedCourse.query.filter_by(course_ID=courseID).first()
    db.session.close()
    if course:
      return jsonify(
      {
        "code": 200,
        "data": {
          "course": [course.json()]
        }
      }
    )
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))
  
retrieve_proposed_course_by_status = api.parser()
retrieve_proposed_course_by_status.add_argument("pcourse_status", help="Enter pcourse_status")
@api.route("/get_proposed_course_by_pcourse_status")
@api.doc(description="Get proposed course by pcourse status")
class GetProposedCourseByStatus(Resource):
  @api.expect(retrieve_proposed_course_by_status)
  def get(self):
    arg = retrieve_proposed_course_by_status.parse_args().get("pcourse_status")
    pcourse_status = arg if arg else ""
    if pcourse_status == "":
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.pcourse_Status.contains(pcourse_status)).all()
    else:
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.pcourse_Status.like(pcourse_status)).all()
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
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

@api.route("/create_proposed_course", methods=["POST"])
@api.doc(description="Create proposed course")
class CreateNewProposedCourse(Resource):
    def post(self):
        try: 
            # Get the data for creating a new course from the request body
            new_proposed_course_data = request.json

            # Create a new course object with the data
            new_proposed_course = ProposedCourse(None, submitted_By=new_proposed_course_data.get("submitted_By"), action_Done_By=None, course_ID=new_proposed_course_data.get("course_ID"), pcourse_Status="Pending", reason=None)

            # Add the new course to the database
            db.session.add(new_proposed_course)

            # Commit the changes to the database
            db.session.commit()

            # Inside the create_proposed_course route
            #print("Data before returning:", new_proposed_course.json())

            # Return the newly created course as JSON response
            return json.loads(json.dumps(new_proposed_course.json(), default=str)), 201

        except Exception as e:
            print("Error:", str(e))
            return "Failed to create a new course: " + str(e), 500