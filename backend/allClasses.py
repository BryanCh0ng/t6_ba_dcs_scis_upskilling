from datetime import datetime, date
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Time
import os

app = Flask(__name__)
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_endpoint = os.getenv("DB_ENDPOINT")
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_endpoint}"
app.config["CORS_ALLOW_CREDENTIALS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CORS(app, supports_credentials=True)

################## User Class Creation ##################

class User(db.Model):
    __tablename__ = 'user'

    user_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_Name = db.Column(db.String(255), nullable=False)
    user_Email = db.Column(db.String(155), nullable=False)
    user_Password = db.Column(db.String(100), nullable=False)
    role_Name = db.Column(db.String(20), nullable=False)

    def __init__(self, user_Name, user_Email, user_Password, role_Name):
        self.user_Name = user_Name
        self.user_Email = user_Email
        self.user_Password = user_Password        
        self.role_Name = role_Name
    
    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
        

################## External User Class Creation ##################

class ExternalUser(db.Model):
    __tablename__ = 'externaluser'

    external_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'),  nullable=False)
    organisation_Name = db.Column(db.String(255), nullable=False)
    is_Alumni = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_ID, organisation_Name, is_Alumni):
        self.user_ID = user_ID
        self.organisation_Name = organisation_Name
        self.is_Alumni = is_Alumni        
    
    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
        
################## Course Category Class Creation ##################

class CourseCategory(db.Model):
    __tablename__ = 'coursecategory'

    coursecat_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    coursecat_Name = db.Column(db.String(10), nullable=False)


    def __init__(self, coursecat_ID, coursecat_Name):
        self.coursecat_ID = coursecat_ID
        self.coursecat_Name = coursecat_Name

    
    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
        


################## Course Class Creation ##################
class Course(db.Model):
    __tablename__ = 'course'

    course_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    course_Name = db.Column(db.String(255), nullable=False)
    course_Desc = db.Column(db.String(800), nullable=False)
    coursecat_ID = db.Column(db.Integer, db.ForeignKey('coursecategory.coursecat_ID'), nullable=False)
    course_Status = db.Column(db.String(255), nullable=False)


    def __init__(self, course_ID, course_Name, course_Desc, coursecat_ID, course_Status):
        self.course_ID = course_ID
        self.course_Name = course_Name
        self.course_Desc = course_Desc
        self.coursecat_ID = coursecat_ID
        self.course_Status = course_Status


    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
################## Propose Course Class Creation ##################
class ProposedCourse(db.Model):
    __tablename__ = 'proposedcourse'

    pcourse_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    submitted_By = db.Column(db.Integer,db.ForeignKey('user.user_ID'), nullable=False)
    action_Done_By = db.Column(db.Integer,db.ForeignKey('user.user_ID'), nullable=False)
    course_ID = db.Column(db.Integer,db.ForeignKey('course.course_ID'), nullable=False)
    pcourse_Status = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    proposed_Date = db.Column(db.Date, nullable=False)
    #proposed_date = db.Column(db.Date, default=datetime.today().strftime('%Y-%m-%d'), nullable=False)
    voteCount = db.Column(db.Integer, nullable=False)


    def __init__(self, pcourse_ID, submitted_By, action_Done_By, course_ID, pcourse_Status, reason, proposed_Date, voteCount):
        self.pcourse_ID = pcourse_ID
        self.submitted_By = submitted_By
        self.course_ID = course_ID
        self.pcourse_Status = pcourse_Status
        self.action_Done_By = action_Done_By
        self.reason = reason  
        self.proposed_Date = proposed_Date
        self.voteCount = voteCount         

    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
################## Vote Course Class Creation ##################
class VoteCourse(db.Model):
    __tablename__ = 'votecourse'

    vote_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    course_ID = db.Column(db.Integer,db.ForeignKey('course.course_ID'), nullable=False)
    vote_Status = db.Column(db.String(15), nullable=False)



    def __init__(self, course_ID, vote_Status ):
        self.course_ID = course_ID
        self.vote_Status = vote_Status

    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

