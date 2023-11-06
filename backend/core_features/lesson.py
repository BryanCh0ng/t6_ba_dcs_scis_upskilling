from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
from sqlalchemy.orm import aliased
import json

api = Namespace('lesson', description='Lesson related operations')

get_all_lessons = api.parser()
@api.route("/get_all_lessons")
@api.doc(description="Get all lessons")
class GetAllLessons(Resource):
    @api.expect(get_all_lessons)
    def get(self):

        def get_runcourse_details(rcourse_id):
            try: 
                rc_alias = aliased(RunCourse)
                user_alias = aliased(User)

                run_course = db.session.query(
                    Course,
                    rc_alias,
                    CourseCategory,
                    user_alias.user_Name
                ).select_from(Course).join(rc_alias, Course.course_ID == rc_alias.course_ID).join(
                    CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
                ).join(user_alias, rc_alias.instructor_ID == user_alias.user_ID) .filter(
                    rc_alias.rcourse_ID == rcourse_id).first()

                if run_course:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
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

        try:
            all_lessons = Lesson.query.all()
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
                            "lesson_Date": common.format_date_time(lesson.lesson_Date),
                            "run_Name": runcourse_response[0]['run_course']['run_Name'],
                            "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                            "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                            "lesson_Status": status,
                            "instructor_Name": runcourse_response[0]['run_course']['instructor_Name'],
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
            return {"code": 200, "lessons": sorted_lessons}, 200

        except Exception as e:
                return {"code": 404, "message": "Failed " + str(e)}, 404
        

get_lessons_by_rcourse_id = api.parser()
get_lessons_by_rcourse_id.add_argument("runcourse_id", help="Enter rcourse id")
@api.route("/get_lessons_by_rcourse_id")
@api.doc(description="Get lessons by rcourse id")
class GetLessonsByRcourseId(Resource):
    @api.expect(get_lessons_by_rcourse_id)
    def get(self):
        
        def get_runcourse_details(rcourse_id):
            try: 
                rc_alias = aliased(RunCourse)
                user_alias = aliased(User)

                run_course = db.session.query(
                    Course,
                    rc_alias,
                    CourseCategory,
                    user_alias.user_Name
                ).select_from(Course).join(rc_alias, Course.course_ID == rc_alias.course_ID).join(
                    CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
                ).join(user_alias, rc_alias.instructor_ID == user_alias.user_ID) .filter(
                    rc_alias.rcourse_ID == rcourse_id).first()

                if run_course:
                    run_course[1].run_Starttime = run_course[1].run_Starttime.strftime('%H:%M:%S')
                    run_course[1].run_Endtime = run_course[1].run_Endtime.strftime('%H:%M:%S')
                    run_course[1].reg_Starttime = run_course[1].reg_Starttime.strftime('%H:%M:%S')
                    run_course[1].reg_Endtime = run_course[1].reg_Endtime.strftime('%H:%M:%S')
                    run_course[1].run_Startdate = run_course[1].run_Startdate.strftime('%Y-%m-%d')
                    run_course[1].run_Enddate = run_course[1].run_Enddate.strftime('%Y-%m-%d')
                    run_course[1].reg_Startdate = run_course[1].reg_Startdate.strftime('%Y-%m-%d')
                    run_course[1].reg_Enddate = run_course[1].reg_Enddate.strftime('%Y-%m-%d')
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

        try:
            rcourse_id = get_lessons_by_rcourse_id.parse_args().get("runcourse_id")
            all_lessons = Lesson.query.filter_by(rcourse_ID = rcourse_id).all()
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
                            "lesson_Date": common.format_date_time(lesson.lesson_Date),
                            "run_Name": runcourse_response[0]['run_course']['run_Name'],
                            "lesson_Starttime": lesson.lesson_Starttime.strftime('%H:%M:%S'),
                            "lesson_Endtime": lesson.lesson_Endtime.strftime('%H:%M:%S'),
                            "lesson_Status": status,
                            "instructor_Name": runcourse_response[0]['run_course']['instructor_Name'],
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
            return {"code": 200, "lessons": sorted_lessons}, 200

        except Exception as e:
                return {"code": 404, "message": "Failed " + str(e)}, 404
                   
