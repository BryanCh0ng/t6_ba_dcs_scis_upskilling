from flask import request, jsonify, session
from core_features import common
from flask_restx import Namespace, Resource, fields, reqparse
from allClasses import *
import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists, not_, select
from datetime import datetime, date, time
import logging
app.logger.setLevel(logging.DEBUG)
import traceback

api = Namespace('course', description='Course related operations')

# ==================== COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

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
		arg = retrieve_all_courses_filter_search.parse_args().get("course_name")
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
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to delete course"}, 404 

            courseID = delete_course.parse_args().get("course_id")
            course = Course.query.filter_by(course_ID=courseID).first()
        
            if(course):
                    try:
                        db.session.delete(course)              
                        db.session.commit()
                        db.session.close()                 
                        return json.loads(json.dumps({"message":"Course successfully deleted"})), 200
                    except Exception as e:
                        return "Foreign key dependencies exist, cannot delete. " + str(e), 408

            return json.loads(json.dumps({"Message": "There is no such course"}, default=str)), 404
        except Exception as e:
            db.session.rollback()
            return "Failed. " + str(e), 500
        
delete_runcourse = api.parser()
delete_runcourse.add_argument("rcourse_ID", help="Enter run course id")
@api.route("/delete_runcourse")
@api.doc(description="Delete run course")
class DeleteCourse(Resource):
    @api.expect(delete_runcourse)
    def delete(self):    
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to delete run course"}, 404 

            rcourse_ID = delete_runcourse.parse_args().get("rcourse_ID")

            current_date = datetime.now().date()

            runCourse = RunCourse.query.filter_by(rcourse_ID=rcourse_ID).first()            
            if runCourse and runCourse.run_Startdate > current_date:
                    try:
                        lessons_to_delete = Lesson.query.filter_by(rcourse_ID=rcourse_ID).all()
                        for lesson in lessons_to_delete:
                            db.session.delete(lesson)

                        db.session.delete(runCourse)              
                        db.session.commit()
                        db.session.close()                 
                        return json.loads(json.dumps({"message":"Run Course and the associated lessons have been successfully deleted."})), 200
                    except Exception as e:
                        return json.loads(json.dumps({"message":"Run Course has unsuccessfully deleted"})), 408
                    

            return json.loads(json.dumps({"Message": "There is no such run course"}, default=str)), 404

        except Exception as e:
            db.session.rollback()
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

        return {"code": 404, "message": "There is no such course"}, 404

@api.route("/create_course", methods=["POST"])
@api.doc(description="Create course")
class CreateCourse(Resource):
    def post(self):
        try:
            # Get the data for creating a new course from the request body
            new_course_data = request.json
            
            new_course_name = new_course_data.get("course_Name") 

            # Assuming new_course_name is the input course name you want to check against the database
            input_course_name = new_course_name.strip()

            # Perform a case-insensitive search and remove leading/trailing spaces
            existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(input_course_name)).first()

            # Check if the course name already exists in the database
            #existing_course = Course.query.filter_by(course_Name=new_course_name).first()

            if existing_course:
                return {
                    "message": "Course name already exists"
                }, 409  # Conflict

            # Create a new course object with the data
            #new_course = Course(None, course_Name=new_course_name, course_Desc=new_course_data.get("course_Desc"), coursecat_ID=new_course_data.get("coursecat_ID"))
            new_course = Course(None, **new_course_data)

            # Add the new course to the database
            db.session.add(new_course)

            # Commit the changes to the database
            db.session.commit()

            # Return the newly created course as JSON response
            #return json.loads(json.dumps(new_course.json(), default=str)), 201
            return {
                'message': 'Course created successfully',
                'data': new_course.json()
            }, 201

        except Exception as e:
            db.session.rollback()
            #print("Error:", str(e))
            #return "Failed to create a new course: " + str(e), 500
            return {
                "message": "Failed to create a new course: " + str(e)
            }, 500

