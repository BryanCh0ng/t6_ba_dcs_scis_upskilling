from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
import json
from sqlalchemy.orm import aliased
from flask_apscheduler import APScheduler


api = Namespace('automated', description='Automated related operations')

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Automate update student attendance 
# @scheduler.task('interval', id='check_and_update_student_attendance', seconds=30, misfire_grace_time=30)
@scheduler.task('cron', id='check_and_update_student_attendance', hour=4, minute=0, misfire_grace_time=900)
def check_and_update_student_attendance():
    with app.app_context():
        try:
            def get_attendance_list_from_lesson_id(lesson_id):
                try:
                    registration_alias = aliased(Registration, name="registration_alias")
                    attendance_record_alias = aliased(AttendanceRecord, name="attendance_record_alias")

                    attendance_record_query = (
                        db.session.query(attendance_record_alias, registration_alias)
                        .join(Lesson, Lesson.rcourse_ID == registration_alias.rcourse_ID)
                        .outerjoin(attendance_record_alias, (attendance_record_alias.user_ID == registration_alias.user_ID) & (attendance_record_alias.lesson_ID == lesson_id))
                        .filter(
                            registration_alias.reg_Status == 'Enrolled',
                            Lesson.lesson_ID == lesson_id
                        )
                        .all()
                    )

                    attendances = []
                    if attendance_record_query:
                        for attendance, registration in attendance_record_query:
                            if attendance is None:
                                attendances.append({
                                    'user_ID': registration.user_ID, 
                                })
                    return {"code": 200, "attendances": attendances}, 200
                except Exception as e:
                    return {"code": 404, "message": "Failed " + str(e)}, 404
            
            def add_update_attendance(lesson_id, student_id):
                try:
                    attendance_record_query = db.session.query(AttendanceRecord).filter(
                            AttendanceRecord.user_ID == student_id,
                            AttendanceRecord.lesson_ID == lesson_id
                        ).first()
                    if attendance_record_query:
                        return True
                    else:
                        new_attendance_record = AttendanceRecord(None, lesson_ID = lesson_id, status='Absent', attrecord_Status='Submited', reason='Attendance not submitted on lesson day', user_ID=student_id)
                        db.session.add(new_attendance_record)
                        db.session.commit()
                        return True
                except Exception as e:
                    return False
            

            today = datetime.now().date()
            lessons = db.session.query(Lesson).filter(Lesson.lesson_Date < today).all()
            if lessons:
                for lesson in lessons:
                    print(lesson.lesson_ID)
                    attendance_response = get_attendance_list_from_lesson_id(lesson.lesson_ID)
                    print(attendance_response)
                    if attendance_response[0]["code"] == 200:
                        attendances = attendance_response[0]["attendances"]
                        for attendance in attendances:
                            print(lesson.lesson_ID)
                            update_attendance_response = add_update_attendance(lesson.lesson_ID, attendance['user_ID'])
                            print("update_attendance_response", update_attendance_response)     
                    
            print('Automate update student attendance done')
            return jsonify({ "code": 201, "message": "Attendance has been successfully updated!"} )   

        except Exception as e:
            db.session.rollback()
            print(str(e))
            print(f"Error while update student attendance: {str(e)}")