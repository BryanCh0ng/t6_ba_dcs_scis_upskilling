from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
from sqlalchemy.orm import aliased
from itertools import groupby
import json

api = Namespace('lesson', description='Lesson related operations')

get_all_lessons = api.parser()
get_all_lessons.add_argument("runcourse_Name", help="Enter run course name")
get_all_lessons.add_argument("instructor_Name", help="Enter instructor name")
get_all_lessons.add_argument("coursecat_id", help="Enter run course category id")
get_all_lessons.add_argument("lesson_Status", help="Enter status name")

@api.route("/get_all_lessons")
@api.doc(description="Get all lessons")
class GetAllLessons(Resource):
    @api.expect(get_all_lessons)
    def get(self):
        def convert_to_datetime(lesson):
            return datetime.strptime(lesson["lesson_Date"], "%Y-%m-%d")

        args = get_all_lessons.parse_args()
        runcourse_name = args.get('runcourse_Name')
        instructor_Name  = args.get('instructor_Name')
        coursecat_id = args.get('coursecat_id')
        lesson_status  = args.get('lesson_Status')
        session_user_ID = common.getUserID()

        def get_runcourse_details(rcourse_id):
            try: 
                run_course = db.session.query(
                    Course,
                    RunCourse,
                    CourseCategory,
                    User.user_Name,
                    User.user_ID
                ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
                    CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
                ).join(User, RunCourse.instructor_ID == User.user_ID) .filter(
                    RunCourse.rcourse_ID == rcourse_id).first()

                if run_course:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Startdate = run_course[1].feedback_Startdate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Enddate = run_course[1].feedback_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Starttime = run_course[1].feedback_Starttime.strftime('%H:%M:%S')
                    run_course[1].feedback_Endtime = run_course[1].feedback_Endtime.strftime('%H:%M:%S')

                    course_info = {
                        **run_course[1].json(),
                        "coursecat_Name": run_course[2].coursecat_Name,
                        "instructor_Name": run_course[3],
                        "course_Desc": run_course[0].course_Desc,
                        "instructor_ID": run_course[4]
                    }
                    return {"code": 200, "run_course": course_info}, 200
                else:
                    return {"code": 400, 'message': "An error has occurred while retrieving run details"}, 400
            except Exception as e:
                print(str(e))
                return  {"code": 404, 'message':  "Failed " + str(e)}, 400

        try:
            all_lessons = Lesson.query.join(RunCourse, Lesson.rcourse_ID == RunCourse.rcourse_ID).join(Course, RunCourse.course_ID == Course.course_ID).join(User, User.user_ID == RunCourse.instructor_ID)

            if all_lessons:
                # Apply filters based on provided arguments
                if runcourse_name:
                    all_lessons = all_lessons.filter(RunCourse.run_Name.contains(runcourse_name))

                if instructor_Name:
                    all_lessons = all_lessons.filter(User.user_Name.contains(instructor_Name))

                if coursecat_id:
                    all_lessons = all_lessons.filter(Course.coursecat_ID == coursecat_id)

                if lesson_status:
                    if lesson_status == "Upcoming":
                        all_lessons = all_lessons.filter(Lesson.lesson_Date >= datetime.now().date())
                    elif lesson_status == "Ongoing":
                        all_lessons = all_lessons.filter(
                            Lesson.lesson_Date == datetime.now().date(),
                            Lesson.lesson_Starttime <= datetime.now().time(),
                            Lesson.lesson_Endtime >= datetime.now().time()
                        )
                    elif lesson_status == "Ended":
                        all_lessons = all_lessons.filter(Lesson.lesson_Date < datetime.now().date())
                
                all_lessons = all_lessons.all()

            lessons = []
            if all_lessons:
                for lesson in all_lessons:
                    rcourse_id = lesson.rcourse_ID
                    runcourse_response = get_runcourse_details(rcourse_id)
                    if runcourse_response[0]['code'] == 200:
                        status = 'Upcoming'
                        lesson_datetime = datetime.combine(lesson.lesson_Date, lesson.lesson_Endtime)
                        if lesson.lesson_Date == datetime.now().date() and datetime.now() <= lesson_datetime:
                            status = "Ongoing"
                        elif lesson.lesson_Date < datetime.now().date():
                            status = "Ended"
                        lessons.append({
                            "lesson_ID": lesson.lesson_ID,
                            "rcourse_ID": lesson.rcourse_ID,
                            "lesson_Date": lesson.lesson_Date.strftime('%Y-%m-%d'),
                            "run_Name": runcourse_response[0]['run_course']['run_Name'],
                            "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                            "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                            "lesson_Status": status,
                            "instructor_Name": runcourse_response[0]['run_course']['instructor_Name'],
                            "isTrainerForLesson": runcourse_response[0]['run_course']['instructor_ID'] == session_user_ID,
                            "run_course": runcourse_response[0]['run_course'],
                        })
                    else: 
                        return runcourse_response

            sorted_lessons = sorted(lessons, key=lambda lesson: (
                lesson["lesson_Status"] == "Ongoing",
                lesson["lesson_Status"] == "Upcoming",
                lesson["lesson_Status"] == "Ended",
                lesson["lesson_Date"],
                lesson["lesson_Starttime"]
            ), reverse=True)
            upcoming_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Upcoming"]
            ongoing_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Ongoing"]
            ended_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Ended"]

            upcoming_lessons_sorted = sorted(upcoming_lessons, key=convert_to_datetime)
            ongoing_lessons_sorted = sorted(ongoing_lessons, key=convert_to_datetime)
            ended_lessons_sorted = sorted(ended_lessons, key=convert_to_datetime)

            combined_sorted_lessons =  ongoing_lessons_sorted + upcoming_lessons_sorted + ended_lessons_sorted
            return {"code": 200, "lessons": combined_sorted_lessons}, 200

        except Exception as e:
            print(str(e))
            return {"code": 404, "message": "Failed " + str(e)}, 404
        finally:
            db.session.close()
        