edit_course = api.parser()
@api.route("/edit_course/<int:course_id>", methods=["PUT"])
class EditCourse(Resource):
    @api.expect(edit_course)
    def put(self, course_id):

        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to edit course"
                }, 404 

            #Get the updated data from the request body 
            updated_data = request.json
            new_course_name = updated_data.get("course_Name") 
        
            course = Course.query.filter_by(course_ID=course_id).first()

            if course:
                # Assuming new_course_name is the input course name you want to check against the database
                input_course_name = new_course_name.strip()

                # Perform a case-insensitive search and remove leading/trailing spaces
                existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(input_course_name)).first()

                # Check if the course name already exists in the database
                #existing_course = Course.query.filter_by(course_Name=new_course_name).first()

                if existing_course and existing_course.course_ID != course_id:
                    return {
                        "message": "Course name already exists"
                    }, 409  # Conflict

                # Update the fields based on updated_data
                for field, value in updated_data.items():
                    
                    setattr(course, field, value)

                #Commit the changes to the database 
                db.session.commit()

                #return json.loads(json.dumps(course.json(), default=str)), 200
                return {
                    "message": "Course updated successfully",
                    "data": course.json()
                }, 200

            #return json.loads(json.dumps({"message": "There is no such course"})), 404
            return {
                "message": "There is no such course"
            }, 404

        except Exception as e:
            db.session.rollback()
            #return "Failed" + str(e), 500
            return {
                "message": "Failed to create a new course: " + str(e)
            }, 500

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

        current_datetime = datetime.now()
        current_time = current_datetime.strftime('%H:%M:%S')

        valid_reg_statuses = ["pending", "enrolled", "not enrolled"]

        registered_course_ids = db.session.query(Registration.rcourse_ID).filter(
            Registration.user_ID == user_ID,
            Registration.reg_Status.in_(valid_reg_statuses)
        ).subquery()

        # Construct the query for unregistered courses with active course status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~RunCourse.rcourse_ID.in_(select([registered_course_ids])),
            Course.course_Status == "active",
            RunCourse.runcourse_Status == "ongoing",
            RunCourse.reg_Enddate >= current_datetime.date(),
            (RunCourse.reg_Enddate > current_datetime.date()) | (RunCourse.reg_Endtime > current_time)
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
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),

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

        # app.logger.debug(user_ID)

        voted_course_ids = db.session.query(Interest.vote_ID).filter_by(user_ID=user_ID).subquery()

        # Construct the query for unvoted courses with ongoing vote status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~VoteCourse.vote_ID.in_(select([voted_course_ids])),
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
                    **result[2].json(),
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

        # app.logger.debug(reg_Status)

        current_datetime = datetime.now()

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            Registration
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)  \
            .filter(RunCourse.run_Enddate > current_datetime)

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
                    "feedback_Startdate": result[2].feedback_Startdate.strftime('%Y-%m-%d'),
                    "feedback_Enddate": result[2].feedback_Enddate.strftime('%Y-%m-%d'),
                    "feedback_Starttime": result[2].feedback_Starttime.strftime('%H:%M:%S'),
                    "feedback_Endtime": result[2].feedback_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    **result[3].json()
                }
                result_data.append(course_info)
            # app.logger.debug("Debug message")
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

        # app.logger.debug(user_ID)

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse
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
                    **result[2].json()
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
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        
        current_datetime = datetime.now()

        UserInstructor = aliased(User)
        UserStudent = aliased(User)

        query = db.session.query(
            Course,
            RunCourse,
            CourseCategory.coursecat_Name,
            UserInstructor.user_Name.label("instructor_name"),
            UserInstructor.user_Email.label("instructor_email"),
            Registration,
            exists().where(and_(
                Feedback.submitted_By == user_id,
                Feedback.rcourse_ID == RunCourse.rcourse_ID,
                Feedback.feedback_Template_ID == RunCourse.template_ID
            )).label("feedback_submitted")
        ).select_from(RunCourse).join(Course, RunCourse.course_ID == Course.course_ID) \
            .join(Registration, RunCourse.rcourse_ID == Registration.rcourse_ID) \
            .join(UserInstructor, RunCourse.instructor_ID == UserInstructor.user_ID) \
            .join(UserStudent, Registration.user_ID == UserStudent.user_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
            .filter(UserStudent.user_ID == user_id) \
            .filter(RunCourse.run_Enddate <= current_datetime) \
            .filter(Registration.reg_Status == "Enrolled")


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
                    'run_Startdate': common.format_date_time(result[1].run_Startdate),
                    'run_Enddate': common.format_date_time(result[1].run_Enddate),
                    'run_Starttime': common.format_date_time(result[1].run_Starttime),
                    'run_Endtime': common.format_date_time(result[1].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[1].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[1].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[1].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[1].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[1].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[1].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[1].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[1].feedback_Endtime)
                }

                modified_run_course = {**result[1].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    **modified_run_course,
                    "coursecat_Name": result[2],
                    "instructor_Name": result[3],
                    "instructor_Email": result[4],
                    **result[5].json(),
                    "feedback_submitted": result[6]
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

        current_datetime = datetime.now()

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
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(RunCourse.run_Enddate >= current_datetime)

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
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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
        
        query = query.group_by(Course.course_ID, ProposedCourse.pcourse_ID)
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

        current_datetime = datetime.now()

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
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(RunCourse.run_Enddate < current_datetime)

        if instructor_id:
            query = query.filter(UserInstructor.user_ID == instructor_id)
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
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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

        # app.logger.debug(coursecat_ID)

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
                # app.logger.debug(proposed_course_info)
                result_data.append(proposed_course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No proposed courses found"})
    
#  Admin - All Voting Campaign
retrieve_all_voting_campaign_courses_admin = api.parser()
retrieve_all_voting_campaign_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_voting_campaign_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_voting_campaign_courses_admin.add_argument("vote_status", help="Enter course category id")

@api.route("/get_all_voting_courses_admin")
@api.doc(description="Get all voting courses (Admin)")
class GetAllVotingCoursesAdmin(Resource):
    @api.expect(retrieve_all_voting_campaign_courses_admin)
    def get(self):
        args = retrieve_all_voting_campaign_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        vote_status = args.get("vote_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status,
            ProposedCourse
        ).select_from(VoteCourse) \
        .join(Course, VoteCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .join(ProposedCourse, Course.course_ID == ProposedCourse.course_ID) \
        .filter(
            (VoteCourse.vote_Status == "Offered") |
            (VoteCourse.vote_Status == "Closed") |
            (VoteCourse.vote_Status == "Ongoing")
        )
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
                    **result[3].json()
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No voting courses found"})
    
#  Admin - All Voting Campaign - Deleted
retrieve_all_voting_courses_admin = api.parser()
retrieve_all_voting_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_voting_courses_admin.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_all_not_offered_courses_admin")
@api.doc(description="Get all voting courses (Admin)")
class GetAllDeletedVotingCoursesAdmin(Resource):
    @api.expect(retrieve_all_voting_courses_admin)
    def get(self):
        args = retrieve_all_voting_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status,
            ProposedCourse
        ).select_from(VoteCourse) \
        .join(Course, VoteCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .join(ProposedCourse, Course.course_ID == ProposedCourse.course_ID) \
        .filter(VoteCourse.vote_Status == "Not Offered")

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2],
                    **result[3].json()
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
        runcourse_status = args.get("course_status", "")

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
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime)
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
    
retrieve_all_run_course_by_course_id_admin = api.parser()
retrieve_all_run_course_by_course_id_admin.add_argument("course_name", help="Enter course name")
retrieve_all_run_course_by_course_id_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_run_course_by_course_id_admin.add_argument("course_status", help="Enter run course status")
retrieve_all_run_course_by_course_id_admin.add_argument("course_id", help="Enter course id")
@api.route("/get_all_run_course_by_course_id")
@api.doc(description="Get all run course by course id")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_run_course_by_course_id_admin)
    def get(self):
        args = retrieve_all_run_course_by_course_id_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("course_status", "")
        course_id = args.get("course_id", "")

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
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)
        if course_id:
            query = query.filter(RunCourse.course_ID == course_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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

# Admin - Get All Course
retrieve_all_courses_admin = api.parser()
retrieve_all_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_courses_admin.add_argument("course_status", help="Enter run course status")

@api.route("/get_all_courses")
@api.doc(description="Get all run courses")
class GetAllCourses(Resource):
    @api.expect(retrieve_all_courses_admin)
    def get(self):
        args = retrieve_all_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        course_status = args.get("course_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
        ).select_from(Course).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        )

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if course_status:
            query = query.filter(Course.course_Status == course_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})
    