################## Interest Class Creation ##################
class Interest(db.Model):
    __tablename__ = 'interest'

    interest_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    vote_ID = db.Column(db.Integer,db.ForeignKey('votecourse.vote_ID'), nullable=False)
    user_ID = db.Column(db.Integer,db.ForeignKey('user.user_ID'),  nullable=False)


    def __init__(self, interest_ID, vote_ID, user_ID ):
        self.interest_ID = interest_ID
        self.vote_ID = vote_ID
        self.user_ID = user_ID



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
################## Feedback Template Class Creation ##################
class FeedbackTemplate(db.Model):
    __tablename__ = 'feedbacktemplate'

    template_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    template_Name = db.Column(db.String(255), nullable=False)
    # created_on = db.Column(db.DateTime, default=datetime.now ,  nullable=False)
    created_On = db.Column(db.Date,  nullable=False)



    def __init__(self, template_ID, template_Name, created_On ):
        self.template_ID = template_ID
        self.template_Name = template_Name
        self.created_On = created_On



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            column_value = getattr(self, column)
            if isinstance(column_value, date):
                result[column] = column_value.strftime("%Y-%m-%d")
            else:
                result[column] = column_value
        return result
    
##################  Template Attribute Class Creation ##################
class TemplateAttribute(db.Model):
    __tablename__ = 'templateattribute'

    template_Attribute_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    input_Type = db.Column(db.String(255),  nullable=False)
    template_ID = db.Column(db.Integer, db.ForeignKey('feedbacktemplate.template_ID'),  nullable=False) 



    def __init__(self, template_Attribute_ID, question, input_Type, template_ID ):
        self.template_Attribute_ID = template_Attribute_ID
        self.question = question
        self.input_Type = input_Type
        self.template_ID = template_ID



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Likert Scale Class Creation ##################
class LikertScale(db.Model):
    __tablename__ = 'likertscale'

    likert_Scale_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    template_Attribute_ID = db.Column(db.Integer,db.ForeignKey('templateattribute.template_Attribute_ID'),  nullable=False)
    position = db.Column(db.Integer,  nullable=False)
    textlabel = db.Column(db.String(255), nullable=False) 



    def __init__(self, likert_Scale_ID, template_Attribute_ID, position, textlabel ):
        self.likert_Scale_ID = likert_Scale_ID
        self.template_Attribute_ID = template_Attribute_ID
        self.position = position
        self.textlabel = textlabel



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Feedback Class Creation ##################
class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    feedback_Template_ID = db.Column(db.Integer,  nullable=False)
    submitted_By = db.Column(db.Integer,  nullable=False)
    template_Attribute_ID = db.Column(db.Integer ,db.ForeignKey('templateattribute.template_Attribute_ID'), nullable=False) 
    answer = db.Column(db.String(255), nullable=False) 
    rcourse_ID = db.Column(db.Integer, db.ForeignKey('runcourse.rcourse_ID'), nullable=False) 



    def __init__(self, feedback_ID, feedback_Template_ID, submitted_By, template_Attribute_ID, answer, rcourse_ID):
        self.feedback_ID = feedback_ID
        self.feedback_Template_ID = feedback_Template_ID
        self.submitted_By = submitted_By
        self.template_Attribute_ID = template_Attribute_ID
        self.answer = answer
        self.rcourse_ID = rcourse_ID



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
################## Run Course Class Creation ##################
class RunCourse(db.Model):
    __tablename__ = 'runcourse'

    rcourse_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    run_Startdate = db.Column(db.Date, nullable=False)
    run_Enddate = db.Column(db.Date, nullable=False)
    run_Starttime = db.Column(Time, nullable=False)
    run_Endtime = db.Column(Time, nullable=False)
    instructor_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)
    course_Format = db.Column(db.String(20), nullable=False)
    course_Venue = db.Column(db.String(255), nullable=False)
    runcourse_Status = db.Column(db.String(15), nullable=False)
    course_Size = db.Column(db.Integer, nullable=False)
    course_Minsize = db.Column(db.Integer, nullable=False)
    course_Fee = db.Column(db.Integer, nullable=False)
    class_Duration = db.Column(db.Integer, nullable=False)
    reg_Startdate = db.Column(db.Date, nullable=False)
    reg_Enddate = db.Column(db.Date, nullable=False)
    reg_Starttime = db.Column(Time, nullable=False)
    reg_Endtime = db.Column(Time, nullable=False)
    template_ID = db.Column(db.Integer, db.ForeignKey('feedbacktemplate.template_ID'), nullable=False)
    course_ID = db.Column(db.Integer, db.ForeignKey('course.course_ID'), nullable=False)


    def __init__(self, run_Startdate, run_Enddate, run_Starttime, run_Endtime, instructor_ID,
                 course_Format, course_Venue, runcourse_Status, course_Size, course_Minsize, course_Fee,
                 class_Duration, reg_Startdate, reg_Enddate, reg_Starttime, reg_Endtime, template_ID,
                  course_ID):
        self.run_Startdate = run_Startdate
        self.run_Enddate = run_Enddate
        self.run_Starttime = run_Starttime
        self.run_Endtime = run_Endtime
        self.instructor_ID = instructor_ID
        self.course_Format = course_Format
        self.course_Venue = course_Venue
        self.runcourse_Status = runcourse_Status
        self.course_Size = course_Size
        self.course_Minsize = course_Minsize
        self.course_Fee = course_Fee
        self.class_Duration = class_Duration
        self.reg_Startdate = reg_Startdate
        self.reg_Enddate = reg_Enddate
        self.reg_Starttime = reg_Starttime
        self.reg_Endtime = reg_Endtime
        self.template_ID = template_ID
        self.course_ID = course_ID   


    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Registration Class Creation ##################
