import unittest
import flask_testing
import json

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from app import app, db
from core_features.course import *

class TestCourse(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'ashSDFSDFbiuoqewiort123!@*U&!&*(@^)'
    
    def create_app(self):
        return app
    
    def setUp(self):
        self.user1 = User(
            user_Name="Testor",
            user_Email="testor.2020@smu.edu.sg",
            user_Password="$2b$12$5ZMFOF1.pQvm6OBEeTlNduMHNbo/I/hzn3z3DLkK12QNeOP4Rej7q",
            role_Name="Admin"
        )

        self.user2 = User(
            user_Name="Testor2",
            user_Email="testor2.2020@smu.edu.sg",
            user_Password="$2b$12$5ZMFOF1.pQvm6OBEeTlNduMHNbo/I/hzn3z3DLkK12QNeOP4Rej7q",
            role_Name="Student"
        )

        self.user3 = User(
            user_Name="Testor3",
            user_Email="testor3.2020@smu.edu.sg",
            user_Password="$2b$12$5ZMFOF1.pQvm6OBEeTlNduMHNbo/I/hzn3z3DLkK12QNeOP4Rej7q",
            role_Name="Instructor"
        )
        
        self.course1 = Course(
            course_ID=1, 
            course_Name="Database Mining", 
            course_Desc="Learn how to mine databases", 
            coursecat_ID=1, 
            course_Status="Inactive"
        )
        
        self.course2 = Course(
            course_ID=2, 
            course_Name="Python Fundamentals", 
            course_Desc="Learn python development", 
            coursecat_ID=1, 
            course_Status="active"
        )
        
        self.course3 = Course(
            course_ID=3, 
            course_Name="Management Communication in Python", 
            course_Desc="Manage your development team with effective communication", 
            coursecat_ID=2, 
            course_Status="active"
        )

        self.course4 = Course(
            course_ID=4, 
            course_Name="Economics 101", 
            course_Desc="Learn some economic theories", 
            coursecat_ID=2, 
            course_Status="active"
        )

        self.registration1 = Registration(
            rcourse_ID=2, 
            user_ID=2, 
            reg_Status="enrolled"
        )

        self.courseCategory1 = CourseCategory(
            coursecat_ID=1,
            coursecat_Name="SCIS"
        )

        self.courseCategory2 = CourseCategory(
            coursecat_ID=2,
            coursecat_Name="SOB"
        )

        self.runCourse1 = RunCourse(
            'Python Fundamentals - Run 1' ,
            datetime.strptime('2023-12-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-11', '%Y-%m-%d').date(), 
            datetime.strptime('12:00:00', '%H:%M:%S').time(), 
            datetime.strptime('14:00:00', '%H:%M:%S').time(), 
            4, 
            'face-to-face', 
            'SCIS SR 2-4', 
            'ongoing', 
            35, 20, 0, 2, 
            datetime.strptime('2023-11-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-11-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('2023-12-15', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            2, 1
        )
        
        self.runCourse2 = RunCourse(
            'Management Communication in Python - Run 1' ,
            datetime.strptime('2023-12-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-11', '%Y-%m-%d').date(), 
            datetime.strptime('12:00:00', '%H:%M:%S').time(), 
            datetime.strptime('14:00:00', '%H:%M:%S').time(), 
            3, 
            'face-to-face', 
            'SCIS SR 2-4', 
            'ongoing', 
            35, 20, 0, 2, 
            datetime.strptime('2023-11-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-11-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('2023-12-15', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            3, 1
        )
        
        self.runCourse3 = RunCourse(
            'Economics 101 - Run 1' ,
            datetime.strptime('2023-12-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-11', '%Y-%m-%d').date(), 
            datetime.strptime('12:00:00', '%H:%M:%S').time(), 
            datetime.strptime('14:00:00', '%H:%M:%S').time(), 
            5, 
            'face-to-face', 
            'SCIS SR 2-4', 
            'ongoing', 
            35, 20, 0, 2, 
            datetime.strptime('2023-11-01', '%Y-%m-%d').date(), 
            datetime.strptime('2023-11-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('2023-12-15', '%Y-%m-%d').date(), 
            datetime.strptime('2023-12-20', '%Y-%m-%d').date(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            datetime.strptime('10:00:00', '%H:%M:%S').time(), 
            4, 1
        )
        
        self.interest1 = Interest(
            interest_ID = 1,
            vote_ID = 2,
            user_ID = 2
        )

        self.voteCourse1 = VoteCourse(
            course_ID = 2,
            vote_Status = 'ongoing'
        )

        self.voteCourse2 = VoteCourse(
            course_ID = 3,
            vote_Status = 'ongoing'
        )

        self.voteCourse3 = VoteCourse(
            course_ID = 4,
            vote_Status = 'ongoing'
        )

        self.proposedCourse1 = ProposedCourse(
            pcourse_ID = 1,
            submitted_By = 2,
            course_ID = 1,
            pcourse_Status = 'Approved',
            action_Done_By = 1,
            reason = "?",  
            proposed_Date = datetime.strptime('2023-09-01', '%Y-%m-%d').date(),
            voteCount = 18
        )

        self.feedback1 = Feedback(
            feedback_ID = 1,
            feedback_Template_ID = 1,
            submitted_By = 2,
            template_Attribute_ID = 1,
            answer = 'high',
            rcourse_ID = 2
        )

        
        db.create_all()
        db.session.add(self.course1)
        db.session.add(self.course2)
        db.session.add(self.course3)
        db.session.add(self.course4)

        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.add(self.user3)
        db.session.add(self.registration1)
        db.session.add(self.courseCategory1)
        db.session.add(self.courseCategory2)
        db.session.add(self.runCourse1)
        db.session.add(self.runCourse2)
        db.session.add(self.runCourse3)

        db.session.add(self.interest1)
        db.session.add(self.voteCourse1)
        db.session.add(self.voteCourse2)
        db.session.add(self.voteCourse3)
        db.session.add(self.proposedCourse1)
        db.session.add(self.feedback1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestGetAllCoursesFilterSearch(TestCourse):
    def test_get_all_courses_success(self):
        with self.app.test_request_context():
            response = GetAllCoursesFilterSearch().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(res['data']['course'], [
                    {
                        'course_Desc': 'Learn how to mine databases', 
                        'course_ID': 1, 
                        'course_Name': 'Database Mining', 
                        'course_Status': 'Inactive', 
                        'coursecat_ID': 1
                    }, 
                    {
                        'course_Desc': 'Learn python development', 
                        'course_ID': 2, 
                        'course_Name': 'Python Fundamentals', 
                        'course_Status': 'active', 
                        'coursecat_ID': 1
                    }, 
                    {
                        'course_Desc': 'Manage your development team with effective communication', 
                        'course_ID': 3, 
                        'course_Name': 'Management Communication in Python', 
                        'course_Status': 'active', 
                        'coursecat_ID': 2
                    },
                    {   
                        'course_ID': 4, 
                        'course_Name': "Economics 101", 
                        'course_Desc': "Learn some economic theories", 
                        'coursecat_ID': 2, 
                        'course_Status': "active"
                    }
                ]
            )

    def test_get_all_courses_filter_by_course_name(self):
        request_body = {"course_name": "python"}
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesFilterSearch().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(res['data']['course'], [
                    {
                        'course_Desc': 'Learn python development', 
                        'course_ID': 2, 
                        'course_Name': 'Python Fundamentals', 
                        'course_Status': 'active', 
                        'coursecat_ID': 1
                    },
                    {
                        'course_Desc': 'Manage your development team with effective communication', 
                        'course_ID': 3, 
                        'course_Name': 'Management Communication in Python', 
                        'course_Status': 'active', 
                        'coursecat_ID': 2
                    }
                ]
            )

    def test_get_all_courses_filter_by_coursecatid(self):
        request_body = {"coursecat_id": 1}
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesFilterSearch().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(res['data']['course'], [
                    {
                        'course_Desc': 'Learn how to mine databases', 
                        'course_ID': 1, 
                        'course_Name': 'Database Mining', 
                        'course_Status': 'Inactive', 
                        'coursecat_ID': 1
                    }, 
                    {
                        'course_Desc': 'Learn python development', 
                        'course_ID': 2, 
                        'course_Name': 'Python Fundamentals', 
                        'course_Status': 'active', 
                        'coursecat_ID': 1
                    }
                ]
            )

    def test_get_all_courses_filter_by_course_name_and_coursecatid(self):
        request_body = {"course_name": "python", "coursecat_id": 1}
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesFilterSearch().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(res['data']['course'], [
                    {
                        'course_Desc': 'Learn python development', 
                        'course_ID': 2, 
                        'course_Name': 'Python Fundamentals', 
                        'course_Status': 'active', 
                        'coursecat_ID': 1
                    }
                ]
            )

    def test_get_all_courses_no_such_course(self):
        request_body = {"course_name": "blockchain"}
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesFilterSearch().get()

            self.assertEqual(response['code'], 404)
            self.assertEqual(response['message'], "There is no such course")

# there are two classes DeleteCourse, so it calls the runcourse version
# class TestDeleteCourse(TestCourse):
#     def test_delete_course_success(self):
#         request_body = {"course_id": 2}
#         with self.app.test_request_context(json=request_body):
#             session['user_ID'] = 1
#             response = DeleteCourse().delete()

#             self.assertEqual(response[1], 200, response[0])
#             self.assertEqual(response[0], {"message":"Course successfully deleted"})


class TestGetCourse(TestCourse):
    def test_get_course_success(self):
        request_body = {"course_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetCourse().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(res['data']['course'], [
                    {
                        'course_Desc': 'Learn python development', 
                        'course_ID': 2, 
                        'course_Name': 'Python Fundamentals', 
                        'course_Status': 'active', 
                        'coursecat_ID': 1
                    }
                ]
            )

    def test_get_course_no_such_course(self):
        request_body = {"course_id": 5}
        with self.app.test_request_context(json=request_body):
            response = GetCourse().get()
            
            self.assertEqual(response[1], 404)
            self.assertEqual(response[0]['message'], "There is no such course")


class TestCreateCourse(TestCourse):
    def test_create_course_success(self):
        request_body = {
            "course_Name": 'Dashboard Specialist',
            "course_Desc": "test description",
            "coursecat_ID": 1,
            "course_Status": "Inactive"
        }
        with self.app.test_request_context(json=request_body):
            response = CreateCourse().post()

            self.assertEqual(response[1], 201)
            self.assertEqual(response[0]['data'], {
                "course_ID": 5,
                "course_Name": 'Dashboard Specialist',
                "course_Desc": "test description",
                "coursecat_ID": 1,
                "course_Status": "Inactive"
                }
            )
            self.assertEqual(len(Course.query.all()), 5)

    def test_create_course_already_exists(self):
        request_body = {
            "course_Name": 'Database Mining',
            "course_Desc": "test description",
            "coursecat_ID": 1,
            "course_Status": "Inactive"
        }
        with self.app.test_request_context(json=request_body):
            response = CreateCourse().post()

            self.assertEqual(response[1], 409)
            self.assertEqual(response[0], {
                "message": "Course name already exists"
                }
            )
            self.assertEqual(len(Course.query.all()), 4)

# admin method
class TestEditCourse(TestCourse):
    def test_edit_course_success(self):
        request_body = {
            "course_Name": 'Database Mining',
            "course_Desc": "edited course description",
            "coursecat_ID": 1,
            "course_Status": "active"
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 1
            course_id = 1
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 200, response[0]['message'])
            self.assertEqual(response[0]['message'], "Course updated successfully")
            self.assertEqual(response[0]['data'], {
                    "course_ID": course_id,
                    "course_Name": 'Database Mining',
                    "course_Desc": "edited course description",
                    "coursecat_ID": 1,
                    "course_Status": "active"
                }
            )
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first().json(), response[0]['data'])

    def test_edit_course_not_admin(self):
        request_body = {
            "course_Name": 'Database Mining 2',
            "course_Desc": "edited course description",
            "coursecat_ID": 1,
            "course_Status": "active"
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 2
            course_id = 1
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 404, response[0]['message'])
            self.assertEqual(response[0]['message'], "Unathorized Access, Failed to edit course")
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first().json(), {
                    "course_ID": 1,
                    "course_Name": 'Database Mining',
                    "course_Desc": "Learn how to mine databases",
                    "coursecat_ID": 1,
                    "course_Status": "Inactive"
                }
            )

    def test_edit_course_course_name_already_exists(self):
        request_body = {
            "course_Name": 'Database Mining',
            "course_Desc": "edited course description",
            "coursecat_ID": 1,
            "course_Status": "active"
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 1
            course_id = 2
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 409, response[0]['message'])
            self.assertEqual(response[0]['message'], "Course name already exists")
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first().json(), {
                    "course_ID": 2,
                    "course_Name": 'Python Fundamentals',
                    "course_Desc": "Learn python development",
                    "coursecat_ID": 1,
                    "course_Status": "active"
                }
            )

    def test_edit_course_course_does_not_exist(self):
        request_body = {
            "course_Name": 'Database Mining',
            "course_Desc": "edited course description",
            "coursecat_ID": 1,
            "course_Status": "active"
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 1
            course_id = 5
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 404, response[0]['message'])
            self.assertEqual(response[0]['message'], "There is no such course")
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first(), None)


class TestGetUnregisteredActiveCourses(TestCourse):
    def test_get_unregistered_active_courses_success(self):
        request_body = {"user_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][1]['course_Name'], 'Economics 101')

    def test_get_unregistered_active_courses_with_course_name(self):
        request_body = {"user_id": 2, "course_name": 'Python'}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')

    def test_get_unregistered_active_courses_with_coursecatid(self):
        request_body = {"user_id": 2, "coursecat_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Economics 101')

    def test_get_unregistered_active_courses_with_course_name_and_coursecatid(self):
        request_body = {"user_id": 2, "course_name": 'Python', "coursecat_id": 1}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')

    def test_get_unregistered_active_courses_no_such_courses(self):
        request_body = {"user_id": 2, "course_name": 'Python', "coursecat_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], 'No courses found')


class TestGetUnvotedOngoingCourses(TestCourse):
    def test_get_unvoted_ongoing_courses_success(self):
        with self.app.test_request_context():
            response = GetUnvotedOngoingCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 3)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][1]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][2]['course_Name'], 'Economics 101')

    def test_get_unvoted_ongoing_courses_with_userid(self):
        request_body = {"user_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnvotedOngoingCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][1]['course_Name'], 'Economics 101')

    def test_get_unvoted_ongoing_courses_with_userid_and_course_name(self):
        request_body = {"user_id": 2, "course_name": "python"}
        with self.app.test_request_context(json=request_body):
            response = GetUnvotedOngoingCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')

    def test_get_unvoted_ongoing_courses_with_userid_and_coursecatid(self):
        request_body = {"user_id": 2, "coursecat_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnvotedOngoingCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Economics 101')

    def test_get_unvoted_ongoing_courses_no_such_courses(self):
        request_body = {"user_id": 2, "course_name": "python", "coursecat_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnvotedOngoingCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No courses found")


class TestGetCourseRegistrationInfo(TestCourse):
    def test_get_course_registration_info_success(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 3)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][2]['course_Name'], 'Economics 101')

    def test_get_course_registration_info_with_course_name(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2,
            "course_name": "python"
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Python Fundamentals')
            
    def test_get_course_registration_info_with_coursecatid(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2,
            "coursecat_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Economics 101')

    def test_get_course_registration_info_with_course_name_and_coursecatid(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2,
            "course_name": 'python',
            "coursecat_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')

    def test_get_course_registration_info_with_regstatus(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="dropped"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2,
            "reg_status": 'dropped'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Economics 101')

    def test_get_course_registration_info_no_match(self):
        self.registration2 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        self.registration3 = Registration(
            rcourse_ID=3, 
            user_ID=2, 
            reg_Status="enrolled"
        )
        db.session.add(self.registration2)
        db.session.add(self.registration3)
        request_body = {
            "user_id": 2,
            "reg_status": 'dropped'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseRegistrationInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No matching course registration information found")


class TestGetCourseInterestInfo(TestCourse):
    def test_get_course_interest_info_success(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        request_body = {
            "user_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 3)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][2]['course_Name'], 'Economics 101')

    def test_get_course_interest_info_with_course_name(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        request_body = {
            "user_id": 2,
            "course_name": 'python'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Python Fundamentals')

    def test_get_course_interest_info_with_coursecatid(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        request_body = {
            "user_id": 2,
            "coursecat_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')
            self.assertEqual(res['data'][1]['course_Name'], 'Economics 101')

    def test_get_course_interest_info_with_course_name_and_coursecatid(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        request_body = {
            "user_id": 2,
            "course_name": 'python',
            "coursecat_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], 'Management Communication in Python')

    def test_get_course_interest_info_with_vote_status(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        setattr(self.voteCourse1, 'vote_Status', 'offered')
        setattr(self.voteCourse3, 'vote_Status', 'offered')
        request_body = {
            "user_id": 2,
            "vote_status": 'offered'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], 'Python Fundamentals')
            self.assertEqual(res['data'][1]['course_Name'], 'Economics 101')

    def test_get_course_interest_info_no_match(self):
        self.interest2 = Interest(
            interest_ID = 2,
            vote_ID = 1,
            user_ID = 2
        )
        self.interest3 = Interest(
            interest_ID = 3,
            vote_ID = 3,
            user_ID = 2
        )
        db.session.add(self.interest2)
        db.session.add(self.interest3)
        request_body = {
            "user_id": 2,
            "vote_status": 'offered'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCourseInterestInfo().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No matching course interest information found")


class TestGetProposedCourses(TestCourse):
    def test_get_proposed_courses_success(self):
        request_body = {
            "user_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetProposedCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Database Mining")

    def test_get_proposed_courses_no_match(self):
        request_body = {
            "user_id": 2,
            "pcourse_status": "rejected"
        }
        with self.app.test_request_context(json=request_body):
            response = GetProposedCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No matching proposed courses found")


class TestGetCompletedCourses(TestCourse):
    def test_get_completed_courses(self):
        setattr(self.registration1, 'reg_Status', 'Enrolled')
        setattr(self.runCourse2, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        request_body = {
            "user_id": 2
        }
        with self.app.test_request_context(json=request_body):
            response = GetCompletedCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")

    def test_get_completed_courses_none_found(self):
        setattr(self.registration1, 'reg_Status', 'Enrolled')
        setattr(self.runCourse2, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        request_body = {
            "user_id": 2,
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetCompletedCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No completed courses found")


class TestGetVotingCampaignCourses(TestCourse):
    def test_get_voting_campaign_courses_success(self):
        with self.app.test_request_context():
            response = GetVotingCampaignCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")

    def test_get_voting_campaign_courses_no_match(self):
        request_body = {
            "user_id": 2,
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetVotingCampaignCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No matching courses found")


class TestGetInstructorCourses(TestCourse):
    def test_get_instructor_courses_success(self):
        setattr(self.runCourse3, 'instructor_ID', 3)
        request_body = {
            "instructor_id": 3
        }
        with self.app.test_request_context(json=request_body):
            response = GetInstructorCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")
            self.assertEqual(res['data'][1]['course_Name'], "Economics 101")

    def test_get_instructor_courses_no_match(self):
        request_body = {
            "instructor_id": 3,
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetInstructorCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No courses found for the given criteria")


class TestGetProposedCoursesByUser(TestCourse):
    def test_get_proposed_courses_by_user_success(self):
        setattr(self.proposedCourse1, 'submitted_By', 3)
        request_body = {
            "instructor_id": 3
        }
        with self.app.test_request_context(json=request_body):
            response = GetProposedCoursesByUser().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Database Mining")

    def test_get_proposed_courses_by_user_no_match(self):
        setattr(self.proposedCourse1, 'submitted_By', 3)
        request_body = {
            "instructor_id": 3,
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetProposedCoursesByUser().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No matching proposed courses found")


class TestGetInstructorTaughtCourses(TestCourse):
    def test_get_instructor_taught_courses_success(self):
        setattr(self.runCourse1, 'instructor_ID', 3)
        setattr(self.runCourse1, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        setattr(self.runCourse2, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        request_body = {
            "instructor_id": 3
        }
        with self.app.test_request_context(json=request_body):
            response = GetInstructorTaughtCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], "Python Fundamentals")
            self.assertEqual(res['data'][1]['course_Name'], "Management Communication in Python")
            
    def test_get_instructor_taught_courses_none_found(self):
        setattr(self.runCourse1, 'instructor_ID', 3)
        setattr(self.runCourse1, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        setattr(self.runCourse2, 'run_Enddate', datetime.strptime('2023-11-11', '%Y-%m-%d').date())
        request_body = {
            "instructor_id": 3,
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetInstructorTaughtCourses().get()
            res = response.get_json()
            
            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No ended courses found for the given criteria")

# only can test the second one of the same class name in course.py
class TestGetAllProposedCoursesAdmin(TestCourse):
    def test_get_all_proposed_courses_admin_success(self):
        with self.app.test_request_context():
            response = GetAllProposedCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Database Mining")

    def test_get_all_proposed_courses_admin_none_found(self):
        setattr(self.proposedCourse1, 'pcourse_Status', 'pending')
        with self.app.test_request_context():
            response = GetAllProposedCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No proposed courses found")


class TestGetAllVotingCoursesAdmin(TestCourse):
    def test_get_all_voting_courses_admin_success(self):
        setattr(self.voteCourse2, 'vote_Status', "Ongoing")
        setattr(self.voteCourse3, 'vote_Status', "Ongoing")
        setattr(self.proposedCourse1, 'course_ID', 3)
        self.proposedCourse2 = ProposedCourse(
            pcourse_ID = 2,
            submitted_By = 2,
            course_ID = 4,
            pcourse_Status = 'Approved',
            action_Done_By = 1,
            reason = "?",  
            proposed_Date = datetime.strptime('2023-09-01', '%Y-%m-%d').date(),
            voteCount = 25
        )
        db.session.add(self.proposedCourse2)
        with self.app.test_request_context():
            response = GetAllVotingCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")
            self.assertEqual(res['data'][1]['course_Name'], "Economics 101")

    def test_get_all_voting_courses_admin_none_found(self):
        setattr(self.voteCourse2, 'vote_Status', "Ongoing")
        setattr(self.voteCourse3, 'vote_Status', "Ongoing")
        setattr(self.proposedCourse1, 'course_ID', 3)
        self.proposedCourse2 = ProposedCourse(
            pcourse_ID = 2,
            submitted_By = 2,
            course_ID = 4,
            pcourse_Status = 'Approved',
            action_Done_By = 1,
            reason = "?",  
            proposed_Date = datetime.strptime('2023-09-01', '%Y-%m-%d').date(),
            voteCount = 25
        )
        db.session.add(self.proposedCourse2)
        request_body = {
            "vote_status": 'pending'
        }
        with self.app.test_request_context(json=request_body):
            response = GetAllVotingCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No voting courses found")


class TestGetAllDeletedVotingCoursesAdmin(TestCourse):
    def test_get_all_deleted_voting_courses_admin(self):
        setattr(self.voteCourse2, 'vote_Status', "Not Offered")
        setattr(self.voteCourse3, 'vote_Status', "Not Offered")
        setattr(self.proposedCourse1, 'course_ID', 3)
        self.proposedCourse2 = ProposedCourse(
            pcourse_ID = 2,
            submitted_By = 2,
            course_ID = 4,
            pcourse_Status = 'Approved',
            action_Done_By = 1,
            reason = "?",  
            proposed_Date = datetime.strptime('2023-09-01', '%Y-%m-%d').date(),
            voteCount = 25
        )
        db.session.add(self.proposedCourse2)
        with self.app.test_request_context():
            response = GetAllDeletedVotingCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 2)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")
            self.assertEqual(res['data'][1]['course_Name'], "Economics 101")

    def test_get_all_deleted_voting_courses_admin_none_found(self):
        setattr(self.voteCourse2, 'vote_Status', "Not Offered")
        setattr(self.voteCourse3, 'vote_Status', "Not Offered")
        setattr(self.proposedCourse1, 'course_ID', 3)
        self.proposedCourse2 = ProposedCourse(
            pcourse_ID = 2,
            submitted_By = 2,
            course_ID = 4,
            pcourse_Status = 'Approved',
            action_Done_By = 1,
            reason = "?",  
            proposed_Date = datetime.strptime('2023-09-01', '%Y-%m-%d').date(),
            voteCount = 25
        )
        db.session.add(self.proposedCourse2)
        request_body = {
            "course_name": 'blockchain'
        }
        with self.app.test_request_context(json=request_body):
            response = GetAllDeletedVotingCoursesAdmin().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No voting courses found")

# this only tests the last class of the same name in course.py
class TestGetAllCoursesWithRegistrationCount(TestCourse):
    def test_get_all_courses_with_registration_count_success(self):
        request_body = {
            "course_id": 3
        }
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesWithRegistrationCount().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 1)
            self.assertEqual(res['data'][0]['course_Name'], "Management Communication in Python")

    def test_get_all_courses_with_registration_count_none_found(self):
        request_body = {
            "course_id": 1
        }
        with self.app.test_request_context(json=request_body):
            response = GetAllCoursesWithRegistrationCount().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No courses found")


class TestGetAllCourses(TestCourse):
    def test_get_all_courses_success(self):
        with self.app.test_request_context():
            response = GetAllCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 200)
            self.assertEqual(len(res['data']), 4)
            self.assertEqual(res['data'][0]['course_Name'], "Database Mining")
            self.assertEqual(res['data'][1]['course_Name'], "Python Fundamentals")
            self.assertEqual(res['data'][2]['course_Name'], "Management Communication in Python")
            self.assertEqual(res['data'][3]['course_Name'], "Economics 101")

    def test_get_all_courses_none_found(self):
        request_body = {
            "course_status": 'rejected'
        }
        with self.app.test_request_context(json=request_body):
            response = GetAllCourses().get()
            res = response.get_json()

            self.assertEqual(res['code'], 404)
            self.assertEqual(res['message'], "No courses found")


class TestDeactivateCourse(TestCourse):
    def test_deactivate_course_success(self):
        setattr(self.course1, 'course_Status', 'Active')
        course_ID = 1
        request_body = {
            "course_id": course_ID
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 1
            self.assertEqual(Course.query.filter_by(course_ID=course_ID).first().json(), {
                    'course_Desc': 'Learn how to mine databases', 
                    'course_ID': 1, 
                    'course_Name': 'Database Mining', 
                    'course_Status': 'Active', 
                    'coursecat_ID': 1
                }
            )
            response = DeactivateCourse().post()
            res = response.get_json()
            
            self.assertEqual(Course.query.filter_by(course_ID=course_ID).first().json(), {
                    'course_Desc': 'Learn how to mine databases', 
                    'course_ID': 1, 
                    'course_Name': 'Database Mining', 
                    'course_Status': 'Inactive', 
                    'coursecat_ID': 1
                }
            )
            self.assertEqual(res['code'], 200)
            self.assertEqual(res['message'], "Course has been deactivated")
            






if __name__ == '__main__':
    unittest.main()