# Cancel/Deactivate Button in adminViewCourse
deactivate_course = api.parser()
deactivate_course.add_argument("course_id", help="Enter course id")
@api.route("/deactivate_course")
@api.doc(description="Cancel or deactivate a run course")
class DeactivateCourse(Resource):
    @api.expect(deactivate_course)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to deactivate course"}, 404 

            args = deactivate_course.parse_args()
            course_id = args.get("course_id")

            current_datetime = datetime.now()
            current_time = current_datetime.strftime('%H:%M:%S')
            
            # Query the database for the RunCourse with the specified course_id
            run_course = RunCourse.query.filter_by(course_ID=course_id).first()
            course = Course.query.filter_by(course_ID=course_id).first()
            
            if run_course:
                if course.course_Status == 'Active':
                    if run_course.runcourse_Status == 'Closed':
                        # Check if there are any ongoing run courses for this course ID and date
                        ongoing_classes = RunCourse.query.filter(
                            RunCourse.course_ID == course_id
                        ).filter(RunCourse.run_Startdate <= current_datetime.date(),
                            RunCourse.run_Enddate >= current_datetime.date(),
                            RunCourse.run_Endtime >= current_time).all()
                        
                        length_of_ongoing_classes = len(ongoing_classes)
                        # app.logger.debug(length_of_ongoing_classes)

                        
                        if length_of_ongoing_classes == 0:
                            # No ongoing run courses, update the course and registration status
                            course.course_Status = 'Inactive'
                            db.session.commit()
                            db.session.close()
                            return jsonify({"code": 200, "message": "Course has been canceled or deactivated"})
                        else:
                            db.session.close()
                            return jsonify({"code": 400, "message": "Cannot deactivate. There are ongoing classes."})
                    elif run_course.runcourse_Status == 'Ongoing':
                        # Update only the course status
                        course.course_Status = 'Inactive'
                        run_course.runcourse_Status = 'Closed'
                        db.session.commit()
                        db.session.close()

                        return jsonify({"code": 200, "message": "Course has been canceled or deactivated"})
                else:
                    db.session.close()
                    return jsonify({"code": 400, "message": "Course is not active, cannot be canceled"})
            
            if course.course_Status == "Active":
                course.course_Status = 'Inactive'
                db.session.commit()
                db.session.close()
                return jsonify({"code": 200, "message": "Course has been deactivated"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "Failed: " + str(e)})

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
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to retire course"}, 404 

            args = retire_course.parse_args()
            courseID = args.get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()
            runCourses = RunCourse.query.filter_by(course_ID=courseID).all()

            if course:
                # Check if the course is inactive
                if course.course_Status == 'Inactive':
                    # Check if all associated run courses are closed
                    if all(runCourse.runcourse_Status == 'Closed' for runCourse in runCourses):
                        # Activate the course and commit the changes
                        course.course_Status = 'Retired'
                        db.session.commit()
                        db.session.close()
                        return jsonify({"code": 200, "message": "Course has been retired"})
                    else:
                        return jsonify({"code": 400, "message": "Course cannot be retired"})
                else:
                    return jsonify({"code": 400, "message": "There is no such run course to retire"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            db.session.rollback()
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
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to activate course"}, 404 

            args = activate_course.parse_args()
            courseID = args.get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()
            runCourses = RunCourse.query.filter_by(course_ID=courseID).all()
            
            if course:
                # Check if the course is inactive
                if course.course_Status == 'Inactive':
                    # Check if all associated run courses are closed
                    if all(runCourse.runcourse_Status == 'Closed' for runCourse in runCourses):
                        # Activate the course and commit the changes
                        course.course_Status = 'Active'
                        db.session.commit()
                        db.session.close()
                        return jsonify({"code": 200, "message": "Course has been activated"})
                    else:
                        return jsonify({"code": 400, "message": "Course cannot be activated because not all run courses are closed"})
                else:
                    return jsonify({"code": 400, "message": "There is no such run course to activate"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "Failed. " + str(e)})


add_interest = api.parser()
add_interest.add_argument("vote_ID", help="Vote ID")
add_interest.add_argument("user_ID", help="User ID")
@api.route('/add_interest', methods=["POST"])
@api.doc(description="Add Interest For Course")
class AddInterest(Resource):
    @api.expect(add_interest)
    def post(self):
        try:
            args = add_interest.parse_args()
            voteID = args.get("vote_ID")
            userID = args.get("user_ID")

            interestList = Interest.query.filter(Interest.interest_ID.contains("")).all()
            finalInterest = interestList[-1]
            interestID = finalInterest.interest_ID

            newInterest = Interest(interestID+1, voteID, userID)
            
            course = VoteCourse.query.filter_by(vote_ID = voteID).first()
            courseID = course.course_ID
            Proposedcourse = ProposedCourse.query.filter_by(course_ID=courseID).first()
            votecount = Interest.query.filter_by(vote_ID = voteID).count()
            Proposedcourse.voteCount = votecount + 1
            db.session.add(newInterest)
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"Express Interest Successfully! Please refer to your profile to find out the status of the course."}, default=str)), 200
        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500



