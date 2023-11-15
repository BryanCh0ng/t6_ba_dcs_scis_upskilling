import unittest
import flask_testing
import json
from app import app, db

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from core_features.coursecat import *
from allClasses import Course

class TestCourse(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    
    def create_app(self):
        return app

    def setUp(self):
        self.coursecat1 = CourseCategory(coursecat_ID=1, 
                              coursecat_Name="SCIS")
        self.coursecat2 = CourseCategory(coursecat_ID=2, 
                              coursecat_Name="SOE")
        self.coursecat3 = CourseCategory(coursecat_ID=3, 
                              coursecat_Name="SOB")
        
       
        
        db.create_all()
        db.session.add(self.coursecat1)
        db.session.add(self.coursecat2)
        db.session.add(self.coursecat3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestGetCourseCategory(TestCourse):
    def test_get_all_course_category(self):
        with self.app.test_request_context(): 
            response = GetAllCoursecat().get()
            response_data = response.get_json()
            self.assertEqual(response_data["code"], 200)
    
    def test_get_course_category_by_name_pass(self):
        request_body = {
            "coursecat_Name": "SC"
        }
        with self.app.test_request_context(json=request_body):
            coursecat_instance = GetAllCoursecat()
            response = coursecat_instance.get()
            response_data = response.get_json()
            self.assertEqual(response_data["code"], 200)

    
    def test_get_course_category_by_name_fail(self):
        request_body = {
            "coursecat_name": "TTT"
        }
        with self.app.test_request_context(json=request_body):
            coursecat_instance = GetAllCoursecat()
            response = coursecat_instance.get()
            print(response)
            self.assertEqual(response[1], 404)
            self.assertEqual(response[0],{'message': 'There is no such course category'} )
    
    def test_get_course_category_by_id_pass(self):
        request_body = {
            "coursecat_id": "1"
        }
        with self.app.test_request_context(json=request_body):
            coursecat_instance = GetCoursecat()
            response = coursecat_instance.get()
            print(response)
            self.assertEqual(response[1], 200)
            self.assertEqual(response[0],{'coursecat_ID': 1, 'coursecat_Name': 'SCIS'})
    
    def test_get_course_category_by_id_fail(self):
        request_body = {
            "coursecat_id": "10"
        }
        with self.app.test_request_context(json=request_body):
            coursecat_instance = GetCoursecat()
            response = coursecat_instance.get()
            print(response)
            self.assertEqual(response["code"], 404)
            self.assertEqual(response["message"],'There is no such course category')



if __name__ == '__main__':
    unittest.main()