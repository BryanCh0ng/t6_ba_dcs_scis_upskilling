from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
import json
from sqlalchemy.orm import aliased

api = Namespace('attendance', description='Attendance related operations')

get_attendance_by_lesson_id = api.parser()
get_attendance_by_lesson_id.add_argument("lesson_id", help="Enter lesson id")
@api.route("/get_attendance_by_lesson_id")
@api.doc(description="Get attendance by lesson id")
class GetAttendanceByLessonId(Resource): 
    @api.expect(get_attendance_by_lesson_id)
    def get(self):
      try:
        user_role = common.getUserRole()
        if (user_role) == 'Student':
            return {"code": 400, "message": "Unathorized Access, Failed to get attendance record"}, 404

        lesson_id = get_attendance_by_lesson_id.parse_args().get("lesson_id")
        registration_alias = aliased(Registration, name="registration_alias")
        attendance_record_alias = aliased(AttendanceRecord, name="attendance_record_alias")

        attendance_record_query = (
            db.session.query(attendance_record_alias, User.user_Name, User.user_Email, RunCourse.run_Name, registration_alias)
            .join(User, registration_alias.user_ID == User.user_ID)
            .join(Lesson, Lesson.rcourse_ID == registration_alias.rcourse_ID)
            .outerjoin(attendance_record_alias, (attendance_record_alias.user_ID == registration_alias.user_ID) & (attendance_record_alias.lesson_ID == lesson_id))
            .join(RunCourse, RunCourse.rcourse_ID == Lesson.rcourse_ID)
            .filter(
                registration_alias.reg_Status == 'Enrolled',
                Lesson.lesson_ID == lesson_id
            )
            .order_by(User.user_Name.asc())
            .all()
        )
        attendances = []
        db.session.close()
        if attendance_record_query:
            for attendance, user_name, user_email, run_name, registration in attendance_record_query:
                if attendance is not None:
                    attendances.append({
                        'status': attendance.status,
                        'reason': attendance.reason,
                        'attrecord_Status': attendance.attrecord_Status,
                        'user_ID': registration.user_ID, 
                        'user_Name': user_name,
                        'user_Email': user_email,
                        'run_Name': run_name
                        })
                else:
                    attendances.append({
                        'status': 'Pending',
                        'reason': '',
                        'attrecord_Status': 'Pending',
                        'user_ID': registration.user_ID, 
                        'user_Name': user_name,
                        'user_Email': user_email,
                        'run_Name': run_name
                    })
            return {"code": 200, "attendances": attendances}, 200
        else:
            return {"code": 400, "message": "There is no attendance record for this lesson"}, 400
      except Exception as e:
          return {"code": 404, "message": "Failed " + str(e)}, 404


get_attendances_by_trainer_instructor_id = api.parser()
get_attendances_by_trainer_instructor_id.add_argument("trainer_instructor_id", help="Enter trainer/instructor id")
@api.route("/get_attendance_by_trainer_instructor_id")
@api.doc(description="Get attendance by trainer instructor id")
class GetAttendanceByLessonId(Resource):
    @api.expect(get_attendances_by_trainer_instructor_id)
    def get(self):
      try:
        user_role = common.getUserRole()
        if (user_role) == 'Student':
            return {"code": 400, "message": "Unathorized Access, Failed to get attendance record"}, 404

        trainer_instructor_id = get_attendances_by_trainer_instructor_id.parse_args().get("trainer_instructor_id")

        
        runcourse_query = (
           db.session.query(RunCourse).filter(RunCourse.instructor_ID == trainer_instructor_id).all()
        )

        rcourses = [rcourse.json() for rcourse in runcourse_query]

        attendances = {}
        for rcourse in rcourses:
            db_query = (
                db.session.query(Lesson, AttendanceRecord)
                .join(RunCourse, Lesson.rcourse_ID == RunCourse.rcourse_ID)
                .join(AttendanceRecord, Lesson.lesson_ID == AttendanceRecord.lesson_ID)
                .filter(RunCourse.rcourse_ID == rcourse['rcourse_ID'])
                .all()
            )

            lesson_attendance = {}
            for lesson, attendance_record in db_query:
                if lesson not in lesson_attendance:
                    lesson_attendance[lesson] = []
                lesson_attendance[lesson].append(attendance_record)

            # Convert the dictionary to a list of key-value tuples
            lesson_attendance_list = list(lesson_attendance.items())

            print(lesson_attendance_list)
            if rcourse not in attendances:
                attendances[tuple(rcourse.items())] = []

            attendances[tuple(rcourse.items())].append(lesson_attendance_list)

    
        # for runcourse, lesson, attendace_record in db_query:
        #     runcourse.run_Startdate = common.format_date_time(runcourse.run_Startdate)
        #     runcourse.run_Enddate = common.format_date_time(runcourse.run_Enddate)
        #     runcourse.run_Starttime = common.format_date_time(runcourse.run_Starttime)
        #     runcourse.run_Endtime = common.format_date_time(runcourse.run_Endtime)
        #     runcourse.reg_Startdate = common.format_date_time(runcourse.reg_Startdate)
        #     runcourse.reg_Enddate = common.format_date_time(runcourse.reg_Enddate)
        #     runcourse.reg_Starttime = common.format_date_time(runcourse.reg_Starttime)
        #     runcourse.reg_Endtime = common.format_date_time(runcourse.reg_Endtime)
        #     runcourse.feedback_Startdate = common.format_date_time(runcourse.feedback_Startdate)
        #     runcourse.feedback_Enddate = common.format_date_time(runcourse.feedback_Enddate)
        #     runcourse.feedback_Starttime = common.format_date_time(runcourse.feedback_Starttime)
        #     runcourse.feedback_Endtime = common.format_date_time(runcourse.feedback_Endtime)
        #     lesson.lesson_Starttime = common.format_date_time(lesson.lesson_Starttime)
        #     lesson.lesson_Endtime = common.format_date_time(lesson.lesson_Endtime)
        #     lesson.lesson_Date = common.format_date_time(lesson.lesson_Endtime)
        #     # lesson.lesson_Starttime = lesson.lesson_Starttime.strftime('%H:%M:%S')
        #     # lesson.lesson_Endtime = lesson.lesson_Endtime.strftime('%H:%M:%S')
        #     attendances.append({
        #         "runcourse": runcourse.json(),
        #         "lesson": lesson.json(),
        #         "attendance_record": attendace_record.json()
        #     })
        # print(attendances)
        
        if attendances:
            return {"code": 200, "data": attendances}, 200
        else:
            return {"code": 400, "message": "There is no attendance record for this lesson"}, 400
      except Exception as e:
          return {"code": 404, "message": "Failed " + str(e)}, 404