delete_interest = api.parser()
delete_interest.add_argument("vote_ID", help="Vote ID")
delete_interest.add_argument("user_ID", help="User ID")
@api.route('/delete_interest')
@api.doc(description="Delete Interest for Course")
class DeleteInterest(Resource):
    @api.expect(delete_interest)
    def post(self):
        try: 
            args = delete_interest.parse_args()
            voteID = args.get("vote_ID")
            userID = args.get("user_ID")
            interest_record = Interest.query.filter_by(vote_ID=voteID, user_ID=userID).first()
            if userID != str(interest_record.user_ID):
                return json.loads(json.dumps({"message": "User id is different"})), 404

            course = VoteCourse.query.filter_by(vote_ID = voteID).first()
            courseID = course.course_ID
            Proposedcourse = ProposedCourse.query.filter_by(course_ID=courseID).first()
            votecount = Interest.query.filter_by(vote_ID = voteID).count()
            Proposedcourse.voteCount = votecount - 1
            db.session.delete(interest_record)                                 
            db.session.commit()
            db.session.close()
            return json.loads(json.dumps({"message":"Unvote Interest Successfully! Please refer to View Course page to find out more courses."}, default=str)), 200
        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500

# Soft delete vote - Update status to Not Offered
update_vote_status_parser = api.parser()
update_vote_status_parser.add_argument("course_ID", type=int, help="Course ID")

