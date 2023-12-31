from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from core_features import common
from allClasses import *
import json
from sqlalchemy import func, and_, exists, not_, select
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
            db.session.close()

            response_data = {
                "course_ID": course.course_ID,
                "course_Name": course.course_Name,
                "course_Desc": course.course_Desc,
                "coursecat_ID": course.coursecat_ID,
                "coursecat_Name": course_category.coursecat_Name,
                "pcourse_ID": proposed_course.pcourse_ID
            }
            
            return jsonify(
                {
                    "code": 200,
                    "data": response_data
                }
            )

        db.session.close()
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

@api.route("/create_proposed_course", methods=["POST"])
@api.doc(description="Create proposed course")
class CreateProposedCourse(Resource):
    def post(self):
        try: 
            # Get the data for creating a new proposed course from the request body
            new_proposed_course_data = request.json

            # Create a new proposed course object with the data
            new_proposed_course = ProposedCourse(None, submitted_By=new_proposed_course_data.get("submitted_By"), course_ID=new_proposed_course_data.get("course_ID"), pcourse_Status="Pending", action_Done_By=None, proposed_Date=new_proposed_course_data.get("proposed_Date"), reason=None, voteCount=0)

            # Add the new proposed course to the database
            db.session.add(new_proposed_course)

            # Commit the changes to the database
            db.session.commit()

            new_proposed_course.proposed_Date = new_proposed_course.proposed_Date.strftime('%Y-%m-%d')

            return {
              "message": "Proposed Course created successfully",
              "data": new_proposed_course.json()
            }, 201

        except Exception as e:
          db.session.rollback()
          #return "Failed to create a new course: " + str(e), 500
          return {
            "message": "Failed to create a propsed course: " + str(e)
          }, 500

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
            data = request.get_json()
            course_name = data.get('course_Name')
            course_desc = data.get('course_Desc')
            coursecat_ID = data.get('coursecat_ID')

            course = Course.query.get(course_id)
            user_id = common.getUserID()
            user_role = common.getUserRole()
            proposed_course = ProposedCourse.query.filter_by(course_ID=course_id).first()
            
            if user_id != proposed_course.submitted_By and user_role != "Admin":
                return jsonify({"message": "Unauthorized Access, no rights to edit proposed course", "code": 403})

            if course is None:
                return jsonify({"message": "Proposed course not found", "code": 404}), 404

            existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(course_name)).first()

            if existing_course and course_name != course.course_Name:
                return jsonify({"message": "Course Update Unsuccessful. A course with the same name already exists.", "code": 405})
            
            
            result_data = {
               'course_Name': course_name,
               'course_Desc': course_desc,
               'coursecat_ID': coursecat_ID
            }
            result = Course.query.filter_by(course_ID=course_id).update(result_data)
           

            db.session.commit()
            db.session.close()

            return jsonify({"message": "Proposed course updated successfully", "code": 200})

        except Exception as e:
            db.session.rollback()
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

            # app.logger.debug(pcourse_id)

            # Find the proposed course by its ID.
            proposed_course = ProposedCourse.query.get(pcourse_id)
            user_id = common.getUserID()
            if (user_id) != proposed_course.submitted_By:
                return {"message": "Unathorized Access, Not owner of this proposed those"}, 404 

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
              db.session.close()

            return {"message": "Proposed course deleted successfully"}

        except Exception as e:
            db.session.rollback()
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
      user_role = common.getUserRole()
      user_id = common.getUserID()
      if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to reject proposed course"}, 404 

      data = request.get_json()
      proposed_course = ProposedCourse.query.filter_by(pcourse_ID = data['pcourseID']).first()
      if proposed_course:
        proposed_course.pcourse_Status = 'Rejected'
        proposed_course.reason = data['reason']
        proposed_course.action_Done_By = user_id
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Proposed Course is successfully rejected", "code": 200})
  
      else:
        return jsonify({"message": "Course does not exist", "code": 404})

    except Exception as e:
      db.session.rollback()
      return jsonify({"message": "Failed " + str(e), "code": 500})
    

approve_proposed_course_model = api.model("accept_proposed_course_model", {
    "pcourseID" : fields.Integer(description="", required=True),
})
@api.route('/approve_proposed_course', methods=["POST"])
@api.doc(description="Approve Proposed Course")
class ApproveProposedCourse(Resource):
  @api.expect(approve_proposed_course_model)
  def post(self):
    try:
      user_role = common.getUserRole()
      if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to approve proposed course"}, 404 

      data = request.get_json()
      proposed_course = ProposedCourse.query.filter_by(pcourse_ID = data['pcourseID']).first()

      if proposed_course:
        proposed_course.pcourse_Status = 'Approved'
        newVoteCourse = VoteCourse(
          course_ID= proposed_course.course_ID,
          vote_Status='Ongoing'
        )
        db.session.add(newVoteCourse)
        db.session.commit()
        db.session.close()
      
        return jsonify({"message": "Proposed Course is successfully accepted", "code": 200})
  
      else:
        return jsonify({"message": "Course does not exist", "code": 404})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed " + str(e), "code": 500})