get_lessons_by_rcourse_id = api.parser()
get_lessons_by_rcourse_id.add_argument("runcourse_id", help="Enter rcourse id")
@api.route("/get_lessons_by_rcourse_id")
@api.doc(description="Get lessons by rcourse id")
class GetLessonsByRcourseId(Resource):
    @api.expect(get_lessons_by_rcourse_id)
    def get(self):

        def convert_to_datetime(lesson):
            return datetime.strptime(lesson["lesson_Date"], "%Y-%m-%d")
        
        def get_runcourse_details(rcourse_id):
            try: 
                run_course = db.session.query(
                    Course,
                    RunCourse,
                    CourseCategory,
                    User.user_Name,
                    User.user_ID
                ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
                    CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
                ).join(User, RunCourse.instructor_ID == User.user_ID) .filter(
                    RunCourse.rcourse_ID == rcourse_id).first()

                if run_course:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Startdate = run_course[1].feedback_Startdate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Enddate = run_course[1].feedback_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Starttime = run_course[1].feedback_Starttime.strftime('%H:%M:%S')
                    run_course[1].feedback_Endtime = run_course[1].feedback_Endtime.strftime('%H:%M:%S')
                    
                    course_info = {
                        **run_course[1].json(),
                        "coursecat_Name": run_course[2].coursecat_Name,
                        "instructor_Name": run_course[3],
                        "course_Desc": run_course[0].course_Desc,
                        "instructor_ID": run_course[4]
                    }
                    return {"code": 200, "run_course": course_info}, 200
                else:
                    return {"code": 400, 'message': "An error has occurred while retrieving run details"}, 400
            except Exception as e:
                
                return  {"code": 404, 'message':  "Failed " + str(e)}, 400

        try:
            rcourse_id = get_lessons_by_rcourse_id.parse_args().get("runcourse_id")
            all_lessons = Lesson.query.filter_by(rcourse_ID=rcourse_id).all()
            session_user_ID = common.getUserID()

            lessons = []
            if all_lessons:
                for lesson in all_lessons:
                    rcourse_id = lesson.rcourse_ID
                    runcourse_response = get_runcourse_details(rcourse_id)
                    if runcourse_response[0]['code'] == 200:
                        status = 'Upcoming'
                        lesson_datetime = datetime.combine(lesson.lesson_Date, lesson.lesson_Endtime)
                        if lesson.lesson_Date == datetime.now().date() and datetime.now() <= lesson_datetime:
                            status = "Ongoing"
                        elif lesson.lesson_Date < datetime.now().date():
                            status = "Ended"
                        lessons.append({
                            "lesson_ID": lesson.lesson_ID,
                            "rcourse_ID": lesson.rcourse_ID,
                            "lesson_Date": lesson.lesson_Date.strftime('%Y-%m-%d'),  # Convert date to string
                            "run_Name": runcourse_response[0]['run_course']['run_Name'],
                            "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                            "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                            "lesson_Status": status,
                            "instructor_Name": runcourse_response[0]['run_course']['instructor_Name'],
                            "isTrainerForLesson": runcourse_response[0]['run_course']['instructor_ID'] == session_user_ID,
                            "run_course": runcourse_response[0]['run_course'],
                        })
                        
                    else: 
                        return runcourse_response

            db.session.close()
            sorted_lessons = sorted(lessons, key=lambda lesson: (
                lesson["lesson_Status"] == "Ongoing",
                lesson["lesson_Status"] == "Upcoming",
                lesson["lesson_Status"] == "Ended",
                lesson["lesson_Date"],
                lesson["lesson_Starttime"]
            ), reverse=True)
            upcoming_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Upcoming"]
            ongoing_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Ongoing"]
            ended_lessons = [lesson for lesson in sorted_lessons if lesson["lesson_Status"] == "Ended"]

            upcoming_lessons_sorted = sorted(upcoming_lessons, key=convert_to_datetime)
            ongoing_lessons_sorted = sorted(ongoing_lessons, key=convert_to_datetime)
            ended_lessons_sorted = sorted(ended_lessons, key=convert_to_datetime)

            combined_sorted_lessons = ongoing_lessons_sorted + upcoming_lessons_sorted + ended_lessons_sorted
            return {"code": 200, "lessons": combined_sorted_lessons}, 200

        except Exception as e:
                return {"code": 404, "message": "Failed " + str(e)}, 404
                   
