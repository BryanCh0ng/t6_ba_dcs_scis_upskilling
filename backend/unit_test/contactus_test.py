import sys
#sys.path.append("C:\\GitHub\\t6_ba_dcs_scis_upskilling")
import unittest
import flask_testing
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
#from allClasses import *
#import app
import json
from allClasses import *
from backend.core_features import contactus
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
        self.contactUs1 = ContactUs(msg_ID=1, user_ID=1, msg_Subject='Active', 
                                msg_Body='I tell people what to do', msg_Datetime= "2023-08-25 17:00:00")

        self.contactUs2 = ContactUs(msg_ID=2, user_ID=1, msg_Subject='Active', 
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
class getallmsg(Testapp):
    def test_get_all_msg(self):
        response = self.app.get('/get_all_msg')
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_msg_by_id(self):
        response = self.app.get("/get_all_msg?msg_ID=1")
        self.assertEqual(response.status_code, 200)

    def test_get_msg_no_id(self):
        response = self.app.get("/get_all_msg?msg_ID=13")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.message, "No such message exists")
