import os
import sys
import unittest
import flask_testing
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields

import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
import logging

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from core_features.feedback import *
from allClasses import Feedback


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def create_app(self):
        return app

    def setUp(self):
        self.feedback_1 = Feedback(feedback_ID=1, feedback_Template_ID=1, submitted_By=1, template_Attribute_ID=1, answer='4', rcourse_ID=1)
        self.feedback_2 = Feedback(feedback_ID=2, feedback_Template_ID=1, submitted_By=1, template_Attribute_ID=2, answer='3', rcourse_ID=1)
        self.feedback_3 = Feedback(feedback_ID=3, feedback_Template_ID=1, submitted_By=1, template_Attribute_ID=3, answer='5', rcourse_ID=1)

        self.feedback_4 = Feedback(feedback_ID=12, feedback_Template_ID=1, submitted_By=6, template_Attribute_ID=1, answer='3', rcourse_ID=1)
        self.feedback_5 = Feedback(feedback_ID=13, feedback_Template_ID=1, submitted_By=6, template_Attribute_ID=2, answer='4', rcourse_ID=1)
        self.feedback_6 = Feedback(feedback_ID=14, feedback_Template_ID=1, submitted_By=6, template_Attribute_ID=3, answer='4', rcourse_ID=1)

      
        db.create_all()
        db.session.add(self.feedback_1)
        db.session.add(self.feedback_2)
        db.session.add(self.feedback_3)

        db.session.add(self.feedback_4)
        db.session.add(self.feedback_5)
        db.session.add(self.feedback_6)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

############## TEST #################################
class getallmsg(TestApp):
    def test_get_template_duplicate(self):
        request_body = {
        "rcourse_id": 1,  # Assuming the rcourse_id value is 1 for all feedback entries
        "template_id": 1,  # Assuming the template_id value is 1 for all feedback entries
        "user_id": 1,  # Assuming the user_id value is 1 for all feedback entries
        "data": [
        {
            "feedback_ID": 4,
            "feedback_Template_ID": 1,
            "submitted_By": 1,
            "attribute_id": 4,
            "answer": "Self-introspection of the concepts taught in class",
            "rcourse_ID": 1
        },
        {
            "feedback_ID": 5,
            "feedback_Template_ID": 1,
            "submitted_By": 1,
            "attribute_id": 5,
            "answer": "Slower pace in class",
            "rcourse_ID": 1
        },
        {
            "feedback_ID": 6,
            "feedback_Template_ID": 1,
            "submitted_By": 1,
            "attribute_id": 6,
            "answer": "5",
            "rcourse_ID": 1
        }
        ],
        "common_questions_data": [
            {"attribute_id": 4, "answer": "Self-introspection of the concepts taught in class"},
            {"attribute_id": 5, "answer": "Slower pace in class"},
            {"attribute_id": 6, "answer": "5"}
    ]
    }   
        json_request_body = json.dumps(request_body)
        with self.app.test_request_context(data=json_request_body, content_type='application/json'): 
            response = GetTemplate().post()
            print (response)
            self.assertEqual(response[1], 409)

    # def test_get_template_pass(self):
    #     request_body = {
    #     "rcourse_id": 1,  # Assuming the rcourse_id value is 1 for all feedback entries
    #     "template_id": 1,  # Assuming the template_id value is 1 for all feedback entries
    #     "user_id": 2,  # Assuming the user_id value is 1 for all feedback entries
    #     "common_questions_data": [
    #         {"attribute_id": 4, "answer": "Self-introspection of the concepts taught in class"},
    #         {"attribute_id": 5, "answer": "Slower pace in class"},
    #         {"attribute_id": 6, "answer": "5"}
    # ]
    # }   
    #     json_request_body = json.dumps(request_body)
    #     with self.app.test_request_context(data=json_request_body, content_type='application/json'): 
    #         response = GetTemplate().post()
    #         print (response)
    #         self.assertEqual(response[1], 200)

if __name__ == '__main__':
    unittest.main()