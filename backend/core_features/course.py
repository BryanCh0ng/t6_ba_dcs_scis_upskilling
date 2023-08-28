from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_  
from datetime import datetime
import logging
app.logger.setLevel(logging.DEBUG)

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
		return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

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
		return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

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
		return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

delete_course = api.parser()
delete_course.add_argument("course_id", help="Enter course id")
@api.route("/delete_course")
@api.doc(description="Delete course")
class DeleteCourse(Resource):
    @api.expect(delete_course)
    def delete(self):    
        try:
            courseID = delete_course.parse_args().get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()            
            if(course):
                    try:
                        db.session.delete(course)              
                        db.session.commit()                 
                        return json.loads(json.dumps({"message":"Course successfully deleted"})), 200
                    except Exception as e:
                        return "Foreign key dependencies exist, cannot delete. " + str(e), 408

            return json.loads(json.dumps({"Message": "There is no such course"}, default=str)), 404



        except Exception as e:
            return "Failed. " + str(e), 500
        
delete_runcourse = api.parser()
delete_runcourse.add_argument("course_id", help="Enter course id")
@api.route("/delete_runcourse")
@api.doc(description="Delete run course")
class DeleteCourse(Resource):
    @api.expect(delete_runcourse)
    def delete(self):    
        try:
            courseID = delete_runcourse.parse_args().get("course_id")
            
            runCourse = RunCourse.query.filter_by(course_ID=courseID).first()            
            if(runCourse):
                    try:
                        db.session.delete(runCourse)              
                        db.session.commit()                 
                        return json.loads(json.dumps({"message":"Run Course has successfully deleted"})), 200
                    except Exception as e:
                        return "Foreign key dependencies exist, cannot delete. " + str(e), 408

            return json.loads(json.dumps({"Message": "There is no such run course"}, default=str)), 404



        except Exception as e:
            return "Failed. " + str(e), 500


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
           return jsonify(
							{
							"code": 200,
							"data": {
								"course": [course.json()]
							}
						}
					)

        return json.loads(json.dumps({"message": "There is no such course"})), 404


create_course_model = api.model("create_course_model", {
    "course_ID" : fields.Integer(description="Course ID", required=True),
    "course_Name" : fields.String(description="Course Name", required=True),
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



# Student - Courses Available for Registration (Ongoing) with Filters
retrieve_unregistered_active_courses_filter = api.parser()
retrieve_unregistered_active_courses_filter.add_argument("user_id", type=int, help="Enter user ID")
retrieve_unregistered_active_courses_filter.add_argument("course_name", help="Enter course name")
retrieve_unregistered_active_courses_filter.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_unregistered_active_courses")
@api.doc(description="Get unregistered active course information")
class GetUnregisteredActiveCourses(Resource):
    @api.expect(retrieve_unregistered_active_courses_filter)
    def get(self):
        args = retrieve_unregistered_active_courses_filter.parse_args()
        user_ID = args.get("user_id")

        app.logger.debug(user_ID)

        # Get the courses that the user has already registered for
        registered_course_ids = db.session.query(Registration.rcourse_ID).filter_by(user_ID=user_ID).subquery()

        # Construct the query for unregistered courses with active course status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~RunCourse.rcourse_ID.in_(registered_course_ids),
            RunCourse.course_Status == "active"
        )

        # Apply additional filters based on user inputs
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Student - Courses Available for Voting (Active) with Filters
retrieve_unvoted_ongoing_courses_filter = api.parser()
retrieve_unvoted_ongoing_courses_filter.add_argument("user_id", type=int, help="Enter user ID")
retrieve_unvoted_ongoing_courses_filter.add_argument("course_name", help="Enter course name")
retrieve_unvoted_ongoing_courses_filter.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_unvoted_ongoing_courses")
@api.doc(description="Get unvoted ongoing course information")
class GetUnvotedOngoingCourses(Resource):
    @api.expect(retrieve_unvoted_ongoing_courses_filter)
    def get(self):
        args = retrieve_unvoted_ongoing_courses_filter.parse_args()
        user_ID = args.get("user_id", "")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")


        app.logger.debug(user_ID)

        # Get the courses that the user has already voted for
        voted_course_ids = db.session.query(Interest.vote_ID).filter_by(user_ID=user_ID).subquery()

        # Construct the query for unvoted courses with ongoing vote status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~VoteCourse.vote_ID.in_(voted_course_ids),
            VoteCourse.vote_Status == "ongoing"
        )

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})



