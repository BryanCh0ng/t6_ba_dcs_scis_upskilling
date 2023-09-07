from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json
import logging
app.logger.setLevel(logging.DEBUG)

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
        proposed_course = ProposedCourse.query.filter_by(course_ID=courseID).first()
        if proposed_course:
            course = Course.query.get(proposed_course.course_ID)
            course_category = CourseCategory.query.get(course.coursecat_ID)
            
            response_data = {
                "course_ID": course.course_ID,
                "course_Name": course.course_Name,
                "course_Desc": course.course_Desc,
                "coursecat_ID": course.coursecat_ID,
                "coursecat_Name": course_category.coursecat_Name
            }
            
            return jsonify(
                {
                    "code": 200,
                    "data": response_data
                }
            )
        return jsonify({"message": "There is no such course", "code": 404})
  
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

# Edit/Update Proposed Course 
update_proposed_course_model = {
    "course_Name": fields.String(description="Course Name", required=True),
    "course_Desc": fields.String(description="Course Description", required=True),
    "coursecat_ID": fields.Integer(description="Course Category ID", required=True),
}

@api.route('/update_proposed_course/<int:course_id>', methods=['PUT'])
@api.doc(description="Update Proposed Course")
class UpdateProposedCourse(Resource):
    @api.expect(update_proposed_course_model)
    def put(self, course_id):
        try:
            # app.logger.debug(course_id)

            data = request.get_json()
            # app.logger.debug(data)
            course_name = data.get('course_Name')
            course_desc = data.get('course_Desc')
            coursecat_ID = data.get('coursecat_ID')

            course = Course.query.get(course_id)

            if course is None:
                return jsonify({"message": "Proposed course not found", "code": 404}), 404

            course.course_Name = course_name
            course.course_Desc = course_desc
            course.coursecat_ID = coursecat_ID

            db.session.commit()

            return jsonify({"message": "Proposed course updated successfully", "code": 200})

        except Exception as e:
            return jsonify({"message": f"Failed to update proposed course: {str(e)}", "code": 500})
        

# Delete Propose Course
delete_proposed_course = api.parser()
delete_proposed_course.add_argument("pcourse_ID", help="Proposed Course ID")

@api.route('/delete_proposed_course')
@api.doc(description="Delete Proposed Course")
class RemoveProposedCourse(Resource):
    @api.expect(delete_proposed_course)
    def delete(self):
        try:
            args = delete_proposed_course.parse_args()
            pcourse_id = args.get("pcourse_ID")

            app.logger.debug(pcourse_id)

            # Find the proposed course by its ID.
            proposed_course = ProposedCourse.query.get(pcourse_id)

            if proposed_course is None:
                return {"message": "Proposed course not found"}, 404

            # Get the associated course ID.
            course_id = proposed_course.course_ID

            # Delete the proposed course.
            db.session.delete(proposed_course)
            db.session.commit()

            # Now, delete the corresponding course if it exists.
            course = Course.query.get(course_id)
            if course is not None:
                db.session.delete(course)
                db.session.commit()

            return {"message": "Proposed course deleted successfully"}

        except Exception as e:
            return {"message": "Failed to delete proposed course: " + str(e)}, 500


reject_proposed_course_model = api.model("reject_proposed_course_model", {
    "pcourseID" : fields.Integer(description="", required=True),
    "reason" : fields.String(description="", required=True)
})
@api.route('/reject_proposed_course', methods=["POST"])
@api.doc(description="Reject Proposed Course")
class RejectProposedCourse(Resource):
  @api.expect(reject_proposed_course_model)
  def post(self):
    try:
      data = request.get_json()
      proposed_course = ProposedCourse.query.filter_by(pcourse_ID = data['pcourseID'], pcourse_Status='Pending').first()
      if proposed_course:
        proposed_course.pcourse_Status = 'Rejected'
        proposed_course.reason = data['reason']
        db.session.commit()
        return jsonify({"message": "Proposed Course is successfully rejected", "code": 200})
  
      else:
        return jsonify({"message": "Course does not exist or is not of Pending status", "code": 404})

    except Exception as e:
      return jsonify({"message": "Failed " + str(e), "code": 500})