class Registration(db.Model):
    __tablename__ = 'registration'

    reg_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    rcourse_ID = db.Column(db.Integer, db.ForeignKey('runcourse.rcourse_ID'),  nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)
    reg_Status = db.Column(db.String(20), nullable=False) 



    def __init__(self, rcourse_ID, user_ID, reg_Status):
        self.rcourse_ID = rcourse_ID
        self.user_ID = user_ID
        self.reg_Status = reg_Status




    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Lesson Class Creation ##################
class Lesson(db.Model):
    __tablename__ = 'lesson'

    lesson_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    reg_ID = db.Column(db.Integer, db.ForeignKey('registration.reg_ID'),  nullable=False)
    lesson_Date = db.Column(db.Date, nullable=False)
    lesson_Time = db.Column(db.Time, nullable=False) 



    def __init__(self, lesson_ID, reg_ID, lesson_Date, lesson_Time):
        self.lesson_ID = lesson_ID
        self.reg_ID = reg_ID
        self.lesson_Date = lesson_Date
        self.lesson_Time = lesson_Time




    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Attendence Record Class Creation ##################
class AttendenceRecord(db.Model):
    __tablename__ = 'attendancerecord'

    attrecord_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    lesson_ID = db.Column(db.Integer, db.ForeignKey('lesson.lesson_ID'),  nullable=False)
    status = db.Column(db.String(15), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    attrecord_Status = db.Column(db.String(20), nullable=False) 



    def __init__(self, attrecord_ID, lesson_ID, status, reason, attrecord_Status):
        self.attrecord_ID = attrecord_ID
        self.lesson_ID = lesson_ID
        self.status = status
        self.reason = reason
        self.attrecord_Status = attrecord_Status




    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
##################  Blacklist Class Creation ##################
class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    blacklist_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'),  nullable=False)
    


    def __init__(self, blacklist_ID, user_ID ):
        self.blacklist_ID = blacklist_ID
        self.user_ID = user_ID
        



    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class ContactUs(db.Model):
    __tablename__ = 'contactus'

    msg_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'),  nullable=False)
    msg_Subject = db.Column(db.String(255), nullable=False)
    msg_Body = db.Column(db.String(800), nullable=False)
    msg_Datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_ID, msg_Subject, msg_Body, msg_Datetime):
        self.user_ID = user_ID
        self.msg_Subject = msg_Subject
        self.msg_Body = msg_Body
        self.msg_Datetime = msg_Datetime

    
    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result