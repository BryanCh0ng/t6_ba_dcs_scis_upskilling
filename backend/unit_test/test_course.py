import unittest
import flask_testing
import json
from app import app, db

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from core_features.course import *
from allClasses import Course, User
# from core_features.user import Login
from core_features.common import *

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

        self.registration1 = Registration(
            rcourse_ID=1, 
            user_ID=2, 
            reg_Status="Enrolled"
        )

        self.courseCategory1 = CourseCategory(
            coursecat_ID=1,
            coursecat_Name="SCIS"
        )

        self.runCourse1 = RunCourse('Python Fundamentals - Run 1' ,
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
                                    2, 2)
        
        self.runCourse2 = RunCourse('Management Communication in Python - Run 1' ,
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
                                    3, 3)
        
        db.create_all()
        db.session.add(self.course1)
        db.session.add(self.course2)
        db.session.add(self.course3)

        setattr(self.user1, "user_ID", 1)
        db.session.add(self.user1)
        setattr(self.user2, "user_ID", 2)
        db.session.add(self.user2)
        setattr(self.registration1, "reg_ID", 1)
        db.session.add(self.registration1)
        db.session.add(self.courseCategory1)
        setattr(self.runCourse1, "rcourse_ID", 1)
        setattr(self.runCourse2, "rcourse_ID", 2)
        db.session.add(self.runCourse1)
        db.session.add(self.runCourse2)


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
        request_body = {"course_id": 4}
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
                "course_ID": 4,
                "course_Name": 'Dashboard Specialist',
                "course_Desc": "test description",
                "coursecat_ID": 1,
                "course_Status": "Inactive"
                }
            )
            self.assertEqual(len(Course.query.all()), 4)

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
            self.assertEqual(len(Course.query.all()), 3)

# admin method
class TestEditCourse(TestCourse):
    def test_edit_course_success(self):
        request_body = {
            "course_Name": 'Database Mining 2',
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
                    "course_Name": 'Database Mining 2',
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
            course_id = 1
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 409, response[0]['message'])
            self.assertEqual(response[0]['message'], "Course name already exists")
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first().json(), {
                    "course_ID": 1,
                    "course_Name": 'Database Mining',
                    "course_Desc": "Learn how to mine databases",
                    "coursecat_ID": 1,
                    "course_Status": "Inactive"
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
            course_id = 4
            response = EditCourse().put(course_id=course_id)

            self.assertEqual(response[1], 404, response[0]['message'])
            self.assertEqual(response[0]['message'], "There is no such course")
            self.assertEqual(Course.query.filter_by(course_ID=course_id).first(), None)


class TestGetUnregisteredActiveCourses(TestCourse):
    def test_get_unregistered_active_courses_success(self):
        request_body = {"user_id": 2}
        with self.app.test_request_context(json=request_body):
            response = GetUnregisteredActiveCourses().get()

            print(response)

            # self.assertEqual(res['code'], 200)
            # self.assertEqual(res['data']['course'], [
            #         {
            #             'course_Desc': 'Learn how to mine databases', 
            #             'course_ID': 1, 
            #             'course_Name': 'Database Mining', 
            #             'course_Status': 'Inactive', 
            #             'coursecat_ID': 1
            #         }, 
            #         {
            #             'course_Desc': 'Learn python development', 
            #             'course_ID': 2, 
            #             'course_Name': 'Python Fundamentals', 
            #             'course_Status': 'active', 
            #             'coursecat_ID': 1
            #         }
            #     ]
            # )



if __name__ == '__main__':
    unittest.main()