lesson_model = api.model('Lesson', {
    'rcourse_ID': fields.Integer(required=True, description='The RunCourse ID'),
    'lesson_Date': fields.Date(required=True, description='Date of the lesson'),
    'lesson_Starttime': fields.String(required=True, description='Start time of the lesson'),
    'lesson_Endtime': fields.String(required=True, description='End time of the lesson')
})

@api.route("/add_lesson")
@api.doc(description="Add a new lesson")
class AddLesson(Resource):
    @api.expect(lesson_model)
    def post(self):
        data = request.get_json()

        try:
            lesson_Date = datetime.strptime(data['lesson_Date'], '%Y-%m-%d').date()
            
            lesson_Starttime = datetime.strptime(data['lesson_Starttime'], '%H:%M:%S').time()
            
            lesson_Endtime = datetime.strptime(data['lesson_Endtime'], '%H:%M:%S').time()

            new_lesson = Lesson(
                rcourse_ID=data['rcourse_ID'],
                lesson_Date=lesson_Date,
                lesson_Starttime=lesson_Starttime,
                lesson_Endtime=lesson_Endtime,
            )

            db.session.add(new_lesson)
            db.session.commit()
            db.session.close()

            return jsonify({"code": 200, "message": "Lesson added successfully"})
        except Exception as e:
            db.session.rollback()
            return {"code": 404, "message": "Failed " + str(e)}

remove_lesson_parser = api.parser()
remove_lesson_parser.add_argument('lesson_ID', type=int, required=True, help='ID of the lesson to be removed')

@api.route("/remove_lesson")
@api.doc(description="Remove a lesson by its ID")
class RemoveLesson(Resource):
    @api.expect(remove_lesson_parser)
    def delete(self):
        args = remove_lesson_parser.parse_args()
        lesson_id = args.get('lesson_ID')

        try:
            lesson_to_delete = Lesson.query.get(lesson_id)
            if lesson_to_delete:
                db.session.delete(lesson_to_delete)
                db.session.commit()
                db.session.close()
                
                return {"code": 200, "message": "Lesson removed successfully"}, 200
            else:
                
                return {"code": 404, "message": "Lesson not found"}, 404
        except Exception as e:
            db.session.rollback() 
            
            return {"code": 500, "message": f"An error occurred while trying to remove the lesson: {str(e)}"}, 500