# Student Registration Search - course name, course cat, status
retrieve_registration_info_filter_search = api.parser()
retrieve_registration_info_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_registration_info_filter_search.add_argument("course_name", help="Enter course name")
retrieve_registration_info_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_registration_info_filter_search.add_argument("reg_status", help="Enter registration status")

@api.route("/get_course_registration_info_filter_search")
@api.doc(description="Get course registration information")
class GetCourseRegistrationInfo(Resource):
    @api.expect(retrieve_registration_info_filter_search)
    def get(self):
        args = retrieve_registration_info_filter_search.parse_args()
        user_ID = args.get("user_id")
        # user_id = session.get("user_id")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")
        reg_Status = args.get("reg_status", "")

        app.logger.debug(reg_Status)

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            Registration
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)

        if user_ID:
            query = query.filter(Registration.user_ID == user_ID)
        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)
        if reg_Status:
            query = query.filter(Registration.reg_Status == reg_Status)
        
        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    **result[3].json()
                }
                result_data.append(course_info)
            app.logger.debug("Debug message")
            # app.logger.debug(result_data)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No matching course registration information found"})

# Student - Vote - course name, course cat, status
retrieve_vote_info_filter_search = api.parser()
retrieve_vote_info_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_vote_info_filter_search.add_argument("course_name", help="Enter course name")
retrieve_vote_info_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_vote_info_filter_search.add_argument("vote_status", help="Enter vote status")

@api.route("/get_course_vote_info_filter_search")
@api.doc(description="Get course interest information")
class GetCourseInterestInfo(Resource):
    @api.expect(retrieve_vote_info_filter_search)
    def get(self):
        args = retrieve_vote_info_filter_search.parse_args()
        user_ID = args.get("user_id")
        # user_id = session.get("user_id")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")
        vote_Status = args.get("vote_status", "")

        app.logger.debug(user_ID)

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            Interest, VoteCourse.vote_ID == Interest.vote_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)

        if user_ID:
            query = query.filter(Interest.user_ID == user_ID)
        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)
        if vote_Status:
            query = query.filter(VoteCourse.vote_Status == vote_Status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No matching course interest information found"})



# Student/Instructor/Trainer - Proposed - course name, course cat, status
retrieve_proposed_courses_filter_search = api.parser()
retrieve_proposed_courses_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_proposed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_proposed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_proposed_courses_filter_search.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_proposed_courses_filter_search")
@api.doc(description="Get proposed courses submitted by a user")
class GetProposedCourses(Resource):
    @api.expect(retrieve_proposed_courses_filter_search)
    def get(self):
        args = retrieve_proposed_courses_filter_search.parse_args()
        user_id = args.get("user_id")
        # user_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")
        
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            ProposedCourse
        ).select_from(ProposedCourse).join(Course, ProposedCourse.course_ID == Course.course_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)
        
        if user_id:
            query = query.filter(ProposedCourse.submitted_By == user_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)
        
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json()
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching proposed courses found"})



