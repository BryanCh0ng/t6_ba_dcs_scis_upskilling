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
        self.user = User(
            user_Name="Testor",
            user_Email="testor.2020@scis.smu.edu.sg",
            user_Password="$2b$12$5ZMFOF1.pQvm6OBEeTlNduMHNbo/I/hzn3z3DLkK12QNeOP4Rej7q",
            role_Name="Admin"
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
            course_Status="Active"
        )
        
        self.course3 = Course(
            course_ID=3, 
            course_Name="Management Communication", 
            course_Desc="Manage your team with effective communication", 
            coursecat_ID=2, 
            course_Status="Active"
        )
        
        db.create_all()
        db.session.add(self.course1)
        db.session.add(self.course2)
        db.session.add(self.course3)

        setattr(self.user, "user_ID", 1)
        db.session.add(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


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

# this method cant be tested cos session closed in helper method getUserRole in common.py
class TestEditCourse(TestCourse):
    def test_edit_course_success(self):
        request_body = {
            "course_Name": 'Database Mining 2',
            "course_Desc": "edited course description",
            "coursecat_ID": 1,
            "course_Status": "Active"
        }
        with self.app.test_request_context(json=request_body):
            session['user_ID'] = 1
            response = EditCourse().put(course_id=1)

            self.assertEqual(response[1], 200, response[0]['message'])
            self.assertEqual(response[0]['message'], "Course updated successfully")
            self.assertEqual(response[0]['data'], {
                    "course_ID": 1,
                    "course_Name": 'Database Mining 2',
                    "course_Desc": "edited course description",
                    "coursecat_ID": 1,
                    "course_Status": "Active"
                }
            )


class TestGetAllCoursesFilterSearch(TestCourse):
    def test_get_all_courses_success(self):
        with self.app.test_request_context():
            response = GetAllCoursesFilterSearch().get()
            
            


if __name__ == '__main__':
    unittest.main()