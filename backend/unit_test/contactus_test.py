from os import name
import sys
import unittest
import flask_testing
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields

import json

from app import *
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
from datetime import datetime
import logging



class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        self.contactUs1 = ContactUs( msg_ID=1,user_ID=1, msg_Subject='Active', 
                                msg_Body='I tell people what to do', msg_Datetime= "2023-08-25 17:00:00")

        self.contactUs2 = ContactUs( msg_ID=2,user_ID=1, msg_Subject='Active', 
                                msg_Body='I tell people ', msg_Datetime= "2023-08-25 17:00:00")
        
        self.contactUs3 = ContactUs(msg_ID=3, user_ID=2, msg_Subject='Active', 
                                msg_Body='I tell', msg_Datetime= "2023-08-25 17:00:00")
      
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
        response = self.client.get('/get_all_msg', content_type='application/json')
        print(response.status_code)
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_msg_by_id(self):
        response = self.client.get("/get_all_msg?msg_ID=1", content_type='application/json')
        print(response.status_code)
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_get_msg_no_id(self):
        response = self.client.get("/get_all_msg?msg_ID=13", content_type='application/json')
        print(response.status_code)
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
                "code": 404,
                "message": "No such message exists"
            })


if name == 'main':
    unittest.main()