# Student - Completed - course name, cat
retrieve_completed_courses_filter_search = api.parser()
retrieve_completed_courses_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_completed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_completed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_completed_courses_filter_search")
@api.doc(description="Get courses completed by a user")
class GetCompletedCourses(Resource):
    @api.expect(retrieve_completed_courses_filter_search)
    def get(self):
        args = retrieve_completed_courses_filter_search.parse_args()
        user_id = args.get("user_id")
        # user_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        
        UserInstructor = aliased(User)
        UserStudent = aliased(User)

        query = db.session.query(
            Course,
            RunCourse,
            UserInstructor.user_Name.label("instructor_name"),
            UserInstructor.user_Email.label("instructor_email"),
        ).select_from(RunCourse).join(Course, RunCourse.course_ID == Course.course_ID) \
            .join(Registration, RunCourse.rcourse_ID == Registration.rcourse_ID) \
            .join(UserInstructor, RunCourse.instructor_ID == UserInstructor.user_ID) \
            .join(UserStudent, Registration.user_ID == UserStudent.user_ID) \
            .filter(UserStudent.user_ID == user_id) \
            .filter(Registration.reg_Status == 'Enrolled') \
            .filter(RunCourse.runcourse_Status == 'Closed') \
            .filter(RunCourse.course_Status == 'Inactive')

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[1].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[1].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[1].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[1].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[1].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[1].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[1].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[1].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[1].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    **modified_run_course,
                    "instructor_Name": result[2],
                    "instructor_Email": result[3]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No completed courses found"})

    

# Instructor/Trainer - Voting Campaign
retrieve_voting_campaign_courses_filter_search = api.parser()
retrieve_voting_campaign_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_voting_campaign_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_voting_campaign_courses_filter_search")
@api.doc(description="Get proposed courses")
class GetVotingCampaignCourses(Resource):
    @api.expect(retrieve_voting_campaign_courses_filter_search)
    def get(self):
        args = retrieve_voting_campaign_courses_filter_search.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        
        vote_counts_subquery = db.session.query(
            VoteCourse.course_ID,
            func.count(Interest.interest_ID).label("vote_count")
        ).join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
        .group_by(VoteCourse.course_ID).subquery()
        
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            vote_counts_subquery.c.vote_count
        ).select_from(Course) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .outerjoin(vote_counts_subquery, Course.course_ID == vote_counts_subquery.c.course_ID)
        
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        
        query = query.filter(vote_counts_subquery.c.vote_count > 0)
        query = query.group_by(Course.course_ID)
        
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_count": result[2]
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching courses found"})
        
# Instructor/Trainer - Assigned Course
retrieve_instructor_courses_filter_search = api.parser()
retrieve_instructor_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_instructor_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_instructor_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_instructor_courses_filter_search.add_argument("runcourse_status", help="Enter run course status")

