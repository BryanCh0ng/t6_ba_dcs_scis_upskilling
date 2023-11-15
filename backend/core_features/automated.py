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

@scheduler.task('interval', id='check_registration_close', seconds=3600, misfire_grace_time=900)
def check_registration_close():
    regList = Registration.query.all()
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    for reg in regList:
        rcourseid_set = set()
        rcourseid_set.add(reg.json()["rcourse_ID"])

    for rcourseid in rcourseid_set:
        rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == rcourseid).first().json()
        rcourse_enddate = rcourse["reg_Enddate"].strftime("%Y-%m-%d")

        if rcourse_enddate == current_date:
            rcourse_endtime = rcourse["reg_Endtime"].strftime("%H:%M:%S")

            if rcourse_endtime <= current_time:
                coursesize = rcourse["course_Size"]
                registrations = Registration.query.filter(Registration.rcourse_ID == rcourseid).order_by(Registration.reg_ID).all()
                registrations_num = len(registrations.json())

                if coursesize >= registrations_num:
                    for registration in registrations:
                        try:
                            setattr(registration, "reg_Status", "Enrolled")

                            db.session.commit()
                            db.session.close()

                            return jsonify(
                                {
                                    "code": 201,
                                    "data": registration.json(),
                                    "message": "Registration has been successfully updated!"
                                }
                            )
    
                        except Exception as e:
                            db.session.rollback()
                            return "Failed" + str(e), 500
                        
                else:
                    reg_list = []
                    blacklist = []
                    i = 0

                    for registration in registrations:
                        userid = registration.json()["user_ID"]

                        blacklist_entry = Blacklist.query.filter(Blacklist.user_ID == userid).first()

                        if blacklist_entry:
                            blacklist.append(registration)
                            
                        elif not blacklist_entry and i < coursesize:
                            reg_list.append(registration)
                            i += 1

                    if i < coursesize:
                        for j in range(0, coursesize - i):
                            reg_list.append(blacklist.pop(0))

                    for reg in reg_list:
                        try:
                            setattr(reg, "reg_Status", "Enrolled")

                            db.session.commit()
                            db.session.close()

                            return jsonify(
                                {
                                    "code": 201,
                                    "data": reg.json(),
                                    "message": "Registration has been successfully updated!"
                                }
                            )
    
                        except Exception as e:
                            db.session.rollback()
                            return "Failed" + str(e), 500

@scheduler.task('interval', id='on_registration_close', seconds=3600, misfire_grace_time=900)
def open_close_registration():
    runCourseList = RunCourse.query.all()
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    for runCourse in runCourseList:
        startDate = runCourse.reg_Startdate.strftime("%Y-%m-%d")
        startTime = runCourse.reg_Starttime.strftime("%H:%M:%S")
        status = runCourse.runcourse_Status
        endDate = runCourse.reg_Enddate.strftime("%Y-%m-%d")
        endTime = runCourse.reg_Endtime.strftime("%H:%M:%S")

        if current_date == startDate and current_time >= startTime:
            if status != "Ongoing":
                try:
                    setattr(runCourse, "runcourse_Status", "Ongoing")
                    db.session.commit()
                    db.session.close()
                    
                    return json.loads(json.dumps({"message": 'Success', "code": 200}, default=str))
                
                except Exception as e:
                    db.session.rollback()
                    return "Failed" + str(e), 500
        
        elif current_date == endDate and current_time >= endTime:
            if status != "Closed":
                try:
                    setattr(runCourse, "runcourse_Status", "Closed")
                    db.session.commit()
                    db.session.close()

                    return json.loads(json.dumps({"message": 'Success', "code": 200}, default=str))
                
                except Exception as e:
                    db.session.rollback()
                    return "Failed" + str(e), 500 
                                        
# Automate update student attendance 
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
                    db.session.rollback()
                    return "Failed" + str(e), 500 
            

            today = datetime.now().date()
            lessons = db.session.query(Lesson).filter(Lesson.lesson_Date < today).all()
            if lessons:
                for lesson in lessons:
                    
                    attendance_response = get_attendance_list_from_lesson_id(lesson.lesson_ID)
                    
                    if attendance_response[0]["code"] == 200:
                        attendances = attendance_response[0]["attendances"]
                        for attendance in attendances:
                           add_update_attendance(lesson.lesson_ID, attendance['user_ID'])

            return jsonify({ "code": 201, "message": "Attendance has been successfully updated!"} )   

        except Exception as e:
            db.session.rollback()
            print(f"Error while update student attendance: {str(e)}")
            return "Failed" + str(e), 500 

# Automate blacklist
@scheduler.task('cron', id='check_and_blacklist_users', hour=4, minute=0, misfire_grace_time=900) 
# Define the function to check and blacklist users
def check_and_blacklist_users():
    with app.app_context():
        try:
            # Get a list of all users
            users = db.session.query(User).all()

            current_date = datetime.now().date()

            for user in users:
                user_ID = user.user_ID

                # Get a list of all run courses for the user
                run_courses = db.session.query(RunCourse).join(
                    Registration, Registration.rcourse_ID == RunCourse.rcourse_ID
                ).filter(
                    Registration.user_ID == user_ID,
                    Registration.reg_Status == "Enrolled",
                    RunCourse.run_Startdate <= current_date
                ).all()

                for run_course in run_courses:
                    
                    lessons = db.session.query(Lesson).filter(Lesson.rcourse_ID == run_course.rcourse_ID).all()
                    total_lessons = len(lessons)

                    attendance_records = db.session.query(AttendanceRecord).filter(
                        AttendanceRecord.user_ID == user_ID,
                        AttendanceRecord.lesson_ID.in_([lesson.lesson_ID for lesson in lessons])
                    ).all()

                    valid_reason_keywords = ["sick", "doctor appointment", "medical leave", "family emergency", "mc", "personal reasons", "hospitalized"]

                    missed_lessons_without_valid_reason = 0

                    for record in attendance_records:
                        if record.status == 'Absent':
                            if not record.reason or record.reason.strip().lower not in valid_reason_keywords:
                                missed_lessons_without_valid_reason += 1
                
                if total_lessons > 0:
                    attendance_rate = (total_lessons - missed_lessons_without_valid_reason) / total_lessons * 100
                    
                    # Check if the attendance rate is below 70%
                    if attendance_rate <= 70:
                        # Check if the user is already blacklisted
                        existing_blacklist = Blacklist.query.filter_by(user_ID=user_ID).first()
                        if not existing_blacklist:
                            # Add the user to the blacklist
                            blacklist_entry = Blacklist(user_ID=user_ID, blacklist_Datetime=datetime.now())
                            db.session.add(blacklist_entry)
                            db.session.commit()
                
            db.session.close()
            return jsonify({ "code": 201, "message": "Blacklist has been successfully updated!"} )   

        except Exception as e:
            db.session.rollback()
            print(f"Error while checking and blacklisting users: {str(e)}")