get_lesson_info = api.parser()
get_lesson_info.add_argument("lesson_ID", help="Enter lesson id")
@api.route("/get_lesson_by_id")
@api.doc(description="Get a lesson by its ID")
class GetLessonById(Resource):
    @api.expect(get_lesson_info)
    def get(self):
        try:
            args = get_lesson_info.parse_args()
            lesson_id = args.get('lesson_ID')
            lesson = db.session.query(Lesson, RunCourse.course_Venue).join(
                RunCourse, Lesson.rcourse_ID == RunCourse.rcourse_ID).filter(
                Lesson.lesson_ID == lesson_id
            ).first()
            db.session.close()
            if lesson:
                lesson_data = {
                    "lesson_ID": lesson[0].lesson_ID,
                    "rcourse_ID": lesson[0].rcourse_ID,
                    "lesson_Date": common.format_date_time(lesson[0].lesson_Date),
                    "lesson_Starttime": lesson[0].lesson_Starttime.strftime('%H:%M:%S'),
                    "lesson_Endtime": lesson[0].lesson_Endtime.strftime('%H:%M:%S'),
                    'course_Venue': lesson[1]
                }
                return {"code": 200, "lesson": lesson_data}, 200
            else:
                return {"code": 404, "message": "Lesson not found"}, 404
        except Exception as e:
            return {"code": 500, "message": "Failed " + str(e)}, 500

update_lesson_model = api.model('UpdateLesson', {
    'lesson_Date': fields.String(required=False, description='Updated date of the lesson'),
    'lesson_Starttime': fields.String(required=False, description='Updated start time of the lesson'),
    'lesson_Endtime': fields.String(required=False, description='Updated end time of the lesson'),
})

@api.route("/update_lesson/<int:lesson_id>")
@api.doc(description="Update a lesson by its ID")
class UpdateLesson(Resource):
    @api.expect(update_lesson_model)
    def put(self, lesson_id):
        
        # Get the updated data from the request body
        updated_data = request.json
        
        try:
            lesson_to_update = Lesson.query.get(lesson_id)
            if not lesson_to_update:
                return {"message": "Lesson not found"}, 404

            # Update lesson with new data
            if 'lesson_Date' in updated_data:
                lesson_to_update.lesson_Date = updated_data['lesson_Date']

            if 'formattedStartTime' in updated_data: 
                formatted_start_time = datetime.strptime(updated_data['formattedStartTime'], '%H:%M:%S').time()
                lesson_to_update.lesson_Starttime = formatted_start_time

            if 'formattedEndTime' in updated_data: 
                formatted_end_time = datetime.strptime(updated_data['formattedEndTime'], '%H:%M:%S').time()
                lesson_to_update.lesson_Endtime = formatted_end_time

            db.session.commit()


            return {"code": 200, "message": "Lesson updated successfully"}

        except Exception as e:
            db.session.rollback()
            return {"code": 500, "message": "Failed " + str(e)}, 500