@api.route("/get_instructor_assigned_courses_filter_search")
@api.doc(description="Get courses taught by an instructor with search options")
class GetInstructorCourses(Resource):
    @api.expect(retrieve_instructor_courses_filter_search)
    def get(self):
        args = retrieve_instructor_courses_filter_search.parse_args()
        instructor_id = args.get("instructor_id", "")
        # instructor_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("runcourse_status", "")

        UserInstructor = aliased(User)
        # RunCourseAlias = aliased(RunCourse)
        # CourseAlias = aliased(Course)
        # CourseCategoryAlias = aliased(CourseCategory)

        query = db.session.query(
            User.user_Name,
            User.user_Email,
            RunCourse,
            Course,
            CourseCategory.coursecat_Name
        ).select_from(User) \
        .join(UserInstructor, UserInstructor.user_ID == User.user_ID) \
        .join(RunCourse, RunCourse.instructor_ID == UserInstructor.user_ID) \
        .join(Course, Course.course_ID == RunCourse.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)

        if instructor_id:
            query = query.filter(UserInstructor.user_ID == instructor_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    "user_Name": result[0],
                    "user_Email": result[1],
                    **modified_run_course,
                    **result[3].json(),
                    "coursecat_Name": result[4]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found for the given criteria"})

# Instructor/Trainer - Proposed
retrieve_staff_proposed_courses_filter_search = api.parser()
retrieve_staff_proposed_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_staff_proposed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_staff_proposed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_staff_proposed_courses_filter_search.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_instructor_proposed_courses_filter_search")
@api.doc(description="Get proposed courses submitted by a user with vote count")
class GetProposedCoursesByUser(Resource):
    @api.expect(retrieve_staff_proposed_courses_filter_search)
    def get(self):
        args = retrieve_staff_proposed_courses_filter_search.parse_args()
        user_id = args.get("instructor_id", "")
        # user_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")

        vote_counts_subquery = db.session.query(
            VoteCourse.course_ID,
            func.count(Interest.interest_ID).label("vote_count")
        ).join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
        .group_by(VoteCourse.course_ID).subquery()
        
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            ProposedCourse,
            vote_counts_subquery.c.vote_count
        ).select_from(ProposedCourse).join(Course, ProposedCourse.course_ID == Course.course_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
            .outerjoin(vote_counts_subquery, Course.course_ID == vote_counts_subquery.c.course_ID)
        
        if user_id:
            query = query.filter(ProposedCourse.submitted_By == user_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)
        
        query = query.group_by(Course.course_ID, ProposedCourse.pcourse_ID)
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json(),
                    "vote_count": result[3]
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching proposed courses found"})

# Instructor/Trainer - Completed/Taught Courses
retrieve_instructor_taught_courses_filter_search = api.parser()
retrieve_instructor_taught_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_instructor_taught_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_instructor_taught_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_instructor_taught_courses_filter_search")
@api.doc(description="Get courses taught by an instructor with search options")
class GetInstructorTaughtCourses(Resource):
    @api.expect(retrieve_instructor_taught_courses_filter_search)
    def get(self):
        args = retrieve_instructor_taught_courses_filter_search.parse_args()
        instructor_id = args.get("instructor_id", "")
        # instructor_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")

        UserInstructor = aliased(User)
        current_time = datetime.now()  # Current time

        query = db.session.query(
            User.user_Name,
            User.user_Email,
            RunCourse,
            Course,
            CourseCategory.coursecat_Name
        ).select_from(User) \
        .join(UserInstructor, UserInstructor.user_ID == User.user_ID) \
        .join(RunCourse, RunCourse.instructor_ID == UserInstructor.user_ID) \
        .join(Course, Course.course_ID == RunCourse.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)

        if instructor_id:
            query = query.filter(UserInstructor.user_ID == instructor_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)

        # Filter out courses that have ended
        query = query.filter(RunCourse.run_Endtime <= current_time)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    "user_Name": result[0],
                    "user_Email": result[1],
                    **modified_run_course,
                    **result[3].json(),
                    "coursecat_Name": result[1]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No ended courses found for the given criteria"})

# Admin - All Proposal - Submitted
retrieve_all_submitted_proposed_courses_admin = api.parser()
retrieve_all_submitted_proposed_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_submitted_proposed_courses_admin.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_all_submitted_proposed_courses_admin")
@api.doc(description="Get all proposed courses (Admin)")
class GetAllProposedCoursesAdmin(Resource):
    @api.expect(retrieve_all_submitted_proposed_courses_admin)
    def get(self):
        args = retrieve_all_submitted_proposed_courses_admin.parse_args()
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")

        app.logger.debug(coursecat_ID)

        query = db.session.query(
            ProposedCourse,
            User.user_Name.label("submitted_by_name"),
            Course,
            CourseCategory.coursecat_Name
        ).select_from(ProposedCourse) \
        .join(User, ProposedCourse.submitted_By == User.user_ID) \
        .join(Course, ProposedCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(ProposedCourse.pcourse_Status != "Approved") \
        .filter(ProposedCourse.pcourse_Status != "Rejected")

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)

        results = query.all()
        db.session.close()

        app.logger.debug(results)

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "submitted_by": result[1],
                    **result[2].json(),
                    "coursecat_Name": result[3]
                }
               
                result_data.append(course_info)
                

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No proposed courses found"})
    

