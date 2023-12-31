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
        session_user_ID = common.getUserID()
        lesson_id = get_attendance_by_lesson_id.parse_args().get("lesson_id")
        if (user_role) == 'Student':
            return {"code": 400, "message": "Unathorized Access, Failed to get attendance record"}, 404
        
        if user_role == 'Trainer' or user_role == 'Instructor':
            instructor_id_query = (
                db.session.query(RunCourse.instructor_ID).join(Lesson, Lesson.rcourse_ID == RunCourse.rcourse_ID)
                .filter(
                    Lesson.lesson_ID == lesson_id
                ).first()
            )
            instructor_id = instructor_id_query[0] if instructor_id_query else None
            if (instructor_id != session_user_ID):
                return {"code": 400, "message": "Unathorized Access, Failed to get attendance record"}, 404
 
        registration_alias = aliased(Registration, name="registration_alias")
        attendance_record_alias = aliased(AttendanceRecord, name="attendance_record_alias")

        attendance_record_query = (
            db.session.query(attendance_record_alias, User.user_Name, User.user_Email, RunCourse.run_Name, registration_alias, RunCourse.instructor_ID)
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
            for attendance, user_name, user_email, run_name, registration, instructor_id in attendance_record_query:
                if attendance is not None:
                    attendances.append({
                        'status': attendance.status,
                        'reason': attendance.reason,
                        'attrecord_Status': attendance.attrecord_Status,
                        'user_ID': registration.user_ID, 
                        'user_Name': user_name,
                        'user_Email': user_email,
                        'run_Name': run_name,
                        'instructor_ID': instructor_id
                        })
                else:
                    attendances.append({
                        'status': 'Pending',
                        'reason': '',
                        'attrecord_Status': 'Pending',
                        'user_ID': registration.user_ID, 
                        'user_Name': user_name,
                        'user_Email': user_email,
                        'run_Name': run_name,
                        'instructor_ID': instructor_id
                    })
            return {"code": 200, "attendances": attendances}, 200
        else:
            return {"code": 400, "message": "There is no attendance record for this lesson"}, 400
      except Exception as e:
          return {"code": 404, "message": "Failed " + str(e)}, 404


update_attendance_by_lesson_id = api.parser()
update_attendance_by_lesson_id.add_argument("lesson_id", help="Enter lesson id")
update_attendance_by_lesson_id.add_argument("student_ids", help="Enter student ids")
update_attendance_by_lesson_id.add_argument("action", help="Enter action")
update_attendance_by_lesson_id.add_argument("absentReason", help="Enter absent reason")
update_attendance_by_lesson_id.add_argument("reasonInput", help="Enter reason input")
@api.route("/update_attendance_by_lesson_id", methods=["POST"])
@api.doc(description="Update Attendance by Lesson Id")
class updateAttendanceByLessonId(Resource):
    @api.expect(update_attendance_by_lesson_id)
    def post(self):
        user_role = common.getUserRole()
        if (user_role) == 'Student':
          return {"message": "Unauthorized Access, Failed to mark attendance"}, 404

        args = update_attendance_by_lesson_id.parse_args()
        lesson_id = args.get("lesson_id", "")
        student_ids = request.json.get("student_ids", [])
        action = args.get("action", "")
        absentReason = args.get("absentReason", "")
        reasonInput = args.get("reasonInput", "")

        def get_lesson_by_lesson_id(lesson_id):
            try:
                lesson = db.session.query(Lesson, RunCourse.course_Venue, RunCourse.instructor_ID).join(
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
                        'course_Venue': lesson[1],
                        'instructor_ID': lesson[2]
                    }
                    return {"code": 200, "lesson": lesson_data}
                else:
                    return {"code": 404, "message": "Lesson not found"}, 404
            except Exception as e:
                return {"code": 500, "message": "Failed " + str(e)}, 500
            
        def add_update_attendance(lesson_id, student_id, action, absentReason, reasonInput):
            try:
                attendance_record_query = db.session.query(AttendanceRecord).filter(
                        AttendanceRecord.user_ID == student_id,
                        AttendanceRecord.lesson_ID == lesson_id
                    ).first()
                if attendance_record_query:
                    if action == 'Present':
                        absentReason = None
                    update_data = {
                        'status': action,
                        'attrecord_Status': 'Submitted',
                        'reason': absentReason,
                    }
                    if (absentReason == 'Others'):
                        update_data = {
                            'status': action,
                            'attrecord_Status': 'Submitted',
                            'reason': reasonInput,
                        }
                    AttendanceRecord.query.filter_by(user_ID=student_id, lesson_ID=lesson_id).update(update_data)
                    db.session.commit()
                    return True
                else:
                    reason = reasonInput if absentReason == 'Others' else absentReason
                    if action == 'Present':
                        reason = None
                    new_attendance_record = AttendanceRecord(None, lesson_ID = lesson_id, status=action, attrecord_Status='Submited', reason=reason, user_ID=student_id)
                    db.session.add(new_attendance_record)
                    db.session.commit()
                    return True
            except Exception as e:
                db.session.rollback()
                return False

        try:
            lesson_response = get_lesson_by_lesson_id(lesson_id)
            if lesson_response['code'] == 200:
                lesson = lesson_response['lesson']
                lesson_date = datetime.strptime(lesson['lesson_Date'], "%Y-%m-%d")
                current_time = datetime.now()
                hours, minutes, seconds = map(int, lesson['lesson_Starttime'].split(':'))
                lesson_date_time = lesson_date.replace(hour=hours, minute=minutes, second=seconds)
                is_same_day = lesson_date.date() == current_time.date()
                has_passed = lesson_date_time <= current_time if is_same_day else False
                if (has_passed == False):
                    return {"code": 404, "message": "Unable to mark attendance as is not during lesson datetime"}, 404
                elif (lesson['instructor_ID'] != common.getUserID()):
                    return {"code": 404, "message": "Unable to mark attendance as user logged in is not instructor of this lesson."}, 404
                elif len(student_ids) == 0:
                    return {"code": 404, "message": "Please select at least 1 student to submit attendance."}, 404
                elif action == None:
                    return {"code": 404, "message": "Please select if student(s) are present, absent, or late before submitting attendance"}, 404
                elif action == 'Others' and reasonInput == '':
                    return {"code": 404, "message": "Please include absent reason"}, 404
                else:
                    for student_id in student_ids:
                        result = add_update_attendance(lesson_id, student_id, action, absentReason, reasonInput)
                        if (result == False):
                            db.session.rollback()
                            return {"code": 404, "message": "An error has occured while submitting attendance"}, 404
                    return {"code": 200, "message": "Successfully Submitted Attendance"}, 200
            else:
                db.session.rollback()
                return lesson_response
        except Exception as e:
            
            db.session.rollback()
            return jsonify({"code": 500, "message": "Failed " + str(e)}), 500


get_attendance_rate = api.parser()
get_attendance_rate.add_argument("rcourse_id", help="Enter rcourse id")
@api.route("/get_attendance_rate")
@api.doc(description="Get Attendance Rate")
class getAttendanceRate(Resource):
    @api.expect(get_attendance_rate)
    def get(self):
        try:
            user_role = common.getUserRole()
            user_id = common.getUserID()
            if (user_role) != 'Student':
                return {"code": 400, "message": "Unauthorized Access, Attendance Rate can only apply to student(s)"}, 400
            
            rcourse_id = get_attendance_rate.parse_args().get("rcourse_id")
            current_date = datetime.now().date()
            run_courses = db.session.query(RunCourse).join(
                Registration, Registration.rcourse_ID == RunCourse.rcourse_ID
            ).filter(
                Registration.user_ID == user_id,
                Registration.reg_Status == "Enrolled",
                RunCourse.run_Startdate <= current_date,
                RunCourse.rcourse_ID == rcourse_id
            ).all()

            if run_courses:
                for run_course in run_courses:
                    lessons = db.session.query(Lesson).filter(Lesson.rcourse_ID == run_course.rcourse_ID).all()
                    total_lessons = len(lessons)

                    attendance_records = db.session.query(AttendanceRecord).filter(
                        AttendanceRecord.user_ID == user_id,
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
                    print(attendance_rate)
                    # Check if the attendance rate is below 70%
                    if attendance_rate <= 70:
                        return {"code": 200, "message": "Your attendance Rate for this course is below 70%, you are not eligible to submit feedback.", "attendanceRatePassed": False}, 200
                
                    return {"code": 200, "attendanceRatePassed": True}, 200
            
            return {"code": 400, "message": "An error has occurred while retrieving student attendance rate"}, 400
        
 
        except Exception as e:
            return {"code": 500, "message":  "Failed " + str(e)}, 500
       