@api.route('/update_vote_unoffered_course')
@api.doc(description="Update Vote Status in VoteCourse Table to 'Not Offered'")
class UpdateVoteStatus(Resource):
    @api.expect(update_vote_status_parser)
    def put(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to reject proposed course"}, 404 

            args = update_vote_status_parser.parse_args()
            course_ID = args.get("course_ID")

            # Find the corresponding VoteCourse record by course ID.
            vote_course = VoteCourse.query.filter_by(course_ID=course_ID).first()

            if vote_course is None:
                return {"message": "VoteCourse record not found for the specified course"}, 404

            # Update the vote_Status to 'Not Offered'.
            vote_course.vote_Status = 'Not Offered'
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"You have delete the course successfully. Please refer to 'Deleted Course' Tab."}, default=str)), 200

        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500
        
# Close Voting
close_vote_course_parser = api.parser()
close_vote_course_parser.add_argument("course_ID", type=int, help="Course ID")

@api.route('/close_vote_course')
@api.doc(description="Close Voting")
class CloseVoteCourse(Resource):
    @api.expect(close_vote_course_parser)
    def put(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to close vote course"}, 404 

            args = close_vote_course_parser.parse_args()
            course_ID = args.get("course_ID")

            vote_course = VoteCourse.query.filter_by(course_ID=course_ID).first()

            if vote_course is None:
                return {"message": "VoteCourse record not found for the specified course"}, 404

            vote_course.vote_Status = 'Closed'
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"You have closed the course. The course is not available for voting now."}, default=str)), 200

        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500