# Admin- All Proposal - Approved/Rejected
retrieve_all_app_rej_proposed_courses_admin = api.parser()
retrieve_all_app_rej_proposed_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_app_rej_proposed_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_app_rej_proposed_courses_admin.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_all_app_reg_proposed_courses_admin")
@api.doc(description="Get all proposed courses (Admin)")
class GetAllProposedCoursesAdmin(Resource):
    @api.expect(retrieve_all_app_rej_proposed_courses_admin)
    def get(self):
        args = retrieve_all_app_rej_proposed_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")

        app.logger.debug(pcourse_status)

        query = db.session.query(
            ProposedCourse,
            User.user_Name.label("submitted_by_name"),
            Course,
            CourseCategory.coursecat_Name
        ).select_from(ProposedCourse) \
        .join(User, ProposedCourse.submitted_By == User.user_ID) \
        .join(Course, ProposedCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(
            (ProposedCourse.pcourse_Status == "Approved") |
            (ProposedCourse.pcourse_Status == "Rejected")
        )

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                proposed_course_info = {
                    **result[0].json(),
                    "submitted_by_name": result[1],
                    **result[2].json(),
                    "coursecat_Name": result[3]
                }
                app.logger.debug(proposed_course_info)
                result_data.append(proposed_course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No proposed courses found"})
    
#  Admin - All Voting Campaign
retrieve_all_voting_courses_admin = api.parser()
retrieve_all_voting_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_voting_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_voting_courses_admin.add_argument("vote_status", help="Enter vote status")

@api.route("/get_all_voting_courses_admin")
@api.doc(description="Get all voting courses (Admin)")
class GetAllVotingCoursesAdmin(Resource):
    @api.expect(retrieve_all_voting_courses_admin)
    def get(self):
        args = retrieve_all_voting_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        vote_status = args.get("vote_status", "")

        vote_counts_subquery = db.session.query(
            VoteCourse.course_ID,
            func.count(Interest.interest_ID).label("vote_count")
        ).join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
        .group_by(VoteCourse.course_ID).subquery()

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status,
            vote_counts_subquery.c.vote_count
        ).select_from(VoteCourse) \
        .join(Course, VoteCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .outerjoin(vote_counts_subquery, Course.course_ID == vote_counts_subquery.c.course_ID)

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if vote_status:
            query = query.filter(VoteCourse.vote_Status == vote_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2],
                    "vote_count": result[3]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No voting courses found"})

# Admin - All Courses - All those in runcourse table with Reg Count
retrieve_all_courses_admin = api.parser()
retrieve_all_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_courses_admin.add_argument("course_status", help="Enter run course status")

@api.route("/get_all_courses_with_registration_count")
@api.doc(description="Get all courses with registration count")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_courses_admin)
    def get(self):
        args = retrieve_all_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        course_status = args.get("course_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            func.coalesce(func.count(Registration.reg_ID), 0).label("registration_count")
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).outerjoin(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID).group_by(Course.course_ID, RunCourse.rcourse_ID)

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if course_status:
            query = query.filter(RunCourse.course_Status == course_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    "registration_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Admin - All Instructors
retrieve_instructors_trainers = api.parser()
retrieve_instructors_trainers.add_argument("instructor_name", help="Enter instructor name")
retrieve_instructors_trainers.add_argument("role_name", help="Enter role name")
retrieve_instructors_trainers.add_argument("organization_name", help="Enter organization")

@api.route("/get_all_instructors_and_trainers")
@api.doc(description="Get all instructors and trainers with organization names")
class GetAllInstructorsAndTrainers(Resource):
    @api.expect(retrieve_instructors_trainers)
    def get(self):
        args = retrieve_instructors_trainers.parse_args()
        instructor_name = args.get("instructor_name", "")
        role_name = args.get("role_name")
        organization_name = args.get("organization_name", "")

        query = db.session.query(
            User.user_ID,
            User.user_Name,
            User.user_Email,
            db.func.ifnull(ExternalUser.organisation_Name, "SMU").label("organisation_Name"),
            User.role_Name,
        ).select_from(User).outerjoin(ExternalUser, User.user_ID == ExternalUser.user_ID)

        # Add filtering for "Instructor" or "Trainer" roles
        query = query.filter(User.role_Name.in_(["Instructor", "Trainer"]))

        if organization_name == "SMU":
            query = query.filter(ExternalUser.organisation_Name.is_(None))
        elif organization_name:
            query = query.filter(ExternalUser.organisation_Name.like(f"%{organization_name}%"))
            
        if instructor_name:
            query = query.filter(User.user_Name.contains(instructor_name))
        
        if role_name:
            query = query.filter(User.role_Name == role_name)
        
        results = query.all()

        if results:
            result_data = []
            for result in results:
                instructor_trainer_info = {
                    "user_ID": result[0],
                    "user_Name": result[1],
                    "user_Email": result[2],
                    "organisation_Name": result[3],
                    "role_Name": result[4]
                }

                result_data.append(instructor_trainer_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No instructors or trainers found"})


# Admin - Get All Run Course
retrieve_all_run_courses_admin = api.parser()
retrieve_all_run_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_run_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_run_courses_admin.add_argument("course_status", help="Enter run course status")

@api.route("/get_all_run_courses")
@api.doc(description="Get all run courses")
class GetAllCourses(Resource):
    @api.expect(retrieve_all_run_courses_admin)
    def get(self):
        args = retrieve_all_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        course_status = args.get("course_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        )

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if course_status:
            query = query.filter(RunCourse.course_Status == course_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})
    

# Cancel/Deactivate Button in adminViewRunCourse
deactivate_runcourse = api.parser()
deactivate_runcourse.add_argument("course_id", help="Enter course id")
@api.route("/deactivate_runcourse")
@api.doc(description="Cancel or deactivate a run course")
class DeactivateCourse(Resource):
    @api.expect(deactivate_runcourse)
    def post(self):
        try:
            args = deactivate_runcourse.parse_args()
            courseID = args.get("course_id")
            
            runCourse = RunCourse.query.filter_by(course_ID=courseID).first()
            
            if runCourse:
                if runCourse.course_Status == 'Active':
                    if runCourse.runcourse_Status == 'Ongoing':
                        # Update the course and registration status
                        runCourse.course_Status = 'Inactive'
                        runCourse.runcourse_Status = 'Closed'
                    elif runCourse.runcourse_Status == 'Closed':
                        # Update only the course status
                        runCourse.course_Status = 'Inactive'
                    db.session.commit()

                    return jsonify({"code": 200, "message": "Run Course has been canceled or deactivated"})
 
                else:
                    return jsonify({"code": 400, "message": "Course is not active, cannot be canceled"})
            else:
                return json.loads(json.dumps({"message": "Course is not active, cannot be canceled"})), 404

        except Exception as e:
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500


# Retire button in the adminViewRunCourse 
# when course_Status = Inactive and runcourse_Status = Closed, changed the course_Status to Retired
retire_course = api.parser()
retire_course.add_argument("course_id", help="Enter course id")
@api.route("/retire_course")
@api.doc(description="Retire a course")
class RetireCourse(Resource):
    @api.expect(retire_course)
    def post(self):
        try:
            args = retire_course.parse_args()
            courseID = args.get("course_id")
            
            runCourse = RunCourse.query.filter_by(course_ID=courseID).first()
            
            if runCourse:
                if runCourse.course_Status == 'Inactive' and runCourse.runcourse_Status == 'Closed':
                    runCourse.course_Status = 'Retired'
                    db.session.commit()
                    return jsonify({"code": 200, "message": "Course has been retired"})
                else:
                    return jsonify({"code": 400, "message": "Course cannot be retired"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            return jsonify({"message": "Failed. " + str(e)}), 500


# Activate button in adminviewruncourse
activate_course = api.parser()
activate_course.add_argument("course_id", help="Enter course id")
@api.route("/activate_course")
@api.doc(description="Activate a course")
class ActivateCourse(Resource):
    @api.expect(activate_course)
    def post(self):
        try:
            args = activate_course.parse_args()
            courseID = args.get("course_id")
            
            runCourse = RunCourse.query.filter_by(course_ID=courseID).first()
            
            if runCourse:
                if runCourse.course_Status == 'Inactive' and runCourse.runcourse_Status == 'Closed':
                    runCourse.course_Status = 'Active'
                    db.session.commit()
                    return jsonify({"code": 200, "message": "Course has been activated"})
                else:
                    return jsonify({"code": 400, "message": "Course cannot be activated"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            return jsonify({"code": 500, "message": "Failed. " + str(e)})