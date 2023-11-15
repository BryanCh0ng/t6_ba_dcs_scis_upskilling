import os
import sys
import unittest
import flask_testing
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields

import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
from datetime import datetime
import logging

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from core_features.contactus import *
from allClasses import ContactUs


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def create_app(self):
        return app

    def setUp(self):
        date_string = '2023-08-25 17:00:00'
        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        self.contactUs1 = ContactUs( user_ID=1, msg_Subject='Active', 
                                msg_Body='I tell people what to do', msg_Datetime= datetime_obj)

        self.contactUs2 = ContactUs( user_ID=1, msg_Subject='Active', 
                                msg_Body='I tell people ', msg_Datetime= datetime_obj)
        
        self.contactUs3 = ContactUs( user_ID=2, msg_Subject='Active', 
                                msg_Body='I tell', msg_Datetime= datetime_obj)
      
        db.create_all()
        db.session.add(self.contactUs1)
        db.session.add(self.contactUs2)
        db.session.add(self.contactUs3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


############## TEST #################################
class getallmsg(TestApp):
    def test_get_all_msg(self):
        with self.app.test_request_context(): 
            response = GetAllMsg().get()
            response_data = response.get_json()
        #returns test response
        # print(response)

        # print(response.get_data(as_text=True))
        # print("test1")
        self.assertEqual(response_data["code"], 200)
        
    def test_get_msg_by_id(self):
        request_body = {
            "msg_ID": 1
        }
        with self.app.test_request_context(json=request_body):
            msg_instance = GetAllMsg()
            response = msg_instance.get()
            response_data = response.get_json()
            # print(response_data)
            # # print(response_data["code"])
            # print(response_data["data"])
        # returns test response object
            # print("=====================================================================================================================")
            # print("test2")
            # print("expected output")
            # print({"code":200,"data":{"msg_list":[{"msg_Body":"I tell people what to do","msg_Datetime":"Fri, 25 Aug 2023 17:00:00 GMT","msg_ID":1,"msg_Subject":"Active","user_ID":1}]}})
            # print("actual output")
            # print(response.get_data(as_text=True))


        self.assertEqual(response_data["code"], 200)

        

    def test_get_msg_invalid_id(self):
        request_body = {
            "msg_ID": 12
        }
        with self.app.test_request_context(json=request_body):
            msg_instance = GetAllMsg()
            response = msg_instance.get()
            response_data = response.get_json()


        print(response.get_data(as_text=True))
        self.assertEqual(response_data["code"], 404)
        # self.assertEqual(response.json, {
        #         "code": 404,
        #         "message": "No such message exists"
        #     })

# class createnewMSG(TestApp):
#     def test_create_valid_msg(self):
#         date_string = '2023-08-25 17:00:00'
#         date  = datetime(2012, 3, 3, 10, 10, 10)
#         datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
#         request_body = {
#             "user_ID": 1, 
#             "msg_Subject": "Active", 
#             "msg_Body": "I am a test", 
#             "msg_Datetime":  date
#         }
        
#         with self.app.test_request_context(json=request_body):
#             create_msg_instance = CreateNewMsg()
#             response = create_msg_instance.post()
#             print(response[1])
#             print(response[0])

#             # response_data = response.get_json()
#             # print(response_data)

#             self.assertEqual(response[1], 201)



if __name__ == '__main__':
    unittest.main()