# update run course by admin
admin_update_course = {
    "course_Name": fields.String(description="Course Name", required=True),
    "course_Desc": fields.String(description="Course Description", required=True),
    "coursecat_ID": fields.Integer(description="Course Category ID", required=True),
}

@api.route('/admin_update_course/<int:course_id>', methods=['PUT'])
@api.doc(description="Admin Update Course")
class AdminUpdateRunCourse(Resource):
    @api.expect(admin_update_course)
    def put(self, course_id):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to create course"}, 404 

            data = request.get_json()
            course_name = data.get('course_Name')
            course_desc = data.get('course_Desc')
            coursecat_ID = data.get('coursecat_ID')

            course = Course.query.get(course_id)

            if course is None:
                return jsonify({"message": "course not found", "code": 404}), 404

            course.course_Name = course_name
            course.course_Desc = course_desc
            course.coursecat_ID = coursecat_ID

            db.session.commit()
            db.session.close()

            return jsonify({"message": "course updated successfully", "code": 200})

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to update course: {str(e)}", "code": 500})

student_enrolled_courses_with_attendance = api.parser()
student_enrolled_courses_with_attendance.add_argument("course_name", help="Enter course name", location="args")
student_enrolled_courses_with_attendance.add_argument("coursecat_id", help="Enter course category id", location="args")
@api.route("/studentEnrolledCourse/<int:user_ID>")
class GetUserCourses(Resource):
    @api.expect(student_enrolled_courses_with_attendance)
    def get(self, user_ID):
        try:
            args = student_enrolled_courses_with_attendance.parse_args()
            course_name = args.get("course_name")
            coursecat_id = args.get("coursecat_id")

            # Base query to retrieve enrolled courses for the user
            base_query = db.session.query(
                Course, CourseCategory, RunCourse, Registration, User
            ).select_from(User).join(
                Registration,
                Registration.user_ID == User.user_ID
            ).join(
                RunCourse,
                RunCourse.rcourse_ID == Registration.rcourse_ID
            ).join(
                Course,
                Course.course_ID == RunCourse.course_ID
            ).join(
                CourseCategory,
                CourseCategory.coursecat_ID == Course.coursecat_ID
            ).filter(
                User.user_ID == user_ID,
                Registration.reg_Status == "Enrolled"
            )

            # Apply filters if course_name and coursecat_id are provided
            if course_name:
                base_query = base_query.filter(RunCourse.run_Name == course_name)
            if coursecat_id:
                base_query = base_query.filter(Course.coursecat_ID == coursecat_id)

            user_courses = base_query.all()

            result_data = []
            for result in user_courses:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
                }

                # Query lessons for this RunCourse
                lessons = db.session.query(Lesson).filter(Lesson.rcourse_ID == result[2].rcourse_ID).all()

                # Calculate attendance rate
                total_lessons = len(lessons)
                attended_lessons = 0
                missed_lessons_with_valid_reason = 0

                # Query attendance records for this run_course
                attendance_records = db.session.query(AttendanceRecord).filter(
                    AttendanceRecord.user_ID == user_ID,
                    AttendanceRecord.lesson_ID.in_([lesson.lesson_ID for lesson in lessons])
                ).all()

                valid_reason_keywords = ["sick", "doctor appointment", "medical leave", "family emergency", "mc", "personal reasons", "hospitalised"]

                # Count attended and missed lessons with valid reasons
                for record in attendance_records:
                    if record.status == 'Present' or record.status == 'Late':
                        attended_lessons += 1
                    elif record.status == 'Absent':
                        if record.reason:
                            # Check if the reason is not empty or only contains whitespace
                            trimmed_reason = record.reason.strip()
                            
                            if trimmed_reason.lower() in valid_reason_keywords:
                                
                                missed_lessons_with_valid_reason += 1
                            

                # Calculate attendance rate
                if total_lessons > 0:
                    attendance_rate = ((attended_lessons + missed_lessons_with_valid_reason) / total_lessons) * 100
                else:
                    attendance_rate = 0
                

                modified_run_course = {**result[2].json(), **run_course_attrs, "attendance_rate": attendance_rate}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1].coursecat_Name,
                    **modified_run_course,
                    **result[3].json(),
                    "user_Name": result[4].user_Name
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        except Exception as e:
            return jsonify({"code": 500, "message": str(e)})