get_lessons_by_user_id = api.parser()
get_lessons_by_user_id.add_argument("user_id", help="Enter user id")
@api.route("/get_lessons_by_user_id")
@api.doc(description="Get lessons by user id")
class GetLessonsByUserId(Resource):
    @api.expect(get_lessons_by_user_id)
    def get(self):
        def get_runcourse_details_lessons(rcourse_id):
            try: 
                run_course = db.session.query(
                    Course,
                    RunCourse,
                    CourseCategory,
                    User.user_Name
                ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
                    CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
                ).join(User, RunCourse.instructor_ID == User.user_ID) .filter(
                    RunCourse.rcourse_ID == rcourse_id).first()

                if run_course:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Startdate = run_course[1].feedback_Startdate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Enddate = run_course[1].feedback_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Starttime = run_course[1].feedback_Starttime.strftime('%H:%M:%S')
                    run_course[1].feedback_Endtime = run_course[1].feedback_Endtime.strftime('%H:%M:%S')
                    course_info = {
                        **run_course[1].json(),
                        "coursecat_Name": run_course[2].coursecat_Name,
                        "instructor_Name": run_course[3],
                        "course_Desc": run_course[0].course_Desc,
                    }
                    return {"code": 200, "run_course": course_info}, 200
                else:
                    return {"code": 400, 'message': "An error has occurred while retrieving run details"}, 400
            except Exception as e:
                return  {"code": 404, 'message':  "Failed " + str(e)}, 400
    
        def get_lessons_details_by_rcourse_id(rcourse_id):
            try:
                all_lessons = Lesson.query.filter_by(rcourse_ID = rcourse_id).order_by(Lesson.lesson_Date.asc()).all()
                lessons = []
                if all_lessons:
                    for lesson in all_lessons:
                        rcourse_id = lesson.rcourse_ID
                        runcourse_response = get_runcourse_details_lessons(rcourse_id)
                        if runcourse_response[0]['code'] == 200:
                            status = 'Upcoming'
                            lesson_datetime = datetime.combine(lesson.lesson_Date, lesson.lesson_Endtime)
                            if lesson.lesson_Date == datetime.now().date() and datetime.now() <= lesson_datetime:
                                status = "Ongoing"
                            elif lesson.lesson_Date < datetime.now().date():
                                status = "Ended"
                            lessons.append({
                                "lesson_ID": lesson.lesson_ID,
                                "rcourse_ID": lesson.rcourse_ID,
                                "lesson_Date": lesson.lesson_Date.strftime('%Y-%m-%d'),  
                                "run_Name": runcourse_response[0]['run_course']['run_Name'],
                                "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                                "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                                "lesson_Status": status,
                                "instructor_Name": runcourse_response[0]['run_course']['instructor_Name'],
                                "run_course": runcourse_response[0]['run_course'],
                            })
                        else: 
                            return runcourse_response
                    return {"code": 200, 'lessons': lessons}, 200
                else:
                    return  {"code": 404, 'message':  "No Lessons Found"}, 404
            except Exception as e:
                return  {"code": 404, 'message':  "Failed " + str(e)}, 404
        
        def group_key(lesson):
            return (
                lesson["rcourse_ID"],
                lesson["lesson_ID"]
            )
        
        def convert_to_datetime(lesson):
            return datetime.strptime(lesson["lesson_Date"], "%Y-%m-%d")

        try:
            args = get_lessons_by_user_id.parse_args()
            user_id = args.get('user_id')
            session_user_ID = common.getUserID()
            user_role = common.getUserRole()
            if user_id != str(session_user_ID):
                return {"message": "Unathorized Access, No rights to view lessons"}, 404
            
            if user_role != "Student":
                return {"message": "Unathorized Access, No rights to view lessons"}, 404
   
            regList = Registration.query.filter(Registration.user_ID == user_id, Registration.reg_Status == 'Enrolled').all()
            regList = [reg.json() for reg in regList]
            lessonList = []
            for reg in regList:
                lessons_response = get_lessons_details_by_rcourse_id(reg['rcourse_ID'])
                if lessons_response[0]['code'] == 200:
                    lessonList.append(lessons_response[0]['lessons'])
                else:
                    return lessons_response
            flattened_lessons = [item for sublist in lessonList for item in sublist]
            upcoming_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Upcoming"]
            ongoing_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Ongoing"]
            ended_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Ended"]

            upcoming_lessons_sorted = sorted(upcoming_lessons, key=convert_to_datetime)
            ongoing_lessons_sorted = sorted(ongoing_lessons, key=convert_to_datetime)
            ended_lessons_sorted = sorted(ended_lessons, key=convert_to_datetime)

            combined_sorted_lessons =  ongoing_lessons_sorted + upcoming_lessons_sorted + ended_lessons_sorted

            unique_sorted_lessons = [next(group) for key, group in groupby(combined_sorted_lessons, key=group_key)]
            return {"code": 200, 'lessons': unique_sorted_lessons}, 200

        except Exception as e:
            
            return {"code": 404, "message": "Failed " + str(e)}, 404
        

