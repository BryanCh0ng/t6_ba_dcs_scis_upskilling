import unittest
import flask_testing
import json
from app import app, db

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from core_features.course import *
from allClasses import Course

class TestCourse(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    
    def create_app(self):
        return app
    
    def setUp(self):
        self.course1 = Course(course_ID=1, 
                              course_Name="Database Mining", 
                              course_Desc="Learn how to mine databases", 
                              coursecat_ID=1, 
                              course_Status="Inactive")
        
        self.course2 = Course(course_ID=2, 
                              course_Name="Python Fundamentals", 
                              course_Desc="Learn python development", 
                              coursecat_ID=1, 
                              course_Status="Active")
        
        self.course3 = Course(course_ID=3, 
                              course_Name="Management Communication", 
                              course_Desc="Manage your team with effective communication", 
                              coursecat_ID=2, 
                              course_Status="Active")
        
        db.create_all()
        db.session.add(self.course1)
        db.session.add(self.course2)
        db.session.add(self.course3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_addition(self):
    #     with self.app.test_request_context(json={"first": 5, "second": 10}):
    #         # Act
    #         response = Addition().post()

    #         # Assert
    #         self.assertEqual(response, 15)
    
class TestCreateCourse(TestCourse):
    def test_create_course(self):
        request_body = {
            # "course_ID": 1,
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


if __name__ == '__main__':
    unittest.main()