retrieve_all_run_course_by_course_id_admin = api.parser()
retrieve_all_run_course_by_course_id_admin.add_argument("course_name", help="Enter course name")
retrieve_all_run_course_by_course_id_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_run_course_by_course_id_admin.add_argument("course_status", help="Enter run course status")
retrieve_all_run_course_by_course_id_admin.add_argument("course_id", help="Enter course id")
@api.route("/get_all_run_course_by_course_id")
@api.doc(description="Get all run course by course id")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_run_course_by_course_id_admin)
    def get(self):
        args = retrieve_all_run_course_by_course_id_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("course_status", "")
        course_id = args.get("course_id", "")

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
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)
        if course_id:
            query = query.filter(RunCourse.course_ID == course_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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

# Course Name
retrieve_course_name = api.parser()
retrieve_course_name.add_argument("course_id", help="Enter course id")

@api.route("/get_course_name")
@api.doc(description="Get course name")
class GetStudentName(Resource):
    @api.expect(retrieve_course_name)
    def get(self):
        args = retrieve_course_name.parse_args()
        course_id = args.get("course_id", "")

        course = Course.query.filter_by(course_ID=course_id).first()

        if course:
            course_name = course.course_Name
           
            return jsonify({"code": 200, "data": course_name})
        else:
            
            return jsonify({"code": 404, "message": "Course not found"})
        
# Student - Check if Course is Completed using user_id and rcourse_id
is_course_completed = api.parser()
is_course_completed.add_argument("rcourse_id", help="Enter rcourse id")
@api.route("/is_course_completed")
@api.doc(description="Check if Course is Completed using user_id and rcourse_id ")
class IsCourseCompleted(Resource):
    @api.expect(is_course_completed)
    def get(self):
        try:
            args = is_course_completed.parse_args()
            user_id = session.get('user_ID')
            rcourse_id = args.get("rcourse_id")
            current_datetime = datetime.now()

            # if student has existing completed course
            query = db.session.query(
                RunCourse,
                Registration
            ).select_from(RunCourse).join(
                Registration,
                Registration.rcourse_ID == RunCourse.rcourse_ID
            ).filter(
                RunCourse.rcourse_ID == rcourse_id,
                RunCourse.run_Enddate <= current_datetime,
                Registration.user_ID == user_id,
                Registration.reg_Status == 'Enrolled'
            )

            results = query.all()
            db.session.close()

            if results:
                # if student completed course, check if there is existing feedback response
                sub_query = db.session.query(
                    Feedback
                ).filter(
                    Feedback.submitted_By == user_id,
                    Feedback.rcourse_ID == rcourse_id
                )
                feedback_result = sub_query.all()
                
                if feedback_result:
                    return jsonify({"code": 200, "isCourseCompleted": True, "isFeedbackDone": True })
                else: 
                    return jsonify({"code": 200, "isCourseCompleted": True, "isFeedbackDone": False })
            else:
                return jsonify({"code": 200, "isCourseCompleted": False, "isFeedbackDone": False})

        except Exception as e:
            return jsonify({"code": 500, "message": str(e)})