get_lessons_by_instructor_id = api.parser()
get_lessons_by_instructor_id.add_argument("user_id", help="Enter user id")
@api.route("/get_lessons_by_instructor_id")
@api.doc(description="Get lessons by instructor id")
class GetLessonsByUserId(Resource):
    @api.expect(get_lessons_by_instructor_id)
    def get(self):
        def group_key(lesson):
            return (
                lesson["rcourse_ID"],
                lesson["lesson_ID"]
            )
        
        def convert_to_datetime(lesson):
            return datetime.strptime(lesson["lesson_Date"], "%Y-%m-%d")

        try:
            args = get_lessons_by_instructor_id.parse_args()
            user_id = args.get('user_id')
            session_user_ID = common.getUserID()
            user_role = common.getUserRole()
            if user_id != str(session_user_ID):
                return {"message": "Unathorized Access, No rights to view lessons"}, 404 

            if user_role != "Trainer" and user_role != "Instructor":
                return {"message": "Unathorized Access, No rights to view lessons"}, 404   
            
            run_courses = db.session.query(
                Course,
                RunCourse,
                CourseCategory,
                User.user_Name
            ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
                CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
            ).join(User, RunCourse.instructor_ID == User.user_ID) .filter(
                RunCourse.instructor_ID == user_id).all()
            
            if run_courses:
                lessons = []
                for run_course in run_courses:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Startdate = run_course[1].feedback_Startdate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Enddate = run_course[1].feedback_Enddate.strftime('%Y-%m-%d')
                    run_course[1].feedback_Starttime = run_course[1].feedback_Starttime.strftime('%H:%M:%S')
                    run_course[1].feedback_Endtime = run_course[1].feedback_Endtime.strftime('%H:%M:%S')
                    course_info = {
                        **run_course[1].json(),
                        "coursecat_Name": run_course[2].coursecat_Name,
                        "instructor_Name": run_course[3],
                        "course_Desc": run_course[0].course_Desc,
                    }
                    all_lessons = Lesson.query.filter_by(rcourse_ID = str(course_info['rcourse_ID'])).order_by(Lesson.lesson_Date.asc()).all()
                    if all_lessons:
                        for lesson in all_lessons:
                            status = 'Upcoming'
                            lesson_datetime = datetime.combine(lesson.lesson_Date, lesson.lesson_Endtime)
                            if lesson.lesson_Date == datetime.now().date() and datetime.now() <= lesson_datetime:
                                status = "Ongoing"
                            elif lesson.lesson_Date < datetime.now().date():
                                status = "Ended"
                            lessons.append({
                                "lesson_ID": lesson.lesson_ID,
                                "rcourse_ID": lesson.rcourse_ID,
                                "lesson_Date": lesson.lesson_Date.strftime('%Y-%m-%d'),  
                                "run_Name": course_info['run_Name'],
                                "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                                "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                                "lesson_Status": status,
                                "instructor_Name": course_info['instructor_Name'],
                                "run_course": course_info,
                            })
                    else:
                        return  {"code": 404, 'message':  "No Lessons Found"}, 40
                flattened_lessons = sorted(lessons, key=lambda lesson: lesson["lesson_Status"])
                upcoming_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Upcoming"]
                ongoing_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Ongoing"]
                ended_lessons = [lesson for lesson in flattened_lessons if lesson["lesson_Status"] == "Ended"]

                upcoming_lessons_sorted = sorted(upcoming_lessons, key=convert_to_datetime)
                ongoing_lessons_sorted = sorted(ongoing_lessons, key=convert_to_datetime)
                ended_lessons_sorted = sorted(ended_lessons, key=convert_to_datetime)

                combined_sorted_lessons =  ongoing_lessons_sorted + upcoming_lessons_sorted + ended_lessons_sorted

                unique_sorted_lessons = [next(group) for key, group in groupby(combined_sorted_lessons, key=group_key)]
                return {"code": 200, 'lessons': unique_sorted_lessons}, 200
            else:
                return  {"code": 404, 'message':  "No Lessons Found"}, 404
        except Exception as e:
            print(str(e))
            return {"code": 404, "message": "Failed " + str(e)}, 404
        finally:
            db.session.close()
