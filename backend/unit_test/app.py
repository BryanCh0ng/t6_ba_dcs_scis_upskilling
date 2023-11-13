import os
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace, Resource, fields, reqparse


import json
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, exists
from datetime import datetime, date, time
import logging

app = Flask(__name__)
# db_username = os.getenv("DB_USERNAME")
# db_password = os.getenv("DB_PASSWORD")
# db_endpoint = os.getenv("DB_ENDPOINT")
app.config["CORS_HEADERS"] = "Content-Type"
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_endpoint}"
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
        
################## Feedback Template Class Creation ##################
class FeedbackTemplate(db.Model):
    __tablename__ = 'feedbacktemplate'

    template_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
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

    
##################  Template Attribute Class Creation ##################
class TemplateAttribute(db.Model):
    __tablename__ = 'templateattribute'

    template_Attribute_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    input_Type = db.Column(db.String(255),  nullable=False)
    template_ID = db.Column(db.Integer, db.ForeignKey('feedbacktemplate.template_ID'),  nullable=False) 


    def __init__(self, question, input_Type, template_ID, template_Attribute_ID=None):
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
class InputOption(db.Model):
    __tablename__ = 'inputoption'

    input_Option_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    template_Attribute_ID = db.Column(db.Integer,db.ForeignKey('templateattribute.template_Attribute_ID'),  nullable=False)
    position = db.Column(db.Integer,  nullable=False)
    textlabel = db.Column(db.String(255), nullable=False) 

    def __init__(self, template_Attribute_ID, position, textlabel ):
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
    feedback_Template_ID = db.Column(db.Integer,  nullable=True)
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
    run_Name = db.Column(db.String(255), nullable=False)
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
    feedback_Startdate = db.Column(db.Date, nullable=False)
    feedback_Enddate = db.Column(db.Date, nullable=False)
    feedback_Starttime = db.Column(Time, nullable=False)
    feedback_Endtime = db.Column(Time, nullable=False)
    course_ID = db.Column(db.Integer, db.ForeignKey('course.course_ID'), nullable=False)
    template_ID = db.Column(db.Integer, db.ForeignKey('feedbacktemplate.template_ID'),  nullable=False) 

    def __init__(self, run_Name, run_Startdate, run_Enddate, run_Starttime, run_Endtime, instructor_ID,
                 course_Format, course_Venue, runcourse_Status, course_Size, course_Minsize, course_Fee,
                 class_Duration, reg_Startdate, reg_Enddate, reg_Starttime, reg_Endtime, feedback_Startdate, 
                 feedback_Enddate, feedback_Starttime, feedback_Endtime, course_ID , template_ID):
        self.run_Name = run_Name 
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
        self.feedback_Startdate = feedback_Startdate
        self.feedback_Enddate = feedback_Enddate
        self.feedback_Starttime = feedback_Starttime
        self.feedback_Endtime = feedback_Endtime
        self.course_ID = course_ID
        self.template_ID = template_ID     
 
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

    blacklist_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'),  nullable=False)
    
    def __init__(self, user_ID ):
        self.user_ID = user_ID
        
    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class ContactUs(db.Model):
    __tablename__ = 'contactus'

    msg_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'),  nullable=False)
    msg_Subject = db.Column(db.String(255), nullable=False)
    msg_Body = db.Column(db.String(800), nullable=False)
    msg_Datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self,msg_ID, user_ID, msg_Subject, msg_Body, msg_Datetime):
        self.msg_ID = msg_ID
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
    

################## METHODS COMMON ############################################
app.logger.setLevel(logging.DEBUG)

api = Namespace('common', description='Course related operations')

sort_records = api.parser()
sort_records.add_argument("sort_column", help="Enter sort column")
sort_records.add_argument("sort_direction", help="Enter sort direction")
sort_records.add_argument("records", help="Enter records")
@api.route("/sort_records", methods=["POST"])
@api.doc(description="Sort Records")
class sortRecords(Resource):
    @api.expect(sort_records)
    def post(self):
      args = sort_records.parse_args()
      sort_column = args.get("sort_column", "")
      sort_direction = args.get("sort_direction", "")
      records = request.json.get("records", [])

      records_with_values = [record for record in records if record.get(sort_column) is not None]
      records_with_none_values = [record for record in records if record.get(sort_column) is None]

      if sort_column != "":
          sorted_data = sorted(records_with_values, key=lambda x: x[sort_column], reverse=(sort_direction == "desc"))
      else:
          sorted_data = records

      sorted_data = records_with_none_values + sorted_data

      return jsonify({"code": 200, "data": sorted_data, "sort": sort_column, "direction": sort_direction})
    

def format_date_time(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, time):
        return value.strftime('%H:%M:%S')
    else:
        return None
    
    
def getUserRole(user_ID=None):
    if user_ID is None:
        user_ID = getUserID()

    if user_ID:
        user = db.session.query(User).filter_by(user_ID=user_ID).first()
        db.session.close()
        if user:
            return user.role_Name
        else:
            return None
    else:
        return None
    
def getUserID():
    user_ID = session.get('user_ID')
    print(user_ID)
    if user_ID:
        id = User.query.filter_by(user_ID=user_ID).first().user_ID
        db.session.close()
        return id
    else:
        db.session.close()
        return 'Session not set'
    
################## METHODS CONTACT US ############################################
# get_all_msg()
get_all_msg = api.parser()
get_all_msg.add_argument("msg_ID", help="Enter message ID")
@api.route("/get_all_msg")
@api.doc(description="Gets all messages")
class GetAllMsg(Resource):
    @api.expect(get_all_msg)
    def get(self):
        arg = get_all_msg.parse_args().get("msg_ID")
        msg_ID = arg if arg else ""
        msg_List = ContactUs.query.filter(ContactUs.msg_ID.contains(msg_ID)).all()

        if len(msg_List):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "msg_list": [msg.json() for msg in msg_List]
                    }
                }
            )
        
        return jsonify(
            {
                "code": 404,
                "message": "No such message exists"
            }
        )

# create_new_msg()
create_msg_model = api.model("create_msg_model", {
    "user_ID" : fields.Integer(description="User ID", required=True),
    "msg_Subject" : fields.String(description="Message subject", required=True),
    "msg_Body" : fields.String(description="Message body", required=True),
    "msg_Datetime" : fields.DateTime(description="Message date & time", required=True)
})

@api.route("/create_new_msg", methods=["POST"])
@api.doc(description="Creates new message record")
class CreateNewMsg(Resource):
    @api.expect(create_msg_model)
    def post(self):
        data = request.get_json()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["msg_Datetime"] = current_datetime
        msg = ContactUs(**data)

        try:
            db.session.add(msg)
            db.session.commit()
 
            return jsonify(
                {
                    "code": 201,
                    "data": msg.json(),
                    "message": "Message record has been successfully created!"
                }
            )
        
        
        except Exception as e:
            db.session.rollback()
            return "Failed" + str(e), 500
        
################## METHODS COURSE ############################################
        
retrieve_all_courses_filter_search = api.parser()
retrieve_all_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_all_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
@api.route("/retrieve_all_courses_filter_search")
@api.doc(description="Get all courses filter + search")
class GetAllCoursesFilterSearch(Resource):
	@api.expect(retrieve_all_courses_filter_search)
	def get(self):
		arg = retrieve_all_courses_filter_search.parse_args().get("course_name")
		course_Name = arg if arg else ""
		arg2 = retrieve_all_courses_filter_search.parse_args().get("coursecat_id")
		coursecat_ID = arg2 if arg2 else ""
		courseList = Course.query.filter(Course.course_Name.contains(course_Name), Course.coursecat_ID.contains(coursecat_ID)).all()
		db.session.close()
		if len(courseList):
			return jsonify(
				{
					"code": 200,
					"data": {
						"course": [course.json() for course in courseList]

					}
				}
			)
		return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

delete_course = api.parser()
delete_course.add_argument("course_id", help="Enter course id")
@api.route("/delete_course")
@api.doc(description="Delete course")
class DeleteCourse(Resource):
    @api.expect(delete_course)
    def delete(self):    
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to delete course"}, 404 

            courseID = delete_course.parse_args().get("course_id")
            course = Course.query.filter_by(course_ID=courseID).first()
        
            if(course):
                    try:
                        db.session.delete(course)              
                        db.session.commit()
                        db.session.close()                 
                        return json.loads(json.dumps({"message":"Course successfully deleted"})), 200
                    except Exception as e:
                        return "Foreign key dependencies exist, cannot delete. " + str(e), 408

            return json.loads(json.dumps({"Message": "There is no such course"}, default=str)), 404
        except Exception as e:
            db.session.rollback()
            return "Failed. " + str(e), 500
        
delete_runcourse = api.parser()
delete_runcourse.add_argument("rcourse_ID", help="Enter run course id")
@api.route("/delete_runcourse")
@api.doc(description="Delete run course")
class DeleteCourse(Resource):
    @api.expect(delete_runcourse)
    def delete(self):    
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to delete run course"}, 404 

            rcourse_ID = delete_runcourse.parse_args().get("rcourse_ID")
            # app.logger.debug(rcourse_ID)

            runCourse = RunCourse.query.filter_by(rcourse_ID=rcourse_ID).first()            
            if(runCourse):
                    try:
                        db.session.delete(runCourse)              
                        db.session.commit()
                        db.session.close()                 
                        return json.loads(json.dumps({"message":"Run Course has successfully deleted"})), 200
                    except Exception as e:
                        return "Foreign key dependencies exist, cannot delete. " + str(e), 408

            return json.loads(json.dumps({"Message": "There is no such run course"}, default=str)), 404

        except Exception as e:
            db.session.rollback()
            return "Failed. " + str(e), 500


retrieve_course = api.parser()
retrieve_course.add_argument("course_id", help="Enter course id")
@api.route("/get_course_by_id")
@api.doc(description="Get course by course id")
class GetCourse(Resource):
    @api.expect(retrieve_course)
    def get(self):
        courseID = retrieve_course.parse_args().get("course_id")
        course = Course.query.filter_by(course_ID=courseID).first()
        db.session.close()
        if course:
           return jsonify(
							{
							"code": 200,
							"data": {
								"course": [course.json()]
							}
						}
					)

        return {"code": 404, "message": "There is no such course"}, 404

@api.route("/addition", methods=["POST"])
class Addition(Resource):
    def post(self):
        data = request.json
        first = data.get("first")
        second = data.get("second")
        return first + second

@api.route("/create_course", methods=["POST"])
@api.doc(description="Create course")
class CreateCourse(Resource):
    def post(self):
        try:
            # Get the data for creating a new course from the request body
            new_course_data = request.json
            #print(new_course_data)
            new_course_name = new_course_data.get("course_Name") 

            # Assuming new_course_name is the input course name you want to check against the database
            input_course_name = new_course_name.strip()

            # Perform a case-insensitive search and remove leading/trailing spaces
            existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(input_course_name)).first()

            # Check if the course name already exists in the database
            #existing_course = Course.query.filter_by(course_Name=new_course_name).first()

            if existing_course:
                return {
                    "message": "Course name already exists"
                }, 409  # Conflict

            # Create a new course object with the data
            #new_course = Course(None, course_Name=new_course_name, course_Desc=new_course_data.get("course_Desc"), coursecat_ID=new_course_data.get("coursecat_ID"))
            new_course = Course(None, **new_course_data)

            # Add the new course to the database
            db.session.add(new_course)

            # Commit the changes to the database
            db.session.commit()

            # Return the newly created course as JSON response
            #return json.loads(json.dumps(new_course.json(), default=str)), 201
            return {
                'message': 'Course created successfully',
                'data': new_course.json()
            }, 201

        except Exception as e:
            db.session.rollback()
            #print("Error:", str(e))
            #return "Failed to create a new course: " + str(e), 500
            return {
                "message": "Failed to create a new course: " + str(e)
            }, 500

edit_course = api.parser()
@api.route("/edit_course/<int:course_id>", methods=["PUT"])
class EditCourse(Resource):
    @api.expect(edit_course)
    def put(self, course_id):

        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to edit course"
                }, 404 

            #Get the updated data from the request body 
            updated_data = request.json
            new_course_name = updated_data.get("course_Name") 
        
            course = Course.query.filter_by(course_ID=course_id).first()

            if course:
                # Assuming new_course_name is the input course name you want to check against the database
                input_course_name = new_course_name.strip()

                # Perform a case-insensitive search and remove leading/trailing spaces
                existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(input_course_name)).first()

                # Check if the course name already exists in the database
                #existing_course = Course.query.filter_by(course_Name=new_course_name).first()

                if existing_course:
                    return {
                        "message": "Course name already exists"
                    }, 409  # Conflict

                # Update the fields based on updated_data
                for field, value in updated_data.items():
                    #print(f"Updating {field} to {value}")
                    setattr(course, field, value)

                #Commit the changes to the database 
                db.session.commit()

                #return json.loads(json.dumps(course.json(), default=str)), 200
                return {
                    "message": "Course updated successfully",
                    "data": course.json()
                }, 200

            #return json.loads(json.dumps({"message": "There is no such course"})), 404
            return {
                "message": "There is no such course"
            }, 404

        except Exception as e:
            db.session.rollback()
            #return "Failed" + str(e), 500
            return {
                "message": "Failed to create a new course: " + str(e)
            }, 500

# Student - Courses Available for Registration (Ongoing) with Filters
retrieve_unregistered_active_courses_filter = api.parser()
retrieve_unregistered_active_courses_filter.add_argument("user_id", type=int, help="Enter user ID")
retrieve_unregistered_active_courses_filter.add_argument("course_name", help="Enter course name")
retrieve_unregistered_active_courses_filter.add_argument("coursecat_id", help="Enter course category id")


@api.route("/get_unregistered_active_courses")
@api.doc(description="Get unregistered active course information")
class GetUnregisteredActiveCourses(Resource):
    @api.expect(retrieve_unregistered_active_courses_filter)
    def get(self):
        args = retrieve_unregistered_active_courses_filter.parse_args()
        user_ID = args.get("user_id")

        current_datetime = datetime.now()
        current_time = current_datetime.strftime('%H:%M:%S')

        valid_reg_statuses = ["pending", "enrolled", "not enrolled"]

        registered_course_ids = db.session.query(Registration.rcourse_ID).filter(
            Registration.user_ID == user_ID,
            Registration.reg_Status.in_(valid_reg_statuses)
        ).subquery()

        # Construct the query for unregistered courses with active course status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~RunCourse.rcourse_ID.in_(select([registered_course_ids])),
            Course.course_Status == "active",
            RunCourse.runcourse_Status == "ongoing",
            RunCourse.reg_Enddate >= current_datetime.date(),
            (RunCourse.reg_Enddate > current_datetime.date()) | (RunCourse.reg_Endtime > current_time)
        )


        # Apply additional filters based on user inputs
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)


        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Student - Courses Available for Voting (Active) with Filters
retrieve_unvoted_ongoing_courses_filter = api.parser()
retrieve_unvoted_ongoing_courses_filter.add_argument("user_id", type=int, help="Enter user ID")
retrieve_unvoted_ongoing_courses_filter.add_argument("course_name", help="Enter course name")
retrieve_unvoted_ongoing_courses_filter.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_unvoted_ongoing_courses")
@api.doc(description="Get unvoted ongoing course information")
class GetUnvotedOngoingCourses(Resource):
    @api.expect(retrieve_unvoted_ongoing_courses_filter)
    def get(self):
        args = retrieve_unvoted_ongoing_courses_filter.parse_args()
        user_ID = args.get("user_id", "")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")

        # app.logger.debug(user_ID)

        voted_course_ids = db.session.query(Interest.vote_ID).filter_by(user_ID=user_ID).subquery()

        # Construct the query for unvoted courses with ongoing vote status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).filter(
            ~VoteCourse.vote_ID.in_(select([voted_course_ids])),
            VoteCourse.vote_Status == "ongoing"
        )

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json(),
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Student Registration Search - course name, course cat, status
retrieve_registration_info_filter_search = api.parser()
retrieve_registration_info_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_registration_info_filter_search.add_argument("course_name", help="Enter course name")
retrieve_registration_info_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_registration_info_filter_search.add_argument("reg_status", help="Enter registration status")

@api.route("/get_course_registration_info_filter_search")
@api.doc(description="Get course registration information")
class GetCourseRegistrationInfo(Resource):
    @api.expect(retrieve_registration_info_filter_search)
    def get(self):
        args = retrieve_registration_info_filter_search.parse_args()
        user_ID = args.get("user_id")
        # user_id = session.get("user_id")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")
        reg_Status = args.get("reg_status", "")

        # app.logger.debug(reg_Status)

        current_datetime = datetime.now()

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            Registration
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)  \
            .filter(RunCourse.run_Enddate > current_datetime)

        if user_ID:
            query = query.filter(Registration.user_ID == user_ID)
        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)
        if reg_Status:
            query = query.filter(Registration.reg_Status == reg_Status)
        
        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    **result[3].json()
                }
                result_data.append(course_info)
            # app.logger.debug("Debug message")
            # app.logger.debug(result_data)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No matching course registration information found"})

# Student - Vote - course name, course cat, status
retrieve_vote_info_filter_search = api.parser()
retrieve_vote_info_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_vote_info_filter_search.add_argument("course_name", help="Enter course name")
retrieve_vote_info_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_vote_info_filter_search.add_argument("vote_status", help="Enter vote status")

@api.route("/get_course_vote_info_filter_search")
@api.doc(description="Get course interest information")
class GetCourseInterestInfo(Resource):
    @api.expect(retrieve_vote_info_filter_search)
    def get(self):
        args = retrieve_vote_info_filter_search.parse_args()
        user_ID = args.get("user_id")
        # user_id = session.get("user_id")
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")
        vote_Status = args.get("vote_status", "")

        # app.logger.debug(user_ID)

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            Interest, VoteCourse.vote_ID == Interest.vote_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)

        if user_ID:
            query = query.filter(Interest.user_ID == user_ID)
        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)
        if vote_Status:
            query = query.filter(VoteCourse.vote_Status == vote_Status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json()
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No matching course interest information found"})



# Student/Instructor/Trainer - Proposed - course name, course cat, status
retrieve_proposed_courses_filter_search = api.parser()
retrieve_proposed_courses_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_proposed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_proposed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_proposed_courses_filter_search.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_proposed_courses_filter_search")
@api.doc(description="Get proposed courses submitted by a user")
class GetProposedCourses(Resource):
    @api.expect(retrieve_proposed_courses_filter_search)
    def get(self):
        args = retrieve_proposed_courses_filter_search.parse_args()
        user_id = args.get("user_id")
        # user_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")
        
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            ProposedCourse
        ).select_from(ProposedCourse).join(Course, ProposedCourse.course_ID == Course.course_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)
        
        if user_id:
            query = query.filter(ProposedCourse.submitted_By == user_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)
        
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json()
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching proposed courses found"})



# Student - Completed - course name, cat
retrieve_completed_courses_filter_search = api.parser()
retrieve_completed_courses_filter_search.add_argument("user_id", type=int, help="Enter user ID")
retrieve_completed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_completed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_completed_courses_filter_search")
@api.doc(description="Get courses completed by a user")
class GetCompletedCourses(Resource):
    @api.expect(retrieve_completed_courses_filter_search)
    def get(self):
        args = retrieve_completed_courses_filter_search.parse_args()
        user_id = args.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        
        current_datetime = datetime.now()

        UserInstructor = aliased(User)
        UserStudent = aliased(User)

        query = db.session.query(
            Course,
            RunCourse,
            CourseCategory.coursecat_Name,
            UserInstructor.user_Name.label("instructor_name"),
            UserInstructor.user_Email.label("instructor_email"),
            Registration,
            exists().where(and_(
                Feedback.submitted_By == user_id,
                Feedback.rcourse_ID == RunCourse.rcourse_ID,
                Feedback.feedback_Template_ID == RunCourse.template_ID
            )).label("feedback_submitted")
        ).select_from(RunCourse).join(Course, RunCourse.course_ID == Course.course_ID) \
            .join(Registration, RunCourse.rcourse_ID == Registration.rcourse_ID) \
            .join(UserInstructor, RunCourse.instructor_ID == UserInstructor.user_ID) \
            .join(UserStudent, Registration.user_ID == UserStudent.user_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
            .filter(UserStudent.user_ID == user_id) \
            .filter(RunCourse.run_Enddate <= current_datetime) \
            .filter(Registration.reg_Status == "Enrolled")


        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[1].run_Startdate),
                    'run_Enddate': common.format_date_time(result[1].run_Enddate),
                    'run_Starttime': common.format_date_time(result[1].run_Starttime),
                    'run_Endtime': common.format_date_time(result[1].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[1].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[1].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[1].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[1].reg_Endtime),
                }

                modified_run_course = {**result[1].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    **modified_run_course,
                    "coursecat_Name": result[2],
                    "instructor_Name": result[3],
                    "instructor_Email": result[4],
                    **result[5].json(),
                    "feedback_submitted": result[6]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No completed courses found"})


# Instructor/Trainer - Voting Campaign
retrieve_voting_campaign_courses_filter_search = api.parser()
retrieve_voting_campaign_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_voting_campaign_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_voting_campaign_courses_filter_search")
@api.doc(description="Get proposed courses")
class GetVotingCampaignCourses(Resource):
    @api.expect(retrieve_voting_campaign_courses_filter_search)
    def get(self):
        args = retrieve_voting_campaign_courses_filter_search.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        
        vote_counts_subquery = db.session.query(
            VoteCourse.course_ID,
            func.count(Interest.interest_ID).label("vote_count")
        ).join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
        .group_by(VoteCourse.course_ID).subquery()
        
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            vote_counts_subquery.c.vote_count
        ).select_from(Course) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .outerjoin(vote_counts_subquery, Course.course_ID == vote_counts_subquery.c.course_ID)
        
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        
        query = query.filter(vote_counts_subquery.c.vote_count > 0)
        query = query.group_by(Course.course_ID)
        
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_count": result[2]
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching courses found"})


# Instructor/Trainer - Assigned Course
retrieve_instructor_courses_filter_search = api.parser()
retrieve_instructor_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_instructor_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_instructor_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_instructor_courses_filter_search.add_argument("runcourse_status", help="Enter run course status")

@api.route("/get_instructor_assigned_courses_filter_search")
@api.doc(description="Get courses taught by an instructor with search options")
class GetInstructorCourses(Resource):
    @api.expect(retrieve_instructor_courses_filter_search)
    def get(self):
        args = retrieve_instructor_courses_filter_search.parse_args()
        instructor_id = args.get("instructor_id", "")
        # instructor_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("runcourse_status", "")

        current_datetime = datetime.now()

        UserInstructor = aliased(User)
        # RunCourseAlias = aliased(RunCourse)
        # CourseAlias = aliased(Course)
        # CourseCategoryAlias = aliased(CourseCategory)

        query = db.session.query(
            User.user_Name,
            User.user_Email,
            RunCourse,
            Course,
            CourseCategory.coursecat_Name
        ).select_from(User) \
        .join(UserInstructor, UserInstructor.user_ID == User.user_ID) \
        .join(RunCourse, RunCourse.instructor_ID == UserInstructor.user_ID) \
        .join(Course, Course.course_ID == RunCourse.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(RunCourse.run_Enddate >= current_datetime)

        if instructor_id:
            query = query.filter(UserInstructor.user_ID == instructor_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    "user_Name": result[0],
                    "user_Email": result[1],
                    **modified_run_course,
                    **result[3].json(),
                    "coursecat_Name": result[4]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found for the given criteria"})

# Instructor/Trainer - Proposed
retrieve_staff_proposed_courses_filter_search = api.parser()
retrieve_staff_proposed_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_staff_proposed_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_staff_proposed_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")
retrieve_staff_proposed_courses_filter_search.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_instructor_proposed_courses_filter_search")
@api.doc(description="Get proposed courses submitted by a user with vote count")
class GetProposedCoursesByUser(Resource):
    @api.expect(retrieve_staff_proposed_courses_filter_search)
    def get(self):
        args = retrieve_staff_proposed_courses_filter_search.parse_args()
        user_id = args.get("instructor_id", "")
        # user_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            ProposedCourse
        ).select_from(ProposedCourse).join(Course, ProposedCourse.course_ID == Course.course_ID) \
            .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)
        
        if user_id:
            query = query.filter(ProposedCourse.submitted_By == user_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)
        
        query = query.group_by(Course.course_ID, ProposedCourse.pcourse_ID)
        results = query.all()
        db.session.close()
        
        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json()
                }
                result_data.append(course_info)
            
            return jsonify({"code": 200, "data": result_data})
        
        return jsonify({"code": 404, "message": "No matching proposed courses found"})

# Instructor/Trainer - Completed/Taught Courses
retrieve_instructor_taught_courses_filter_search = api.parser()
retrieve_instructor_taught_courses_filter_search.add_argument("instructor_id", help="Enter instructor ID")
retrieve_instructor_taught_courses_filter_search.add_argument("course_name", help="Enter course name")
retrieve_instructor_taught_courses_filter_search.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_instructor_taught_courses_filter_search")
@api.doc(description="Get courses taught by an instructor with search options")
class GetInstructorTaughtCourses(Resource):
    @api.expect(retrieve_instructor_taught_courses_filter_search)
    def get(self):
        args = retrieve_instructor_taught_courses_filter_search.parse_args()
        instructor_id = args.get("instructor_id", "")
        # instructor_id = session.get("user_id")
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")

        UserInstructor = aliased(User)

        current_datetime = datetime.now()

        query = db.session.query(
            User.user_Name,
            User.user_Email,
            RunCourse,
            Course,
            CourseCategory.coursecat_Name
        ).select_from(User) \
        .join(UserInstructor, UserInstructor.user_ID == User.user_ID) \
        .join(RunCourse, RunCourse.instructor_ID == UserInstructor.user_ID) \
        .join(Course, Course.course_ID == RunCourse.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(RunCourse.run_Enddate < current_datetime)

        if instructor_id:
            query = query.filter(UserInstructor.user_ID == instructor_id)
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)


        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                }
                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    "user_Name": result[0],
                    "user_Email": result[1],
                    **modified_run_course,
                    **result[3].json(),
                    "coursecat_Name": result[4]
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No ended courses found for the given criteria"})

# Admin - All Proposal - Submitted
retrieve_all_submitted_proposed_courses_admin = api.parser()
retrieve_all_submitted_proposed_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_submitted_proposed_courses_admin.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_all_submitted_proposed_courses_admin")
@api.doc(description="Get all proposed courses (Admin)")
class GetAllProposedCoursesAdmin(Resource):
    @api.expect(retrieve_all_submitted_proposed_courses_admin)
    def get(self):
        args = retrieve_all_submitted_proposed_courses_admin.parse_args()
        course_Name = args.get("course_name", "")
        coursecat_ID = args.get("coursecat_id", "")

        # app.logger.debug(coursecat_ID)

        query = db.session.query(
            ProposedCourse,
            User.user_Name.label("submitted_by_name"),
            Course,
            CourseCategory.coursecat_Name
        ).select_from(ProposedCourse) \
        .join(User, ProposedCourse.submitted_By == User.user_ID) \
        .join(Course, ProposedCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(ProposedCourse.pcourse_Status != "Approved") \
        .filter(ProposedCourse.pcourse_Status != "Rejected")

        if course_Name:
            query = query.filter(Course.course_Name.contains(course_Name))
        if coursecat_ID:
            query = query.filter(Course.coursecat_ID == coursecat_ID)

        results = query.all()
        db.session.close()

        # app.logger.debug(results)

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "submitted_by": result[1],
                    **result[2].json(),
                    "coursecat_Name": result[3]
                }
               
                result_data.append(course_info)
                

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No proposed courses found"})
    

# Admin- All Proposal - Approved/Rejected
retrieve_all_app_rej_proposed_courses_admin = api.parser()
retrieve_all_app_rej_proposed_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_app_rej_proposed_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_app_rej_proposed_courses_admin.add_argument("pcourse_status", help="Enter proposed course status")

@api.route("/get_all_app_reg_proposed_courses_admin")
@api.doc(description="Get all proposed courses (Admin)")
class GetAllProposedCoursesAdmin(Resource):
    @api.expect(retrieve_all_app_rej_proposed_courses_admin)
    def get(self):
        args = retrieve_all_app_rej_proposed_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        pcourse_status = args.get("pcourse_status", "")

        # app.logger.debug(pcourse_status)

        query = db.session.query(
            ProposedCourse,
            User.user_Name.label("submitted_by_name"),
            Course,
            CourseCategory.coursecat_Name
        ).select_from(ProposedCourse) \
        .join(User, ProposedCourse.submitted_By == User.user_ID) \
        .join(Course, ProposedCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .filter(
            (ProposedCourse.pcourse_Status == "Approved") |
            (ProposedCourse.pcourse_Status == "Rejected")
        )

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if pcourse_status:
            query = query.filter(ProposedCourse.pcourse_Status == pcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                proposed_course_info = {
                    **result[0].json(),
                    "submitted_by_name": result[1],
                    **result[2].json(),
                    "coursecat_Name": result[3]
                }
                # app.logger.debug(proposed_course_info)
                result_data.append(proposed_course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No proposed courses found"})
    
#  Admin - All Voting Campaign
retrieve_all_voting_campaign_courses_admin = api.parser()
retrieve_all_voting_campaign_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_voting_campaign_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_voting_campaign_courses_admin.add_argument("vote_status", help="Enter course category id")

@api.route("/get_all_voting_courses_admin")
@api.doc(description="Get all voting courses (Admin)")
class GetAllVotingCoursesAdmin(Resource):
    @api.expect(retrieve_all_voting_campaign_courses_admin)
    def get(self):
        args = retrieve_all_voting_campaign_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        vote_status = args.get("vote_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status,
            ProposedCourse
        ).select_from(VoteCourse) \
        .join(Course, VoteCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .join(ProposedCourse, Course.course_ID == ProposedCourse.course_ID) \
        .filter(
            (VoteCourse.vote_Status == "Offered") |
            (VoteCourse.vote_Status == "Closed") |
            (VoteCourse.vote_Status == "Ongoing")
        )
        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if vote_status:
            query = query.filter(VoteCourse.vote_Status == vote_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2],
                    **result[3].json()
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No voting courses found"})
    
#  Admin - All Voting Campaign - Deleted
retrieve_all_voting_courses_admin = api.parser()
retrieve_all_voting_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_voting_courses_admin.add_argument("coursecat_id", help="Enter course category id")

@api.route("/get_all_not_offered_courses_admin")
@api.doc(description="Get all voting courses (Admin)")
class GetAllDeletedVotingCoursesAdmin(Resource):
    @api.expect(retrieve_all_voting_courses_admin)
    def get(self):
        args = retrieve_all_voting_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse.vote_Status,
            ProposedCourse
        ).select_from(VoteCourse) \
        .join(Course, VoteCourse.course_ID == Course.course_ID) \
        .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID) \
        .join(ProposedCourse, Course.course_ID == ProposedCourse.course_ID) \
        .filter(VoteCourse.vote_Status == "Not Offered")

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    "vote_Status": result[2],
                    **result[3].json()
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No voting courses found"})

# Admin - All Courses - All those in runcourse table with Reg Count
retrieve_all_courses_admin = api.parser()
retrieve_all_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_courses_admin.add_argument("course_status", help="Enter run course status")

@api.route("/get_all_courses_with_registration_count")
@api.doc(description="Get all courses with registration count")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_courses_admin)
    def get(self):
        args = retrieve_all_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("course_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            func.coalesce(func.count(Registration.reg_ID), 0).label("registration_count")
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).outerjoin(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID).group_by(Course.course_ID, RunCourse.rcourse_ID)

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime)
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    "registration_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})
    
retrieve_all_run_course_by_course_id_admin = api.parser()
retrieve_all_run_course_by_course_id_admin.add_argument("course_name", help="Enter course name")
retrieve_all_run_course_by_course_id_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_run_course_by_course_id_admin.add_argument("course_status", help="Enter run course status")
retrieve_all_run_course_by_course_id_admin.add_argument("course_id", help="Enter course id")
@api.route("/get_all_run_course_by_course_id")
@api.doc(description="Get all run course by course id")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_run_course_by_course_id_admin)
    def get(self):
        args = retrieve_all_run_course_by_course_id_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("course_status", "")
        course_id = args.get("course_id", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            func.coalesce(func.count(Registration.reg_ID), 0).label("registration_count")
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).outerjoin(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID).group_by(Course.course_ID, RunCourse.rcourse_ID)

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)
        if course_id:
            query = query.filter(RunCourse.course_ID == course_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    "registration_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Admin - Get All Course
retrieve_all_courses_admin = api.parser()
retrieve_all_courses_admin.add_argument("course_name", help="Enter course name")
retrieve_all_courses_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_courses_admin.add_argument("course_status", help="Enter run course status")

@api.route("/get_all_courses")
@api.doc(description="Get all run courses")
class GetAllCourses(Resource):
    @api.expect(retrieve_all_courses_admin)
    def get(self):
        args = retrieve_all_courses_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        course_status = args.get("course_status", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
        ).select_from(Course).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        )

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if course_status:
            query = query.filter(Course.course_Status == course_status)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})
    

# Cancel/Deactivate Button in adminViewCourse
deactivate_course = api.parser()
deactivate_course.add_argument("course_id", help="Enter course id")
@api.route("/deactivate_course")
@api.doc(description="Cancel or deactivate a run course")
class DeactivateCourse(Resource):
    @api.expect(deactivate_course)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to deactivate course"}, 404 

            args = deactivate_course.parse_args()
            course_id = args.get("course_id")

            current_datetime = datetime.now()
            current_time = current_datetime.strftime('%H:%M:%S')
            
            # Query the database for the RunCourse with the specified course_id
            run_course = RunCourse.query.filter_by(course_ID=course_id).first()
            course = Course.query.filter_by(course_ID=course_id).first()
            
            if run_course:
                if course.course_Status == 'Active':
                    if run_course.runcourse_Status == 'Closed':
                        # Check if there are any ongoing run courses for this course ID and date
                        ongoing_classes = RunCourse.query.filter(
                            RunCourse.course_ID == course_id
                        ).filter(RunCourse.run_Startdate <= current_datetime.date(),
                            RunCourse.run_Enddate >= current_datetime.date(),
                            RunCourse.run_Endtime >= current_time).all()
                        
                        length_of_ongoing_classes = len(ongoing_classes)
                        # app.logger.debug(length_of_ongoing_classes)

                        
                        if length_of_ongoing_classes == 0:
                            # No ongoing run courses, update the course and registration status
                            course.course_Status = 'Inactive'
                            db.session.commit()
                            db.session.close()
                            return jsonify({"code": 200, "message": "Course has been canceled or deactivated"})
                        else:
                            db.session.close()
                            return jsonify({"code": 400, "message": "Cannot deactivate. There are ongoing classes."})
                    elif run_course.runcourse_Status == 'Ongoing':
                        # Update only the course status
                        course.course_Status = 'Inactive'
                        run_course.runcourse_Status = 'Closed'
                        db.session.commit()
                        db.session.close()

                        return jsonify({"code": 200, "message": "Course has been canceled or deactivated"})
                else:
                    db.session.close()
                    return jsonify({"code": 400, "message": "Course is not active, cannot be canceled"})
            
            if course.course_Status == "Active":
                course.course_Status = 'Inactive'
                db.session.commit()
                db.session.close()
                return jsonify({"code": 200, "message": "Course has been deactivated"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "Failed: " + str(e)})

# Retire button in the adminViewRunCourse 
# when course_Status = Inactive and runcourse_Status = Closed, changed the course_Status to Retired
retire_course = api.parser()
retire_course.add_argument("course_id", help="Enter course id")
@api.route("/retire_course")
@api.doc(description="Retire a course")
class RetireCourse(Resource):
    @api.expect(retire_course)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to retire course"}, 404 

            args = retire_course.parse_args()
            courseID = args.get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()
            runCourses = RunCourse.query.filter_by(course_ID=courseID).all()

            if course:
                # Check if the course is inactive
                if course.course_Status == 'Inactive':
                    # Check if all associated run courses are closed
                    if all(runCourse.runcourse_Status == 'Closed' for runCourse in runCourses):
                        # Activate the course and commit the changes
                        course.course_Status = 'Retired'
                        db.session.commit()
                        db.session.close()
                        return jsonify({"code": 200, "message": "Course has been retired"})
                    else:
                        return jsonify({"code": 400, "message": "Course cannot be retired"})
                else:
                    return jsonify({"code": 400, "message": "There is no such run course to retire"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed. " + str(e)}), 500


# Activate button in adminviewruncourse
activate_course = api.parser()
activate_course.add_argument("course_id", help="Enter course id")
@api.route("/activate_course")
@api.doc(description="Activate a course")
class ActivateCourse(Resource):
    @api.expect(activate_course)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to activate course"}, 404 

            args = activate_course.parse_args()
            courseID = args.get("course_id")
            
            course = Course.query.filter_by(course_ID=courseID).first()
            runCourses = RunCourse.query.filter_by(course_ID=courseID).all()
            
            if course:
                # Check if the course is inactive
                if course.course_Status == 'Inactive':
                    # Check if all associated run courses are closed
                    if all(runCourse.runcourse_Status == 'Closed' for runCourse in runCourses):
                        # Activate the course and commit the changes
                        course.course_Status = 'Active'
                        db.session.commit()
                        db.session.close()
                        return jsonify({"code": 200, "message": "Course has been activated"})
                    else:
                        return jsonify({"code": 400, "message": "Course cannot be activated because not all run courses are closed"})
                else:
                    return jsonify({"code": 400, "message": "There is no such run course to activate"})
            else:
                return jsonify({"code": 404, "message": "There is no such run course"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "Failed. " + str(e)})


add_interest = api.parser()
add_interest.add_argument("vote_ID", help="Vote ID")
add_interest.add_argument("user_ID", help="User ID")
@api.route('/add_interest', methods=["POST"])
@api.doc(description="Add Interest For Course")
class AddInterest(Resource):
    @api.expect(add_interest)
    def post(self):
        try:
            args = add_interest.parse_args()
            voteID = args.get("vote_ID")
            userID = args.get("user_ID")

            interestList = Interest.query.filter(Interest.interest_ID.contains("")).all()
            finalInterest = interestList[-1]
            interestID = finalInterest.interest_ID

            newInterest = Interest(interestID+1, voteID, userID)
            
            course = VoteCourse.query.filter_by(vote_ID = voteID).first()
            courseID = course.course_ID
            Proposedcourse = ProposedCourse.query.filter_by(course_ID=courseID).first()
            votecount = Interest.query.filter_by(vote_ID = voteID).count()
            Proposedcourse.voteCount = votecount + 1
            db.session.add(newInterest)
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"Express Interest Successfully! Please refer to your profile to find out the status of the course."}, default=str)), 200
        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500



delete_interest = api.parser()
delete_interest.add_argument("vote_ID", help="Vote ID")
delete_interest.add_argument("user_ID", help="User ID")
@api.route('/delete_interest')
@api.doc(description="Delete Interest for Course")
class DeleteInterest(Resource):
    @api.expect(delete_interest)
    def post(self):
        try: 
            args = delete_interest.parse_args()
            voteID = args.get("vote_ID")
            userID = args.get("user_ID")
            interest_record = Interest.query.filter_by(vote_ID=voteID, user_ID=userID).first()
            if userID != str(interest_record.user_ID):
                return json.loads(json.dumps({"message": "User id is different"})), 404

            course = VoteCourse.query.filter_by(vote_ID = voteID).first()
            courseID = course.course_ID
            Proposedcourse = ProposedCourse.query.filter_by(course_ID=courseID).first()
            votecount = Interest.query.filter_by(vote_ID = voteID).count()
            Proposedcourse.voteCount = votecount - 1
            db.session.delete(interest_record)                                 
            db.session.commit()
            db.session.close()
            return json.loads(json.dumps({"message":"Unvote Interest Successfully! Please refer to View Course page to find out more courses."}, default=str)), 200
        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500

# Soft delete vote - Update status to Not Offered
update_vote_status_parser = api.parser()
update_vote_status_parser.add_argument("course_ID", type=int, help="Course ID")

@api.route('/update_vote_unoffered_course')
@api.doc(description="Update Vote Status in VoteCourse Table to 'Not Offered'")
class UpdateVoteStatus(Resource):
    @api.expect(update_vote_status_parser)
    def put(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to reject proposed course"}, 404 

            args = update_vote_status_parser.parse_args()
            course_ID = args.get("course_ID")

            # Find the corresponding VoteCourse record by course ID.
            vote_course = VoteCourse.query.filter_by(course_ID=course_ID).first()

            if vote_course is None:
                return {"message": "VoteCourse record not found for the specified course"}, 404

            # Update the vote_Status to 'Not Offered'.
            vote_course.vote_Status = 'Not Offered'
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"You have delete the course successfully. Please refer to 'Deleted Course' Tab."}, default=str)), 200

        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500
        
# Close Voting
close_vote_course_parser = api.parser()
close_vote_course_parser.add_argument("course_ID", type=int, help="Course ID")

@api.route('/close_vote_course')
@api.doc(description="Close Voting")
class CloseVoteCourse(Resource):
    @api.expect(close_vote_course_parser)
    def put(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to close vote course"}, 404 

            args = close_vote_course_parser.parse_args()
            course_ID = args.get("course_ID")

            vote_course = VoteCourse.query.filter_by(course_ID=course_ID).first()

            if vote_course is None:
                return {"message": "VoteCourse record not found for the specified course"}, 404

            vote_course.vote_Status = 'Closed'
            db.session.commit()
            db.session.close()

            return json.loads(json.dumps({"message":"You have closed the course. The course is not available for voting now."}, default=str)), 200

        except Exception as e:
            db.session.rollback()
            return json.loads(json.dumps({"message": "Failed" + str(e)})), 500


# update run course by admin
admin_update_course = {
    "course_Name": fields.String(description="Course Name", required=True),
    "course_Desc": fields.String(description="Course Description", required=True),
    "coursecat_ID": fields.Integer(description="Course Category ID", required=True),
}

@api.route('/admin_update_course/<int:course_id>', methods=['PUT'])
@api.doc(description="Admin Update Course")
class AdminUpdateRunCourse(Resource):
    @api.expect(admin_update_course)
    def put(self, course_id):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unathorized Access, Failed to create course"}, 404 

            data = request.get_json()
            course_name = data.get('course_Name')
            course_desc = data.get('course_Desc')
            coursecat_ID = data.get('coursecat_ID')

            course = Course.query.get(course_id)

            if course is None:
                return jsonify({"message": "course not found", "code": 404}), 404

            course.course_Name = course_name
            course.course_Desc = course_desc
            course.coursecat_ID = coursecat_ID

            db.session.commit()
            db.session.close()

            return jsonify({"message": "course updated successfully", "code": 200})

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to update course: {str(e)}", "code": 500})

combined_search_parser = api.parser()
combined_search_parser.add_argument("course_name", help="Enter course name", location="args")
combined_search_parser.add_argument("coursecat_id", help="Enter course category id", location="args")

@api.route("/user_courses/<int:user_id>")
class GetUserCourses(Resource):
    @api.expect(combined_search_parser)
    def get(self, user_id):
        try:
            print(user_id)
            args = combined_search_parser.parse_args()
            course_name = args.get("course_name")
            coursecat_id = args.get("coursecat_id")

            # Base query to retrieve enrolled courses for the user
            base_query = db.session.query(
                Course, CourseCategory, RunCourse, Registration, User
            ).select_from(User).join(
                Registration,
                Registration.user_ID == User.user_ID
            ).join(
                RunCourse,
                RunCourse.rcourse_ID == Registration.rcourse_ID
            ).join(
                Course,
                Course.course_ID == RunCourse.course_ID
            ).join(
                CourseCategory,
                CourseCategory.coursecat_ID == Course.coursecat_ID
            ).filter(
                User.user_ID == user_id,
                Registration.reg_Status == "Enrolled"
            )

            # Apply filters if course_name and coursecat_id are provided
            if course_name:
                base_query = base_query.filter(Course.course_Name == course_name)
            if coursecat_id:
                base_query = base_query.filter(Course.coursecat_ID == coursecat_id)

            user_courses = base_query.all()

            result_data = []
            for result in user_courses:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1].coursecat_Name,
                    **modified_run_course,
                    **result[3].json(),
                    "user_Name": result[4].user_Name
                }
                result_data.append(course_info)

            return jsonify({"code": 200, "data": result_data})

        except Exception as e:
            return jsonify({"code": 500, "message": str(e)})


retrieve_all_run_course_by_course_id_admin = api.parser()
retrieve_all_run_course_by_course_id_admin.add_argument("course_name", help="Enter course name")
retrieve_all_run_course_by_course_id_admin.add_argument("coursecat_id", help="Enter course category id")
retrieve_all_run_course_by_course_id_admin.add_argument("course_status", help="Enter run course status")
retrieve_all_run_course_by_course_id_admin.add_argument("course_id", help="Enter course id")
@api.route("/get_all_run_course_by_course_id")
@api.doc(description="Get all run course by course id")
class GetAllCoursesWithRegistrationCount(Resource):
    @api.expect(retrieve_all_run_course_by_course_id_admin)
    def get(self):
        args = retrieve_all_run_course_by_course_id_admin.parse_args()
        course_name = args.get("course_name", "")
        course_category_id = args.get("coursecat_id", "")
        runcourse_status = args.get("course_status", "")
        course_id = args.get("course_id", "")

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            func.coalesce(func.count(Registration.reg_ID), 0).label("registration_count")
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).outerjoin(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID).group_by(Course.course_ID, RunCourse.rcourse_ID)

        if course_name:
            query = query.filter(Course.course_Name.contains(course_name))
        if course_category_id:
            query = query.filter(Course.coursecat_ID == course_category_id)
        if runcourse_status:
            query = query.filter(RunCourse.runcourse_Status == runcourse_status)
        if course_id:
            query = query.filter(RunCourse.course_ID == course_id)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    "registration_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Course Name
retrieve_course_name = api.parser()
retrieve_course_name.add_argument("course_id", help="Enter course id")

@api.route("/get_course_name")
@api.doc(description="Get course name")
class GetStudentName(Resource):
    @api.expect(retrieve_course_name)
    def get(self):
        args = retrieve_course_name.parse_args()
        course_id = args.get("course_id", "")

        course = Course.query.filter_by(course_ID=course_id).first()

        if course:
            course_name = course.course_Name
            print(course_name)
            return jsonify({"code": 200, "data": course_name})
        else:
            print('else')
            return jsonify({"code": 404, "message": "Course not found"})

# Student - Check if Course is Completed using user_id and rcourse_id
is_course_completed = api.parser()
is_course_completed.add_argument("rcourse_id", help="Enter rcourse id")
@api.route("/is_course_completed")
@api.doc(description="Check if Course is Completed using user_id and rcourse_id ")
class IsCourseCompleted(Resource):
    @api.expect(is_course_completed)
    def get(self):
        try:
            args = is_course_completed.parse_args()
            user_id = session.get('user_ID')
            rcourse_id = args.get("rcourse_id")
            current_datetime = datetime.now()

            # if student has existing completed course
            query = db.session.query(
                RunCourse,
                Registration
            ).select_from(RunCourse).join(
                Registration,
                Registration.rcourse_ID == RunCourse.rcourse_ID
            ).filter(
                RunCourse.rcourse_ID == rcourse_id,
                RunCourse.run_Enddate <= current_datetime,
                Registration.user_ID == user_id,
                Registration.reg_Status == 'Enrolled'
            )

            results = query.all()
            db.session.close()

            if results:
                # if student completed course, check if there is existing feedback response
                sub_query = db.session.query(
                    Feedback
                ).filter(
                    Feedback.submitted_By == user_id,
                    Feedback.rcourse_ID == rcourse_id
                )
                feedback_result = sub_query.all()
                
                if feedback_result:
                    return jsonify({"code": 200, "isCourseCompleted": True, "isFeedbackDone": True })
                else: 
                    return jsonify({"code": 200, "isCourseCompleted": True, "isFeedbackDone": False })
            else:
                return jsonify({"code": 200, "isCourseCompleted": False, "isFeedbackDone": False})

        except Exception as e:
            return jsonify({"code": 500, "message": str(e)})

# ==================== COURSE Category FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

retrieve_all_coursecat = api.parser()
retrieve_all_coursecat.add_argument("coursecat_name", help="Enter course category name")
@api.route("/get_all_coursecat")
@api.doc(description="Get all course categories")
class GetAllCoursecat(Resource):
    @api.expect(retrieve_all_coursecat)
    def get(self):
        arg = retrieve_all_coursecat.parse_args().get("coursecat_name")
        coursecat_Name = arg if arg else ""
        coursecatList = CourseCategory.query.filter(CourseCategory.coursecat_Name.contains(coursecat_Name)).all()
        db.session.close()
        if len(coursecatList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [coursecat.json() for coursecat in coursecatList]
                    }
                }
            )

        return json.loads(json.dumps({"message": "There is no such course category"}, default=str)), 404


retrieve_coursecat = api.parser()
retrieve_coursecat.add_argument("coursecat_id", help="Enter course category id")
@api.route("/get_coursecat_by_id")
@api.doc(description="Get course category by course category id")
class GetCoursecat(Resource):
    @api.expect(retrieve_coursecat)
    def get(self):
        courseID = retrieve_coursecat.parse_args().get("coursecat_id")
        coursecat = CourseCategory.query.filter_by(coursecat_ID=courseID).first()
        db.session.close()
        if coursecat:
            return json.loads(json.dumps(coursecat.json())), 200

        return json.loads(json.dumps({"message": "There is no such course category", "code": 404}, default=str))

# ==================== USER FUNCTIONS ====================#

# To get course average ratings - all and specific
average_course_ratings = api.parser()
average_course_ratings.add_argument("course_ID", help="Enter course_ID")

@api.route("/course_average_ratings")
@api.doc(description="Course specific feedback")
class CourseAverageRatings(Resource):
    def get(self):
        args = average_course_ratings.parse_args()
        course_ID = args.get("course_ID", "")

        keywords = ['rate', 'course']  # Define keywords to identify relevant questions

        try:
            total_ratings = []
            total_questions = 0

            # To retrieve relevant questions and calculate average rating
            relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
                .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
                .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
                .join(RunCourse, RunCourse.rcourse_ID == Feedback.rcourse_ID) \
                .join(Course, Course.course_ID == RunCourse.course_ID) \
                .filter(TemplateAttribute.input_Type == 'Likert Scale') \
                .filter(func.lower(TemplateAttribute.question).contains(keywords[0])) \
                .filter(func.lower(TemplateAttribute.question).contains(keywords[1]))

            if course_ID:
                relevant_questions = relevant_questions.filter(Course.course_ID == course_ID)  # Filter by a specific course if course_ID is provided

            for feedback_template, template_attribute in relevant_questions:
                question_id = template_attribute.template_Attribute_ID
                feedback_entries = db.session.query(Feedback) \
                    .filter(Feedback.template_Attribute_ID == question_id)

                if course_ID:
                    feedback_entries = feedback_entries.filter(Course.course_ID == course_ID)  # Filter by a specific course if course_ID is provided

                feedback_entries = feedback_entries.all()

                if feedback_entries:
                    for entry in feedback_entries:
                        # print(entry)
                        total_ratings.append(int(entry.answer))  # Assuming 'answer' contains the Likert Scale value as an integer
                        total_questions += 1
            
            total_feedback = int(total_questions / len(relevant_questions.all()))

            # Calculate the overall average rating
            if total_ratings and total_questions > 0:
                overall_average_rating = round(sum(total_ratings) / total_questions, 2)
                message = "Course ratings calculated successfully."
            else:
                overall_average_rating = 0
                message = "No ratings"

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "course_ID": course_ID,
                    "overall_average_rating": overall_average_rating,
                    "total_feedback": total_feedback
                },
                "message": message,
            }
        
        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)


# To get instructor specific average ratings
instructor_average_ratings = api.parser()
instructor_average_ratings.add_argument("instructor_ID", help="Enter instructor_ID")

@api.route("/instructor_average_ratings")
@api.doc(description="Instructor specific feedback")
class InstructorAverageRatings(Resource):
    @api.expect(instructor_average_ratings)
    def get(self):
        args = instructor_average_ratings.parse_args()
        instructor_ID = args.get("instructor_ID", "")

        keywords = ['rate', 'instructor']  # Define keywords to identify relevant questions
        try:

            total_ratings = []
            total_questions = 0

            # To retrieve relevant questions and calculate average rating
            relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
                .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
                .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
                .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                .filter(TemplateAttribute.input_Type == 'Likert Scale') \
                .filter(func.lower(TemplateAttribute.question).contains(keywords[0])) \
                .filter(func.lower(TemplateAttribute.question).contains(keywords[1]))

            if instructor_ID:  # Filter by instructor ID if provided
                relevant_questions = relevant_questions.filter(RunCourse.instructor_ID == instructor_ID)

            relevant_questions = relevant_questions.all()

            for feedback_template, template_attribute in relevant_questions:
                question_id = template_attribute.template_Attribute_ID
                feedback_entries = db.session.query(Feedback) \
                    .filter(Feedback.template_Attribute_ID == question_id)

                if instructor_ID:
                    feedback_entries = feedback_entries.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                        .filter(RunCourse.instructor_ID == instructor_ID)  # Filter by instructor ID if provided

                feedback_entries = feedback_entries.all()

                if feedback_entries:
                    for entry in feedback_entries:
                        total_ratings.append(int(entry.answer))  # assuming 'answer' contains the Likert Scale value as an integer
                        total_questions += 1

            # Calculate the instructor-specific average rating
            if total_ratings and total_questions > 0:
                instructor_average_rating = round(sum(total_ratings) / total_questions, 2)
                message = "Instructor ratings calculated successfully."
            else:
                instructor_average_rating = 0
                message = "No ratings for this instructor."

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "instructor_ID": instructor_ID,
                    "instructor_average_rating": instructor_average_rating
                },
                "message": message,
            }

        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)


def drop_col(df):
    df = df.dropna(how='all')
    values_to_drop = ["nil", "none", "-", "na", "nan", "nothing"]
    df = df[~df['answer'].isin(values_to_drop)]
    drop = ['na', 'nil']
    df = df[~df['answer'].apply(lambda x: any(word in x.lower() for word in drop))]

    df.reset_index(drop=True, inplace=True)
    return df

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return None
    
def lemmatize_token(token, pos_tag):
    tag = get_wordnet_pos(pos_tag)
    if tag is None:
        return lemmatizer.lemmatize(token)
    else:
        return lemmatizer.lemmatize(token, tag)

def preprocess_text(text_series):
    def process_text(text):
        
        text = text.lower() # Convert text to lowercase

        text = re.sub(r'[^a-zA-Z\s-]', '', text) # Remove non-alphabetic characters and split hyphenated words

        tokens = nltk.word_tokenize(text) # Tokenize text

        pos_tags = nltk.pos_tag(tokens) # Tag part of speech for each token

        lemmatized_tokens = [lemmatize_token(token, pos) for token, pos in pos_tags] # Lemmatize tokens with specified part of speech

        tokens = [token for token in lemmatized_tokens if not token in stop_words] # Remove stop words

        tokens = [token for token in tokens if len(token) >= 3] # Remove words with length less than 3 characters

        text = ' '.join(tokens) # Join tokens back into text

        return text
    
    return text_series.apply(process_text)

def tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range):
    best_n_topics = None
    best_max_df = None
    best_silhouette_score = -1

    # Split your data into training and validation sets
    X_train, X_val = train_test_split(corpus, test_size=0.2, random_state=1)

    for n_topics in n_topics_range:
        for max_df_value in max_df_range:
            # Vectorize the training data using TfidfVectorizer with the current max_df
            tfidf_vectorizer = TfidfVectorizer(max_df=max_df_value, stop_words='english')
            tfidf_matrix_train = tfidf_vectorizer.fit_transform(X_train)

            # Perform NMF with the current n_topics
            nmf_model = NMF(n_components=n_topics, random_state=1)
            nmf_matrix_train = nmf_model.fit_transform(tfidf_matrix_train)

            # Calculate silhouette score on the validation set
            tfidf_matrix_val = tfidf_vectorizer.transform(X_val)
            nmf_matrix_val = nmf_model.transform(tfidf_matrix_val)
            silhouette_avg = silhouette_score(nmf_matrix_val, labels=nmf_matrix_val.argmax(axis=1))

            # Check if the current score is better than the best score
            if silhouette_avg > best_silhouette_score:
                best_n_topics = n_topics
                best_max_df = max_df_value
                best_silhouette_score = silhouette_avg

    return best_n_topics, best_max_df, best_silhouette_score

# Get the topic for specific course or all courses
feedback_course_done_well_specific = api.parser()
feedback_course_done_well_specific.add_argument("course_ID", help="Enter course_ID")

@api.route("/feedback_course_done_well_specific")
@api.doc(description="Course-specific feedback")
class CourseDoneWellFeedback(Resource):
    @api.expect(feedback_course_done_well_specific)
    def get(self):
        # Parse the course_ID from the request arguments
        args = feedback_course_done_well_specific.parse_args()
        course_ID = args.get("course_ID", "")

        # Query the database to retrieve feedback related to the specified course (using rcourse_ID)
        if not course_ID:
            # If course_ID is empty, retrieve feedback for all courses
            course_well_query = (
                db.session.query(Feedback.answer)
                .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.question.contains('course'))
                .filter(TemplateAttribute.question.contains("done well"))
                .filter(TemplateAttribute.input_Type == 'Text')
            )
        else:
            # If course_ID is provided, filter feedback for the specific course
            course_well_query = (
                db.session.query(Feedback.answer)
                .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                .filter(RunCourse.course_ID == course_ID)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.question.contains('course'))
                .filter(TemplateAttribute.question.contains("done well"))
                .filter(TemplateAttribute.input_Type == 'Text')
            )
        
        results = course_well_query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                feedback = {
                    "answer": result[0],
                }
                result_data.append(feedback)

            # Create a Pandas DataFrame from the result_data list
            df = pd.DataFrame(result_data)
            df = drop_col(df)
            
            df['preprocessed_text'] = preprocess_text(df['answer'])
            corpus = df['preprocessed_text']

            n_topics_range = range(3, 11)
            max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
            best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range)

            tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            nmf_model = NMF(n_components=best_n_topics, random_state=1)
            nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

            feature_names = tfidf_vectorizer.get_feature_names_out()
            topic_words_list = []

            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words_indices = topic.argsort()[:-10 - 1:-1]
                top_words = [feature_names[i] for i in top_words_indices]
                top_word_probabilities = [topic[i] for i in top_words_indices]
                topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
                topic_words_list.append(topic_data)
            
            topic_words_list_formatted = []

            for topic_words in topic_words_list:
                word_data = {"wordData": topic_words}
                topic_words_list_formatted.append(word_data)

            dominant_topics = nmf_matrix.argmax(axis=1) + 1
            df['topic_number'] = dominant_topics

            # Convert the DataFrame to JSON
            response_data = df.to_dict(orient='records')

            return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

        return jsonify({"code": 404, "message": "No matching course interest information found"})

# ==================== Feedback FUNCTIONS ====================#
post_feedback_student = api.parser()
@api.route("/post_feedback_student" ,methods=["POST", "GET"])
@api.doc(description="Search if template id exists, if does get template, else create new template")
class GetTemplate(Resource):
    @api.expect(post_feedback_student)
    def post(self):
        
        new_student_feedback = request.json
        courseID = new_student_feedback.get("rcourse_id")
        templateID = new_student_feedback.get("template_id")
        userID = new_student_feedback.get("user_id")
        data = new_student_feedback.get("data")
        common_questions_data = new_student_feedback.get("common_questions_data")

        print(courseID)
        print(templateID)
        print(userID)

        def submit_common_questions(common_questions_data):
            try:
              for eachdata in common_questions_data:
                  AttributeID = eachdata.get("attribute_id")
                  answer = eachdata.get("answer")
                  NewFeedback =Feedback( None, None, userID, AttributeID, answer, courseID)
                  db.session.add(NewFeedback)
                  db.session.commit()
              return True
            except Exception as e:
                print(str(e))
                db.session.rollback()
                return False
       
        template = Feedback.query.filter(Feedback.feedback_Template_ID==templateID,Feedback.submitted_By == userID, Feedback.rcourse_ID == courseID ).first()

        if not template:
            try:
                for eachdata in data:
                   AttributeID = eachdata.get("attribute_id")
                   answer = eachdata.get("answer")
                   print(AttributeID)
                   print(answer)
                   NewFeedback =Feedback( None, templateID, userID, AttributeID, answer, courseID)
                   db.session.add(NewFeedback)
                   db.session.commit()

                submit_common_questions_success = submit_common_questions(common_questions_data)
                if (submit_common_questions_success):
                  return {"code": 200, "message": "Feedback Successfully Submitted"}, 200
                else:
                   db.session.rollback()
                   return {"code": 400, "message": "An error has occured while submitting feedback"}, 400
           
            except Exception as e:
                db.session.rollback()
                return {"code": 500, "message": "Failed" + str(e)}, 500
        else:
            db.session.rollback()
            return {"code": 409, "message": "Feedback already exists"}, 409


get_student_feedback_including_answers_and_template = api.parser()
get_student_feedback_including_answers_and_template.add_argument("rcourse_id", help="Enter rcourse id")
@api.route('/get_student_feedback_including_answers_and_template')
@api.doc(description= "get student feedback including answers and template")
class GetStudentFeedbackIncludingAnswersAndTemplate(Resource):
    @api.expect(get_student_feedback_including_answers_and_template)
    def get(self):

      def get_template(template_id):
        try:
          
          query = db.session.query(
              FeedbackTemplate,
              TemplateAttribute,
              InputOption,
          ).select_from(FeedbackTemplate).outerjoin(
              TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID
          ).outerjoin(
              InputOption, TemplateAttribute.template_Attribute_ID == InputOption.template_Attribute_ID
          ).filter(
              FeedbackTemplate.template_ID == template_id,
          ).order_by(
              asc(InputOption.position)
          )

          if template_id == None:
            query = db.session.query(
                TemplateAttribute,
                InputOption,
            ).select_from(TemplateAttribute).outerjoin(
                InputOption, TemplateAttribute.template_Attribute_ID == InputOption.template_Attribute_ID
            ).filter(
                TemplateAttribute.template_ID == None
            ).order_by(
                asc(InputOption.position)
            )

          template_query = query.all()

          template_data = {
            'feedback_template_name': None,
            'template_id': None,
            'created_on': None,
            'data': [],
          }
          
          if template_query and template_id != None:
            question_dict = {}
            for template, attribute, input_option in template_query:
              if template_data['feedback_template_name'] is None:
                template_data['feedback_template_name'] = template.template_Name
                template_data['template_id'] = template.template_ID
                template_data['created_on'] = common.format_date_time(template.created_On)
                    
              if input_option is not None:
                if attribute.question in question_dict:
                  question_dict[attribute.question]['inputOptions'].append({
                      'id': input_option.input_Option_ID,
                      'position': input_option.position,
                      'option': input_option.textlabel
                  })
                else:
                  question_data = {
                    'question': attribute.question,
                    'selectedInputType': attribute.input_Type,
                    'attribute_id': attribute.template_Attribute_ID,
                    'inputOptions': [{
                        'id': input_option.input_Option_ID,
                        'position': input_option.position,
                        'option': input_option.textlabel
                    }],
                  }
                  question_dict[attribute.question] = question_data
              elif attribute is not None:
                question_data = {
                  'question': attribute.question,
                  'selectedInputType': attribute.input_Type,
                  'attribute_id': attribute.template_Attribute_ID
                }
                question_dict[attribute.question] = question_data
            template_data['data'] = list(question_dict.values())
            return {"code": 200, "template": template_data}, 200
          elif template_query and template_id == None :
            question_dict = {}
            if template_query:
              for attribute, input_option in template_query:
                if input_option is not None:
                  if attribute.question in question_dict:
                    question_dict[attribute.question]['inputOptions'].append({
                        'id': input_option.input_Option_ID,
                        'position': input_option.position,
                        'option': input_option.textlabel
                    })
                  else:
                    question_data = {
                      'question': attribute.question,
                      'selectedInputType': attribute.input_Type,
                      'attribute_id': attribute.template_Attribute_ID,
                      'inputOptions': [{
                          'id': input_option.input_Option_ID,
                          'position': input_option.position,
                          'option': input_option.textlabel
                      }],
                    }
                    question_dict[attribute.question] = question_data
                elif attribute is not None:
                  question_data = {
                    'question': attribute.question,
                    'selectedInputType': attribute.input_Type,
                    'attribute_id': attribute.template_Attribute_ID
                  }
                  question_dict[attribute.question] = question_data
                common_questions_list = list(question_dict.values())
            return {"code": 200, "template": common_questions_list}, 200
          else:
              return {"code": 400, "message": "There is no such template"}, 404
        except Exception as e :
              print(str(e))
              return {"code": 404, "message": 'template' + str(e)}, 404
      
      def get_answer(template_id, submitted_by, template_attribute_id, rcourse_id):
        try:
          query = db.session.query(
              Feedback,
          ).filter(
              Feedback.submitted_By == submitted_by,
              Feedback.rcourse_ID == rcourse_id,
              Feedback.feedback_Template_ID == template_id,
              Feedback.template_Attribute_ID == template_attribute_id
          )
          answer = query.first()
          if answer:
            return {"code": 200, "answer": answer.answer}, 200
          else:
            return {"code": 200, "answer": ''}, 200
          # else:
          #   return {"code": 400, "message": "There was an error retrieving feedback answers"}, 400
        except Exception as e :
              print(str(e))
              return {"code": 404, "message": 'answer ' + str(e)}, 404

      try:
        args = get_student_feedback_including_answers_and_template.parse_args()
        user_id = session.get("user_ID")
        rcourse_id = args.get("rcourse_id")
        query = db.session.query(
            Feedback,
        ).filter(
            Feedback.submitted_By == user_id,
            Feedback.rcourse_ID == rcourse_id
        )
        feedback = query.all()
        template_id = feedback[0].feedback_Template_ID
        template_response, _  = get_template(template_id)
        common_response, _  = get_template(None)
        if template_response['code'] == 200 and common_response['code'] == 200:
           common_questions = common_response['template']
           questions = template_response['template']['data']
           template_id = template_response['template']['template_id']
           for question in questions:
              answer_response , _ = get_answer(template_id, user_id, question['attribute_id'], rcourse_id)
              if answer_response['code'] == 200:
                question['answer'] = answer_response['answer']
              else:
                 return answer_response
           for common_question in common_questions:
              answer_response , _ = get_answer(None, user_id, common_question['attribute_id'], rcourse_id)
              if answer_response['code'] == 200:
                common_question['answer'] = answer_response['answer']
              else:
                 return answer_response
        else:
           return template_response

        db.session.close()
        return {"code": 200, "question_response": template_response['template'], "common_question_response": common_questions}, 200

      except Exception as e:
        print(str(e))
        return {"code": 404, "message": "Failed" + str(e)}, 404
      

# ==================== USER FUNCTIONS ====================#
# get_all_templates()
# get_template_by_id()


get_all_templates = api.parser()
@api.route("/get_all_templates")
@api.doc(description="Get all feedback templates")
class GetAllTemplates(Resource):
    @api.expect(get_all_templates)
    def get(self):
      templates = FeedbackTemplate.query.all()

      if templates:
        for template in templates: 
          template_id = template.template_ID
          template.existingFeedback = False 
          existingFeedback = db.session.query(Feedback).filter(Feedback.feedback_Template_ID == template_id).first()
          if existingFeedback != None:
             template.existingFeedback = True

          if not template.existingFeedback:
            courses_using_template = RunCourse.query.filter_by(template_ID = template.template_ID).all()
            if courses_using_template:
              for course in courses_using_template:
                  if datetime.now().date() > course.run_Startdate: #TO CAHNGE TO FEEDBACK START DATE
                    template.existingFeedback = True
                  elif datetime.now().date() > course.run_Enddate: #TO CAHNGE TO FEEDBACK START DATE:
                    template.existingFeedback = True
        db.session.close()
        templates_json = [template.json() for template in templates]
        templates_json = [{'template_ID': template.template_ID, 'template_Name': template.template_Name, 'created_On': common.format_date_time(template.created_On),'existingFeedback': template.existingFeedback} for template in templates]
        return {"code": 200, "templates": templates_json}, 200

      return {"code": 404, "message": "No templates found"}, 404

get_template_by_id = api.parser()
get_template_by_id.add_argument("template_id", help="Enter template id")
@api.route("/get_template_by_id")
@api.doc(description="Get template by tempate id")
class GetTemplate(Resource):
    @api.expect(get_template_by_id)
    def get(self):
      try:
        templateID = get_template_by_id.parse_args().get("template_id")
        query = db.session.query(
            FeedbackTemplate,
            TemplateAttribute,
            InputOption,
        ).select_from(FeedbackTemplate).outerjoin(
            TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID
        ).outerjoin(
            InputOption, TemplateAttribute.template_Attribute_ID == InputOption.template_Attribute_ID
        ).filter(
            or_(
              FeedbackTemplate.template_ID == templateID,
              FeedbackTemplate.template_ID == None
            )
        ).order_by(
            asc(InputOption.position)
        )
        template_query = query.all()
        db.session.close()

        template_data = {
          'feedback_template_name': None,
          'template_id': None,
          'created_on': None,
          'data': [],
        }
        question_dict = {}
        
        if template_query:
          for template, attribute, input_option in template_query:
            if template_data['feedback_template_name'] is None:
              template_data['feedback_template_name'] = template.template_Name
              template_data['template_id'] = template.template_ID
              template_data['created_on'] = common.format_date_time(template.created_On)
                  
            if input_option is not None:
              if attribute.question in question_dict:
                question_dict[attribute.question]['inputOptions'].append({
                    'id': input_option.input_Option_ID,
                    'position': input_option.position,
                    'option': input_option.textlabel
                })
              else:
                question_data = {
                  'question': attribute.question,
                  'selectedInputType': attribute.input_Type,
                  'attribute_id': attribute.template_Attribute_ID,
                  'inputOptions': [{
                      'id': input_option.input_Option_ID,
                      'position': input_option.position,
                      'option': input_option.textlabel
                  }],
                }
                question_dict[attribute.question] = question_data
            elif attribute is not None:
              question_data = {
                'question': attribute.question,
                'selectedInputType': attribute.input_Type,
                'attribute_id': attribute.template_Attribute_ID
              }
              question_dict[attribute.question] = question_data
          template_data['data'] = list(question_dict.values())
          return {"code": 200, "data": {"template": template_data}}, 200
        else:
            return {"code": 400, "message": "There is no such template"}, 404
      except Exception as e :
            print(str(e))
            return {"code": 404, "message": str(e)}, 404
    
@api.route("/post_feedback_template", methods=["POST"])
@api.doc(description="Post feedback template attribute")
class CreateFeedbackTemplate(Resource):
    def post(self):
        user_role = common.getUserRole()
        if (user_role) != 'Admin':
          return {"message": "Unauthorized Access, Failed to create feedback template"}, 404
 
        req = request.json
        templateName = req.get("feedback_template_name")
        currentDate = datetime.now().strftime('%Y-%m-%d')

        NewFeedbackTemplate = FeedbackTemplate(None, templateName, currentDate)

        try:
            db.session.add(NewFeedbackTemplate)
            db.session.commit()

        except Exception as e:
          return {"code": 500, "message": "Failed to create feedback template: "}, 500
        
        templateID = NewFeedbackTemplate.json().get("template_ID")

        try:
            attributeList = req.get("data")
            
            for attribute in attributeList:
                position = 1
                question = attribute.get("question")
                inputType = attribute.get("selectedInputType")

                TemplateAttributeList = TemplateAttribute.query.filter(TemplateAttribute.template_Attribute_ID.contains("")).all()
                finalAttribute = TemplateAttributeList[-1]
                templateAttributeID = finalAttribute.template_Attribute_ID + 1

                newTemplateAttribute = TemplateAttribute(template_Attribute_ID=templateAttributeID, question=question, input_Type=inputType, template_ID=templateID)
                db.session.add(newTemplateAttribute)

                # commit first to fulfil foreign key constraint
                db.session.commit()

                if inputType == "Likert Scale" or inputType == "Radio Button" or inputType == "Single Select":
                    inputOptions = attribute.get("inputOptions")

                    for inputOption in inputOptions:
                        textlabel = inputOption.get("option")

                        newInputOption = InputOption(templateAttributeID, position, textlabel)
                        db.session.add(newInputOption)

                        position += 1

                # Commit the changes to the database
                db.session.commit()

            return {"code": 200, "message": "Feedback Template successfully created"}, 200
        
        except Exception as e:
          return {"code": 500, "message": str(e)}, 500
        
        


get_courses_by_template_id = api.parser()
get_courses_by_template_id.add_argument("template_id", help="Enter template id")
@api.route("/get_courses_by_template_id")
@api.doc(description="Get Courses by tempate id")
class GetCoursesByTemplateId(Resource):
    @api.expect(get_courses_by_template_id)
    def get(self):
      try:
        templateID = get_courses_by_template_id.parse_args().get("template_id")
        query = db.session.query(
            FeedbackTemplate,
            RunCourse, 
            Course
        ).select_from(FeedbackTemplate).outerjoin(
            RunCourse, FeedbackTemplate.template_ID == RunCourse.template_ID
        ).join(
            Course, RunCourse.course_ID == Course.course_ID  
        ).filter(
           or_(
              FeedbackTemplate.template_ID == templateID,
              FeedbackTemplate.template_ID == None
            )
        )
        query_results = query.all()
        db.session.close()
        courses = []
        if query_results:
          for _, runcourse, course in query_results:
            if runcourse is not None:
              courses.append({
                "course_Name": course.course_Name,
                "run": [{
                  "run_Name": runcourse.run_Name,
                  "rcourse_id": runcourse.rcourse_ID
                }]
              })
        return {"code": 200, "data": {"courses": courses}}, 200
      except Exception as e:
        return {"code": 404, "message": "Failed " + str(e)}, 404

get_all_feedback_template_names = api.parser()
@api.route("/get_all_feedback_template_names")
@api.doc(description="Get all feedback template Names")
class GetAllFeedbackTemplateNames(Resource):
    @api.expect(get_all_feedback_template_names)
    def get(self):
      template_names = db.session.query(FeedbackTemplate.template_Name).all()
      db.session.close()
      
      if template_names:
        template_names_json = [template_name[0] for template_name in template_names]
        return {"code": 200, "feedback_template_names": template_names_json}, 200

      return {"code": 404, "message": "Failed to retrieve all feedback template names"}, 404
    
get_course_names_by_feedback_template_id = api.parser()
get_course_names_by_feedback_template_id.add_argument("template_id", help="Enter template id")
@api.route("/get_course_names_by_feedback_template_id")
@api.doc(description="Get course names by feedback template id")
class GetCourseNamesByFeedbackTemplateId(Resource):
    @api.expect(get_course_names_by_feedback_template_id)
    def get(self):
      try:
        templateID = get_course_names_by_feedback_template_id.parse_args().get("template_id")

        courses_using_template = (
          db.session.query(
          RunCourse
        ).filter(RunCourse.template_ID == templateID).all())

        courses_no_template = (
          db.session.query(
          RunCourse
        ).filter(RunCourse.template_ID == None).all())

        db.session.close()

        course_names_using = []
        course_name_no_template = []

        if courses_using_template:
          for runcourse in courses_using_template:
            course_names_using.append({
              "run_Name": runcourse.run_Name,
              "rcourse_id": runcourse.rcourse_ID,
              "feedback_start_date": common.format_date_time(runcourse.feedback_Startdate)
            })

        if courses_no_template:
          for runcourse in courses_no_template:
            course_name_no_template.append({
              'run_Name': runcourse.run_Name,
              'rcourse_id': runcourse.rcourse_ID,
              "feedback_start_date": common.format_date_time(runcourse.feedback_Startdate)
            })

        return {"code": 200, "course_names_using": course_names_using, "course_name_no_template": course_name_no_template}, 200

      except Exception as e:
        return {"code": 404, "message": "Failed" + str(e)}, 404
         
edit_feedback_template = api.parser()
@api.route("/edit_feedback_template/<int:template_id>", methods=["PUT"])
class EditFeedbackTemplate(Resource):
    @api.expect(edit_feedback_template)
    def put(self, template_id):

        try: 
          user_role = common.getUserRole()
          if (user_role) != 'Admin':
            return {"message": "Unauthorized Access, Failed to edit feedback template"}, 404
            #Get the updated data from the request body
            data = request.json
        
            template = FeedbackTemplate.query.filter_by(template_ID=template_id).first()

            if template == None:
              return {"code": 404, "message": "Feedback template does not exist" }, 404

            existingFeedback = db.session.query(Feedback).filter(Feedback.feedback_Template_ID == template_id).first()
            if existingFeedback != None:
              return {"code": 404, "message": "There are existing run course feedbacks using this template, unable to edit feedback template" }, 404

            courses_using_template = RunCourse.query.filter_by(template_ID = template_id).all()
            if courses_using_template:
              for course in courses_using_template:
                  if datetime.now().date() > course.run_Startdate: #TO CAHNGE TO FEEDBACK START DATE
                    return {"code": 404, "message": "There are run courses with ongoing feedback period, unable to edit feedback template" }, 404
                  elif datetime.now().date() > course.run_Enddate: #TO CAHNGE TO FEEDBACK START DATE:
                    return {"code": 404, "message": "There are run courses with past feedback period, unable to edit feedback template" }, 404

            if template:
                # if template exists, update template name and delete all attributes and options
                setattr(template, 'template_Name', data['feedback_template_name'])

                template_attributes = TemplateAttribute.query.filter_by(template_ID = template_id).all() # get all template attributes linked to the feedback       
            
                if template_attributes:
                    for template_attri in template_attributes:
                        template_attri_ID = template_attri.template_Attribute_ID
                        feedback_to_delete = Feedback.query.filter_by(template_Attribute_ID = template_attri_ID).all()
                        if feedback_to_delete:
                            for feedback in feedback_to_delete:
                                db.session.delete(feedback) # delete feedback containing template id and attribute id
                        template_attributes_options = InputOption.query.filter_by(template_Attribute_ID = template_attri_ID).all() # get all input options linked to template attributes
                        if template_attributes_options:
                            for option in template_attributes_options:
                                db.session.delete(option) #delete template attribute options                      
                        db.session.delete(template_attri)

                # Update the fields based on data
                for editAttribute in data['data']:
                    new_attribute = TemplateAttribute(question=editAttribute['question'], input_Type=editAttribute['selectedInputType'], template_ID=template_id)
                    db.session.add(new_attribute)
                    if 'inputOptions' in editAttribute:
                        template_Attribute_ID = TemplateAttribute.query.filter_by(template_ID=template_id).filter_by(question=editAttribute['question']).first().template_Attribute_ID
                        position = 1
                        for editOption in editAttribute['inputOptions']:
                            new_option = InputOption(template_Attribute_ID=template_Attribute_ID, position=position, textlabel=editOption['option'])
                            position += 1
                            db.session.add(new_option)

                #Commit the changes to the database 
                db.session.commit()

                return {"code": 200, "message": "Feedback Template successfully edited"}, 200

            return {"code": 404, "message": "There is no such feedback template"}, 404

        except Exception as e:
            print("Error:", str(e))
            return {"code": 500, "message": "Failed " + str(e) }, 500

delete_feedback_template = api.parser()
delete_feedback_template.add_argument("template_ID", help="Feedback Template ID")
@api.route('/delete_feedback_template')
@api.doc(description="Delete Feedback Template ")
class DeleteFeedbackTemplate(Resource):
    @api.expect(delete_feedback_template)
    def post(self):
      try:
        user_role = common.getUserRole()
        if (user_role) != 'Admin':
          return {"message": "Unauthorized Access, Failed to delete feedback template"}, 404

        args = delete_feedback_template.parse_args()
        templateID = args.get("template_ID")
        feedback_template = FeedbackTemplate.query.filter_by(template_ID = templateID).first() # get first feedback template
        if feedback_template == None:
           return {"code": 404, "message": "Feedback template does not exist" }, 404

        existingFeedback = db.session.query(Feedback).filter(Feedback.feedback_Template_ID == templateID).first()
        if existingFeedback != None:
           return {"code": 404, "message": "There are existing run course feedbacks using this template, unable to delete feedback template" }, 404

        courses_using_template = RunCourse.query.filter_by(template_ID = templateID).all()
        if courses_using_template:
           for course in courses_using_template:
              if datetime.now().date() > course.run_Startdate: #TO CAHNGE TO FEEDBACK START DATE
                 return {"code": 404, "message": "There are run courses with ongoing feedback period, unable to delete feedback template" }, 404
              elif datetime.now().date() > course.run_Enddate: #TO CAHNGE TO FEEDBACK START DATE:
                 return {"code": 404, "message": "There are run courses with past feedback period, unable to delete feedback template" }, 404

        # check if feedback template in use
        feedbacks = Feedback.query.filter(Feedback.feedback_Template_ID == templateID).all()
        if feedbacks:
          for feedback in feedbacks:
              runCourseID = feedback.rcourse_ID
              IstemplateinUse = RunCourse.query.filter(RunCourse.rcourse_ID ==runCourseID, RunCourse.runcourse_Status == "Ongoing").first()
              if IstemplateinUse:
                  return {"code": 404, "message": "Failed the feedback template is in use" }, 404
     
        # runningcourse = RunCourse.query.filter(RunCourse.template_ID == templateID, RunCourse.runcourse_Status == "Ongoing").all()
        # if runningcourse:
        #    return {"code": 404, "message": "Failed the feedback template is in use" }, 404
        # allrunningcourrse = RunCourse.query.filter_by(template_ID = templateID).all()
        # for runcourse in allrunningcourrse:
        #    runcourse.template_ID = None

        if feedback_template:
            course_to_change = RunCourse.query.filter_by(template_ID = templateID)
            for course in course_to_change:
               course.template_ID = None
          
            template_attributes = TemplateAttribute.query.filter_by(template_ID = templateID).all() # get all template attributes linked to the feedback       
            
            if template_attributes:
                for template_attri in template_attributes:
                    template_attri_ID = template_attri.template_Attribute_ID
                    feedback_to_delete = Feedback.query.filter_by(template_Attribute_ID = template_attri_ID).all()
                    if feedback_to_delete:
                        for feedback in feedback_to_delete:
                            db.session.delete(feedback) # delete feedback containing template id and attribute id
                    template_attributes_options = InputOption.query.filter_by(template_Attribute_ID = template_attri_ID).all() # get all input options linked to template attributes
                    if template_attributes_options:
                        for option in template_attributes_options:
                            db.session.delete(option) #delete template attribute options                      
                    db.session.delete(template_attri)                                        
        db.session.commit()
        if feedback_template:
            db.session.delete(feedback_template)
            db.session.commit()

        return {"code": 200, "message": "Delete Feedback Template Successfully"}, 200
      except Exception as e:
        return {"code": 404, "message": "Failed " + str(e)}, 404

    

get_feedback_template_records = api.parser()
get_feedback_template_records.add_argument("template_ID", help="Feedback Template ID")
get_feedback_template_records.add_argument("user_ID", help="User ID")
get_feedback_template_records.add_argument("rcourse_ID", help="Run course ID")
@api.route('/get_feedback_template_records')
@api.doc(description= "get feedback records")
class GetFeedbackTemplateRecords(Resource):
    @api.expect(get_feedback_template_records)
    def post(self):
        args = get_feedback_template_records.parse_args()
        templateID = args.get('template_ID')
        userID = args.get('user_ID')
        rcourseID = args.get('rcourse_ID')
        feedback = Feedback.query.filter( Feedback.rcourse_ID == rcourseID, Feedback.feedback_Template_ID == templateID, Feedback.submitted_By == userID).all()
        if feedback:
          eachfeedback_json = [eachfeedback.json() for eachfeedback in feedback]
          return {"code": 200, "feedback": eachfeedback_json}, 200

        return {"code": 404, "message" : "feedback does not exist for this rcourse"},404


@api.route("/apply_feedback_template_to_courses", methods=["POST"])
@api.doc(description="Apply Feedback Template to Courses")
class ApplyFeedbackTemplateToCourses(Resource):
    def post(self):
        user_role = common.getUserRole()
        if (user_role) != 'Admin':
            return {"message": "Unauthorized Access, Failed to edit feedback template"}, 404
  
        req = request.json
        templateID = req.get("template_ID")
        included_courses = req.get("included_courses")
        not_included_courses = req.get("not_included_courses")

        errorCourseRecord = []

        def update_course_template(course_list, template_id, included_course):
            if included_course:
              haveError = False
              for course in course_list:
                  course_record = RunCourse.query.filter(RunCourse.rcourse_ID == course['rcourse_id']).first()
                  if course_record:
                      if course_record.template_ID == template_id:
                         haveError = False
                      elif course_record.template_ID != template_id and course_record.feedback_Startdate > datetime.now().date(): 
                        course_record.template_ID = template_id
                        haveError = False
                      else:
                        errorCourseRecord.append(course_record.run_Name) 
                        haveError = True
                  else:
                      haveError = True
              return haveError
            else:
              haveError = False
              for course in course_list:
                course_record = RunCourse.query.filter(RunCourse.rcourse_ID == course.get("rcourse_id")).first()
                if course_record:
                      course_record.template_ID = None
                      db.session.commit()
                else:
                    haveError = True
              return haveError
        try:
            have_error_included = update_course_template(included_courses, templateID, True)
            have_error_not_included = update_course_template(not_included_courses, None, False)

            if have_error_included == False and have_error_not_included == False:
                db.session.commit()
                return {"code": 200, "message": "Successfully apply feedback template to course(s)"}, 200
            else:
                db.session.rollback()
                if errorCourseRecord:
                  error_message = "Could not apply feedback template to the following courses: " + ", ".join(errorCourseRecord)
                  return {"code": 404, "message": error_message}, 404

                return {"code": 404, "message": "Course(s) not found, unable to apply feedback template to course(s)"}, 404

        except Exception as e:
            db.session.rollback()
            return {"code": 500, "message": "Failed " + str(e)}, 500


get_feedback_template_common_questions = api.parser()
@api.route('/get_feedback_template_common_questions')
@api.doc(description= "get feedback template common questions")
class GetFeedbackTemplateCommonQuestions(Resource):
    @api.expect(get_feedback_template_common_questions)
    def get(self):
      try:
        query = db.session.query(
            TemplateAttribute,
            InputOption,
        ).select_from(TemplateAttribute).outerjoin(
            InputOption, TemplateAttribute.template_Attribute_ID == InputOption.template_Attribute_ID
        ).filter(
            TemplateAttribute.template_ID == None
        ).order_by(
            asc(InputOption.position)
        )
        common_questions = query.all()
        db.session.close()

        if common_questions:
          question_dict = {}
          if common_questions:
            for attribute, input_option in common_questions:
              if input_option is not None:
                if attribute.question in question_dict:
                  question_dict[attribute.question]['inputOptions'].append({
                      'id': input_option.input_Option_ID,
                      'position': input_option.position,
                      'option': input_option.textlabel
                  })
                else:
                  question_data = {
                    'question': attribute.question,
                    'selectedInputType': attribute.input_Type,
                    'attribute_id': attribute.template_Attribute_ID,
                    'inputOptions': [{
                        'id': input_option.input_Option_ID,
                        'position': input_option.position,
                        'option': input_option.textlabel
                    }],
                  }
                  question_dict[attribute.question] = question_data
              elif attribute is not None:
                question_data = {
                  'question': attribute.question,
                  'selectedInputType': attribute.input_Type,
                  'attribute_id': attribute.template_Attribute_ID
                }
                question_dict[attribute.question] = question_data
            common_questions_list = list(question_dict.values())
            return {"code": 200, "common_questions": common_questions_list}, 200

        return {"code": 404, "message": "Failed to retrieve common questions"}, 404

      except Exception as e:
        return {"code": 404, "message": "Failed" + str(e)}, 404

# ==================== PROPOSED COURSE FUNCTIONS ====================#
# get_all_courses()
# get_all_courses_hr()
# get_course_by_id()
# create_new_course()

retrieve_all_proposedcourses = api.parser()
retrieve_all_proposedcourses.add_argument("course_id", help="Enter course id")
@api.route("/get_all_proposedcourses")
@api.doc(description="Get all proposed courses")
class GetAllProposedCourses(Resource):
  @api.expect(retrieve_all_proposedcourses)
  def get(self):
    arg = retrieve_all_proposedcourses.parse_args().get("course_id")
    course_id = arg if arg else ""
    if course_id == "":
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.course_ID.contains(course_id)).all()
    else:
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.course_ID.like(course_id)).all()
    db.session.close()
    if len(proposedCourseList):
      return jsonify(
        {
          "code": 200,
          "data": {
            "course": [course.json() for course in proposedCourseList]
          }
        }
      )
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

retrieve_proposed_course = api.parser()
retrieve_proposed_course.add_argument("course_id", help="Enter course id")

@api.route("/get_proposed_course_by_course_id")
@api.doc(description="Get proposed course by course id")
class GetProposedCourse(Resource):
    @api.expect(retrieve_proposed_course)
    def get(self):
        courseID = retrieve_proposed_course.parse_args().get("course_id")
        proposed_course = ProposedCourse.query.filter_by(course_ID=courseID).first()
        if proposed_course:
            course = Course.query.get(proposed_course.course_ID)
            course_category = CourseCategory.query.get(course.coursecat_ID)
            db.session.close()

            response_data = {
                "course_ID": course.course_ID,
                "course_Name": course.course_Name,
                "course_Desc": course.course_Desc,
                "coursecat_ID": course.coursecat_ID,
                "coursecat_Name": course_category.coursecat_Name,
                "pcourse_ID": proposed_course.pcourse_ID
            }
            
            return jsonify(
                {
                    "code": 200,
                    "data": response_data
                }
            )

        db.session.close()
        return jsonify({"message": "There is no such course", "code": 404})
  
retrieve_proposed_course_by_status = api.parser()
retrieve_proposed_course_by_status.add_argument("pcourse_status", help="Enter pcourse_status")
@api.route("/get_proposed_course_by_pcourse_status")
@api.doc(description="Get proposed course by pcourse status")
class GetProposedCourseByStatus(Resource):
  @api.expect(retrieve_proposed_course_by_status)
  def get(self):
    arg = retrieve_proposed_course_by_status.parse_args().get("pcourse_status")
    pcourse_status = arg if arg else ""
    if pcourse_status == "":
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.pcourse_Status.contains(pcourse_status)).all()
    else:
      proposedCourseList = ProposedCourse.query.filter(ProposedCourse.pcourse_Status.like(pcourse_status)).all()
    db.session.close()
    if len(proposedCourseList):
      return jsonify(
        {
          "code": 200,
          "data": {
            "course": [course.json() for course in proposedCourseList]
          }
        }
      )
    return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

@api.route("/create_proposed_course", methods=["POST"])
@api.doc(description="Create proposed course")
class CreateProposedCourse(Resource):
    def post(self):
        try: 
            # Get the data for creating a new proposed course from the request body
            new_proposed_course_data = request.json

            # Create a new proposed course object with the data
            new_proposed_course = ProposedCourse(None, submitted_By=new_proposed_course_data.get("submitted_By"), course_ID=new_proposed_course_data.get("course_ID"), pcourse_Status="Pending", action_Done_By=None, proposed_Date=new_proposed_course_data.get("proposed_Date"), reason=None, voteCount=0)

            # Add the new proposed course to the database
            db.session.add(new_proposed_course)

            # Commit the changes to the database
            db.session.commit()

            # Return the newly created course as JSON response
            #return json.loads(json.dumps(new_proposed_course.json(), default=str)), 201

            new_proposed_course.proposed_Date = new_proposed_course.proposed_Date.strftime('%Y-%m-%d')

            return {
              "message": "Proposed Course created successfully",
              "data": new_proposed_course.json()
            }, 201

        except Exception as e:
          db.session.rollback()
          #return "Failed to create a new course: " + str(e), 500
          return {
            "message": "Failed to create a propsed course: " + str(e)
          }, 500

# Edit/Update Proposed Course 
update_proposed_course_model = {
    "course_Name": fields.String(description="Course Name", required=True),
    "course_Desc": fields.String(description="Course Description", required=True),
    "coursecat_ID": fields.Integer(description="Course Category ID", required=True),
}

@api.route('/update_proposed_course/<int:course_id>', methods=['PUT'])
@api.doc(description="Update Proposed Course")
class UpdateProposedCourse(Resource):
    @api.expect(update_proposed_course_model)
    def put(self, course_id):
        try:
            data = request.get_json()
            course_name = data.get('course_Name')
            course_desc = data.get('course_Desc')
            coursecat_ID = data.get('coursecat_ID')

            course = Course.query.get(course_id)
            user_id = common.getUserID()
            user_role = common.getUserRole()
            proposed_course = ProposedCourse.query.filter_by(course_ID=course_id).first()
            
            if user_id != proposed_course.submitted_By and user_role != "Admin":
                return jsonify({"message": "Unauthorized Access, no rights to edit proposed course", "code": 403})

            if course is None:
                return jsonify({"message": "Proposed course not found", "code": 404}), 404

            existing_course = Course.query.filter(func.lower(func.trim(Course.course_Name)) == func.lower(course_name)).first()

            if existing_course and course_name != course.course_Name:
                return jsonify({"message": "Course Update Unsuccessful. A course with the same name already exists.", "code": 405})
            
            
            result_data = {
               'course_Name': course_name,
               'course_Desc': course_desc,
               'coursecat_ID': coursecat_ID
            }
            result = Course.query.filter_by(course_ID=course_id).update(result_data)
            # course.course_Name = course_name
            # course.course_Desc = course_desc
            # course.coursecat_ID = coursecat_ID

            db.session.commit()
            db.session.close()

            return jsonify({"message": "Proposed course updated successfully", "code": 200})

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to update proposed course: {str(e)}", "code": 500})

        

# Delete Propose Course
delete_proposed_course = api.parser()
delete_proposed_course.add_argument("pcourse_ID", help="Proposed Course ID")

@api.route('/delete_proposed_course')
@api.doc(description="Delete Proposed Course")
class RemoveProposedCourse(Resource):
    @api.expect(delete_proposed_course)
    def delete(self):
        try:
            args = delete_proposed_course.parse_args()
            pcourse_id = args.get("pcourse_ID")

            # app.logger.debug(pcourse_id)

            # Find the proposed course by its ID.
            proposed_course = ProposedCourse.query.get(pcourse_id)
            user_id = common.getUserID()
            if (user_id) != proposed_course.submitted_By:
                return {"message": "Unathorized Access, Not owner of this proposed those"}, 404 

            if proposed_course is None:
                return {"message": "Proposed course not found"}, 404

            # Get the associated course ID.
            course_id = proposed_course.course_ID

            # Delete the proposed course.
            db.session.delete(proposed_course)
            db.session.commit()

            # Now, delete the corresponding course if it exists.
            course = Course.query.get(course_id)
            if course is not None:
              db.session.delete(course)
              db.session.commit()
              db.session.close()

            return {"message": "Proposed course deleted successfully"}

        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete proposed course: " + str(e)}, 500


reject_proposed_course_model = api.model("reject_proposed_course_model", {
    "pcourseID" : fields.Integer(description="", required=True),
    "reason" : fields.String(description="", required=True)
})
@api.route('/reject_proposed_course', methods=["POST"])
@api.doc(description="Reject Proposed Course")
class RejectProposedCourse(Resource):
  @api.expect(reject_proposed_course_model)
  def post(self):
    try:
      user_role = common.getUserRole()
      user_id = common.getUserID()
      if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to reject proposed course"}, 404 

      data = request.get_json()
      proposed_course = ProposedCourse.query.filter_by(pcourse_ID = data['pcourseID']).first()
      if proposed_course:
        proposed_course.pcourse_Status = 'Rejected'
        proposed_course.reason = data['reason']
        proposed_course.action_Done_By = user_id
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Proposed Course is successfully rejected", "code": 200})
  
      else:
        return jsonify({"message": "Course does not exist", "code": 404})

    except Exception as e:
      db.session.rollback()
      return jsonify({"message": "Failed " + str(e), "code": 500})
    

approve_proposed_course_model = api.model("accept_proposed_course_model", {
    "pcourseID" : fields.Integer(description="", required=True),
})
@api.route('/approve_proposed_course', methods=["POST"])
@api.doc(description="Approve Proposed Course")
class ApproveProposedCourse(Resource):
  @api.expect(approve_proposed_course_model)
  def post(self):
    try:
      user_role = common.getUserRole()
      if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to approve proposed course"}, 404 

      data = request.get_json()
      proposed_course = ProposedCourse.query.filter_by(pcourse_ID = data['pcourseID']).first()

      if proposed_course:
        proposed_course.pcourse_Status = 'Approved'
        newVoteCourse = VoteCourse(
          course_ID= proposed_course.course_ID,
          vote_Status='Ongoing'
        )
        db.session.add(newVoteCourse)
        db.session.commit()
        db.session.close()
      
        return jsonify({"message": "Proposed Course is successfully accepted", "code": 200})
  
      else:
        return jsonify({"message": "Course does not exist", "code": 404})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed " + str(e), "code": 500})

# ==================== REGISTRATION FUNCTIONS ====================#
# get_all_registrations()
# create_new_registration()
# update_registration()

# get_all_registrations()
get_all_registrations = api.parser()
get_all_registrations.add_argument("reg_ID", help="Enter registration ID")
@api.route("/get_all_registrations")
@api.doc(description="Gets all registrations")
class GetAllRegistrations(Resource):
    @api.expect(get_all_registrations)
    def get(self):
        arg = get_all_registrations.parse_args().get("reg_ID")
        reg_ID = arg if arg else ""
        regList = Registration.query.filter(Registration.reg_ID == reg_ID).all()
        db.session.close()

        if len(regList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reg_list": [reg.json() for reg in regList]
                    }
                }
            )
        
        return jsonify(
            {
                "code": 404,
                "message": "No such registration record exists"
            }
        )

# create_new_registration()
create_registration_model = api.model("create_registration_model", {
    "rcourse_ID" : fields.Integer(description="Run Course ID", required=True),
    "user_ID" : fields.Integer(description="User ID", required=True),
    "reg_Status" : fields.String(description="Registration status", required=True)
})

@api.route("/create_new_registration", methods=["POST"])
@api.doc(description="Creates new registration")
class CreateNewRegistration(Resource):
    @api.expect(create_registration_model)
    def post(self):
        data = request.get_json()
        print(data)
        rcourse_ID = data.get("rcourse_ID")
        user_ID = data.get("user_ID")
        session_user_ID = common.getUserID()
        if session_user_ID != user_ID:
            return {"message": "Unathorized Access, No rights to create new registration"}, 404 

        # Check if a registration with the given rcourse_ID and user_ID exists
        existing_registration = Registration.query.filter_by(rcourse_ID=rcourse_ID, user_ID=user_ID).first()

        if existing_registration:
            # If the registration exists, update its reg_Status to "pending"
            try:
                existing_registration.reg_Status = "Pending"
                db.session.commit()

                return jsonify(
                    {
                        "code": 200,
                        "data": existing_registration.json(),
                        "message": "You have successfully registered for the course again. Please refer to your profile to find out the status."
                    }
                )
            except Exception as e:
                db.session.rollback()
                return "Failed to update registration status: " + str(e), 500
        else:
            # If the registration does not exist, create a new one
            registration = Registration(**data)
            try:
                db.session.add(registration)
                db.session.commit()

                return jsonify(
                    {
                        "code": 201,
                        "data": registration.json(),
                        "message": "You have successfully registered for the course. Please refer to your profile to find out the status."
                    }
                )
            except Exception as e:
                db.session.rollback()
                return "Failed to create new registration: " + str(e), 500

#update_registration()
update_registration_model = api.model("update_registration_model", {
    "reg_ID": fields.Integer(description="Registration ID", required=True),
    "rcourse_ID" : fields.Integer(description="Run Course ID", required=True),
    "user_ID" : fields.Integer(description="User ID", required=True),
    "reg_Status" : fields.String(description="Registration status", required=True)
})

@api.route("/update_registration", methods=["PUT"])
@api.doc(description="Update registration record")
class UpdateRegistration(Resource):
    @api.expect(update_registration_model)
    def put(self):
        data = request.get_json()
        reg_ID = data["reg_ID"]
        registration = Registration.query.filter_by(reg_ID=reg_ID).first()

        if not registration:
            db.session.close()
            return jsonify(
                {
                    "code": 404,
                    "message": "No such registration record exists"
                }
            )
        
        try:
            if data["user_ID"] != registration.user_ID:
                return {"message": "Unathorized Access, No rights to update registration"}, 404 

            for key, value in data.items():
                setattr(registration, key, value)

            db.session.commit()
            db.session.close()

            return jsonify(
                {
                    "code": 201,
                    "data": registration.json(),
                    "message": "Registration has been successfully updated!"
                }
            )
        
        except Exception as e:
            db.session.rollback()
            return "Failed" + str(e), 500

#get_registration_by_userid()
get_registration_by_userid = api.parser()
get_registration_by_userid.add_argument("user_ID", help="Enter user ID")
@api.route("/get_registration_by_userid")
@api.doc(description="Gets registration by user ID")
class GetRegistrationByUserID(Resource):
    @api.expect(get_registration_by_userid)
    def get(self):
        arg = get_registration_by_userid.parse_args().get("user_ID")
        user_ID = arg if arg else ""
        session_user_ID = common.getUserID()
        if user_ID != session_user_ID:
          return {"message": "Unathorized Access, No rights to view registrations"}, 404
 
        regList = Registration.query.filter(Registration.user_ID == user_ID).all()
        db.session.close()

        if len(regList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reg_list": [reg.json() for reg in regList]
                    }
                }
            )
        
        return jsonify(
            {
                "code": 404,
                "message": "No such registration record exists"
            }
        )
    
# Drop registered course
drop_registered_course = api.parser()
drop_registered_course.add_argument("rcourse_ID", type=int, help="Run Course ID")
drop_registered_course.add_argument("user_ID", type=int, help="User ID")

@api.route('/drop_registered_course')
@api.doc(description="Update Registration Status to 'Dropped'")
class dropRegisteredCourse(Resource):
    @api.expect(drop_registered_course)
    def put(self):
        try:
            args = drop_registered_course.parse_args()
            rcourse_ID = args.get("rcourse_ID")
            user_ID = args.get("user_ID")

            registration = Registration.query.filter_by(rcourse_ID=rcourse_ID, user_ID=user_ID).first()

            if registration is None:
                return {"message": "Registration record not found for the specified course and user"}, 404

            if user_ID != registration.user_ID:
                return {"message": "Unathorized Access, No rights to update registration"}, 404 
    
            registration.reg_Status = 'Dropped'
            db.session.commit()
            db.session.close()

            return {"message": "The course has been dropped successfully."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to drop the course: " + str(e)}, 500
        
# ==================== Run COURSE FUNCTIONS ====================#
# get_all_runcourses()
# get_run_course_by_course_id()
# change_registration_status()
# create_runcourse()

# get_all_runcourses() ---------------------------------------------
retrieve_all_runcourses = api.parser()
retrieve_all_runcourses.add_argument("course_id", help="Enter course id")
@api.route("/get_all_runcourses")
@api.doc(description="Get all run courses")
class GetAllRunCourses(Resource):
    @api.expect(retrieve_all_runcourses)
    def get(self):
        arg = retrieve_all_runcourses.parse_args().get("course_id")
        course_id = arg if arg else ""
        if course_id == "":
            runCourseList = RunCourse.query.filter(RunCourse.course_ID.contains(course_id)).all()
        else:
            runCourseList = RunCourse.query.filter(RunCourse.course_ID.like(course_id)).all()
        
        db.session.close()
        if len(runCourseList):
            for course in runCourseList:
                course.run_Starttime = course.run_Starttime.strftime('%H:%M:%S')
                course.run_Endtime = course.run_Endtime.strftime('%H:%M:%S')
                course.reg_Starttime = course.reg_Starttime.strftime('%H:%M:%S')
                course.reg_Endtime = course.reg_Endtime.strftime('%H:%M:%S')  
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [finalcourse.json() for finalcourse in runCourseList]
                    }
                }
            )
        return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

# get_run_course_by_course_id() ------------------------------------
retrieve_run_course = api.parser()
retrieve_run_course.add_argument("course_id", help="Enter course id")
@api.route("/get_run_course_by_course_id")
@api.doc(description="Get run course by course id")
class GetRunCourse(Resource):
    @api.expect(retrieve_run_course)
    def get(self):
        courseID = retrieve_run_course.parse_args().get("course_id")
        course = RunCourse.query.filter_by(course_ID=courseID).first()
        db.session.close()
        if course:
            course.run_Starttime = course.run_Starttime.strftime('%H:%M:%S')
            course.run_Endtime = course.run_Endtime.strftime('%H:%M:%S')
            course.reg_Starttime = course.reg_Starttime.strftime('%H:%M:%S')
            course.reg_Endtime = course.reg_Endtime.strftime('%H:%M:%S')
            course.feedback_Starttime = course.feedback_Starttime.strftime('%H:%M:%S')
            course.feedback_Endtime = course.feedback_Endtime.strftime('%H:%M:%S')

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json()]
                    }
                }
            )
        return json.loads(json.dumps({"message": "There is no such course", "code": 404}, default=str))

# change_registration_status() --------------------------------
change_registration_status_model = api.model("change_registration_status_model", {
    "rcourse_ID": fields.Integer(description="Runcourse ID", required=True),
})

@api.route("/change_registration_status", methods=["POST"])
@api.doc(description="Change registration status between ongoing and closed")
class ChangeRegistrationStatus(Resource):
    @api.expect(change_registration_status_model)
    def post(self):

        user_role = common.getUserRole()
        if (user_role) != 'Admin':
            return {
                "message": "Unathorized Access, Failed to create run course"
            }, 404

        data = request.get_json()

        try:
            rcourseID = data["rcourse_ID"]
            rcourse = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            course = Course.query.filter_by(course_ID=rcourse.course_ID).first()
            message = ''            

            current_datetime = datetime.now()
            current_date = current_datetime.strftime('%Y-%m-%d')
            close_date = (current_datetime + timedelta(days=5)).strftime('%Y-%m-%d')

            rcourse_run_startdate_str = rcourse.run_Startdate.strftime('%Y-%m-%d')
            # print(rcourse_run_startdate_str)
            if rcourse_run_startdate_str <= close_date:
                close_date = (rcourse.run_Startdate - timedelta(days=1)).strftime('%Y-%m-%d')
            
            current_time = current_datetime.strftime('%H:%M:%S')

            if(rcourse):
                if rcourse.runcourse_Status == "Closed":
                    setattr(rcourse, "runcourse_Status", "Ongoing")
                    setattr(course, "course_Status", "Active")
                    setattr(rcourse, "reg_Startdate", current_date)
                    setattr(rcourse, "reg_Starttime", current_time)
                    setattr(rcourse, "reg_Enddate", close_date)
                    setattr(rcourse, "reg_Endtime", "10:00:00")
                    message = 'Run Course registration Opened'
                else:
                    setattr(rcourse, "runcourse_Status", "Closed")
                    setattr(course, "course_Status", "Inactive")
                    message = 'Run Course registration Closed'

                db.session.commit()

                return json.loads(json.dumps({"message": message, "code": 200}, default=str))

            return json.loads(json.dumps({"message": "There is no such runcourse", "code": 404}, default=str))

        except Exception as e:
            db.session.rollback()
            return "Failed" + str(e), 500

get_runcourse_by_id = api.parser()
get_runcourse_by_id.add_argument("runcourse_id", help="Enter runcourse id")
@api.route("/get_runcourse_by_id")
@api.doc(description="Get run course by runcourse id")
class GetRunCourse(Resource):
    @api.expect(get_runcourse_by_id)
    def get(self):
        rcourse_id = get_runcourse_by_id.parse_args().get("runcourse_id")  # Use "runcourse_id" instead of "rcourse_ID"
        runcourse = RunCourse.query.filter_by(rcourse_ID=rcourse_id).first()  # Use "rcourse_ID" instead of "rcourse_id"
        db.session.close()

        if runcourse:
            return json.loads(json.dumps(runcourse.json(), default=str)), 200

        return json.loads(json.dumps({"message": "There is no such runcourse"})), 404

edit_runcourse = api.parser()
@api.route("/edit_runcourse/<int:runcourse_id>", methods=["PUT"])
@api.doc(description="Edit run course")
class EditRunCourse(Resource):
    @api.expect(edit_runcourse)
    def put(self, runcourse_id):

        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to edit run course"
                }, 404
    
            #Get the updated data from the request body 
            updated_data = request.json
        
            runcourse = RunCourse.query.filter_by(rcourse_ID=runcourse_id).first()

            if not runcourse:
                return {
                    'message': "There is no such runcourse"
                }, 404

             # Get instructor availability data from the updated data
            start_date = datetime.strptime(updated_data.get('run_Startdate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(updated_data.get('run_Enddate'), '%Y-%m-%d').date()
            start_time = datetime.strptime(updated_data.get('run_Starttime'), '%H:%M:%S').time()
            end_time = datetime.strptime(updated_data.get('run_Endtime'), '%H:%M:%S').time()
            instructor_id = updated_data.get('instructor_ID')

            # Query existing run courses for the given instructor
            #runs = RunCourse.query.filter_by(instructor_ID=instructor_id).all()

            # Query existing run courses for the given instructor excluding the current record being edited
            runs = RunCourse.query.filter(RunCourse.instructor_ID == instructor_id, RunCourse.rcourse_ID != runcourse_id).all()
            
            # Check instructor availability
            if runs:
                for run in runs:
                    if run.run_Startdate <= end_date and run.run_Enddate >= start_date:
                        if run.run_Endtime >= start_time and run.run_Starttime <= end_time:
                            return {
                                'message': 'Instructor is already occupied at the chosen date and time'
                            }, 400

    
            # Update the fields based on updated_data
            for field, value in updated_data.items():
                #print(f"Updating {field} to {value}")
                setattr(runcourse, field, value)

            #Commit the changes to the database 
            db.session.commit()
            # db.session.close()

           # Convert dates and times to formatted strings
            runcourse.run_Startdate = start_date.strftime('%Y-%m-%d')
            runcourse.run_Enddate = end_date.strftime('%Y-%m-%d')
            runcourse.run_Starttime = start_time.strftime('%H:%M:%S')
            runcourse.run_Endtime = end_time.strftime('%H:%M:%S')

            runcourse.reg_Startdate = runcourse.reg_Startdate.strftime('%Y-%m-%d')
            runcourse.reg_Enddate = runcourse.reg_Enddate.strftime('%Y-%m-%d')
            runcourse.reg_Starttime = runcourse.reg_Starttime.strftime('%H:%M:%S')
            runcourse.reg_Endtime = runcourse.reg_Endtime.strftime('%H:%M:%S')

            runcourse.feedback_Startdate = runcourse.feedback_Startdate.strftime('%Y-%m-%d')
            runcourse.feedback_Enddate = runcourse.feedback_Enddate.strftime('%Y-%m-%d')
            runcourse.feedback_Starttime = runcourse.feedback_Starttime.strftime('%H:%M:%S')
            runcourse.feedback_Endtime = runcourse.feedback_Endtime.strftime('%H:%M:%S')

            return {
                'message': 'Run course updated successfully',
                'data': runcourse.json()
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                "message": "Failed to update run course: " + str(e)
            }, 500

create_runcourse = api.parser()
@api.route("/create_runcourse/<int:course_id>", methods=["POST"])
@api.doc(description="Create run course")
class CreateRunCourse(Resource):
    def post(self, course_id):
        try: 
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {
                    "message": "Unathorized Access, Failed to create run course"
                }, 404

            # Get the data for creating a new run course from the request body
            new_run_course_data = request.json

            start_date = datetime.strptime(new_run_course_data.get('run_Startdate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(new_run_course_data.get('run_Enddate'), '%Y-%m-%d').date()
            start_time = datetime.strptime(new_run_course_data.get('run_Starttime'), '%H:%M:%S').time()
            end_time = datetime.strptime(new_run_course_data.get('run_Endtime'), '%H:%M:%S').time()
            instructor_id = new_run_course_data.get('instructor_ID')

            runs = RunCourse.query.filter_by(instructor_ID=instructor_id).all()

            if runs:
                for run in runs:
                    if run.run_Startdate <= end_date and run.run_Enddate >= start_date:
                        if run.run_Endtime >= start_time and run.run_Starttime <= end_time:
                            return {
                                'message': 'Instructor is already occupied at the chosen date and time'
                            }, 400
                
            #print(new_run_course_data)

            # Create a new run course object with the data
            new_run_course = RunCourse(**new_run_course_data)

            # Add the new course to the database
            db.session.add(new_run_course)

            # Commit the changes to the database
            db.session.commit()

            # Inside the create_proposed_course route
            #print("Data before returning:", new_proposed_course.json())

            # Return the newly created course as JSON response
            #return json.loads(json.dumps(new_run_course.json(), default=str)), 201

            # Convert dates and times to formatted strings
            new_run_course.run_Startdate = start_date.strftime('%Y-%m-%d')
            new_run_course.run_Enddate = end_date.strftime('%Y-%m-%d')
            new_run_course.run_Starttime = start_time.strftime('%H:%M:%S')
            new_run_course.run_Endtime = end_time.strftime('%H:%M:%S')

            new_run_course.reg_Startdate = new_run_course.reg_Startdate.strftime('%Y-%m-%d')
            new_run_course.reg_Enddate = new_run_course.reg_Enddate.strftime('%Y-%m-%d')
            new_run_course.reg_Starttime = new_run_course.reg_Starttime.strftime('%H:%M:%S')
            new_run_course.reg_Endtime = new_run_course.reg_Endtime.strftime('%H:%M:%S')

            new_run_course.feedback_Startdate = new_run_course.feedback_Startdate.strftime('%Y-%m-%d')
            new_run_course.feedback_Enddate = new_run_course.feedback_Enddate.strftime('%Y-%m-%d')
            new_run_course.feedback_Starttime = new_run_course.feedback_Starttime.strftime('%H:%M:%S')
            new_run_course.feedback_Endtime = new_run_course.feedback_Endtime.strftime('%H:%M:%S')

            return {
                'message': 'Run course created successfully',
                'data': new_run_course.json()  # Assuming new_run_course.json() returns the required data as a dictionary
            }, 201

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {
                "message": "Failed to create a new run course: " + str(e)
            }, 500
        
# Apply Feedback Template to Course
course_apply_feedback_template = api.parser()
course_apply_feedback_template.add_argument("rcourse_id", help="Enter course id")
course_apply_feedback_template.add_argument("template_id", help="Enter template id")
@api.route("/course_apply_feedback_template")
@api.doc(description="Apply feedback template to a course")
class CourseApplyFeedbackTemplate(Resource):
    @api.expect(course_apply_feedback_template)
    def post(self):
        try:
            user_role = common.getUserRole()
            if (user_role) != 'Admin':
                return {"message": "Unauthorized Access, Failed to apply feedback template to run course"}, 404

            args = course_apply_feedback_template.parse_args()
            rcourseID = args.get("rcourse_id")
            templateID = args.get("template_id")
            
            course = RunCourse.query.filter_by(rcourse_ID=rcourseID).first()
            print(course)
            print(templateID)

            # check if template id is valid
            if course is None:
                return jsonify({"message": "run course course not found", "code": 404}), 404

            if datetime.now().date() > course.feedback_Startdate:
                return jsonify({"message": "run course in ongoing feedback period", "code": 404}), 404
            elif datetime.now().date() > course.feedback_Enddate:
                return jsonify({"message": "run course in past feedback period", "code": 404}), 404

            course.template_ID = templateID
            db.session.commit()
            return jsonify({"code": 200, "message": "Run course assign feedback template success"})

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({"code": 500, "message": "Failed. " + str(e)})

get_course_formats = api.parser()
@api.route("/get_course_formats")
@api.doc(description="Get course formats")
class GetCourseFormats(Resource):
    @api.expect(get_course_formats)
    def get(self):
        distinct_course_formats = db.session.query(distinct(RunCourse.course_Format)).all()
        db.session.close()

        if distinct_course_formats:
            return json.loads(json.dumps(distinct_course_formats, default=str)), 200

        return json.loads(json.dumps({"message": "No course formats found."})), 404

retrieve_run_course_count = api.parser()
retrieve_run_course_count.add_argument("course_id", help="Enter course id")
@api.route("/get_run_course_count_by_course_id")
@api.doc(description="Get run course count by course id")
class GetRunCourseCount(Resource):
    @api.expect(retrieve_run_course_count)
    def get(self):
        try: 
            courseID = retrieve_run_course_count.parse_args().get("course_id")
            
            run_course_count = RunCourse.query.filter_by(course_ID=courseID).count()

            course = Course.query.filter_by(course_ID=courseID).first()

            db.session.close()

            if run_course_count >= 0:

                course_name = course.course_Name

                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "run_course_count": run_course_count,
                            "course_name": course_name
                        }
                    }
                )
            
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no run courses for this course ID"
                }

            )
        
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {
                    "code": 500, 
                    "message": "Failed to retrieve run course count: " + str(e)
                }
            )

get_available_instructors = api.parser()
get_available_instructors.add_argument("rcourse_ID", help="Enter run course ID")
get_available_instructors.add_argument("run_Startdate", help="Enter run course start date")
get_available_instructors.add_argument("run_Enddate", help="Enter run course end date")
get_available_instructors.add_argument("run_Starttime", help="Enter run course start time")
get_available_instructors.add_argument("run_Endtime", help="Enter run course end time")
@api.route("/get_available_instructors", methods=["GET"])
@api.doc(description="Get all the available instructors")
class GetAvailableInstructors(Resource):
    def get(self):
        try: 
            
            args = get_available_instructors.parse_args()

            run_course_id = args.get("rcourse_ID", "")
            start_date = datetime.strptime(args.get('run_Startdate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(args.get('run_Enddate'), '%Y-%m-%d').date()
            start_time = datetime.strptime(args.get('run_Starttime'), '%H:%M:%S').time()
            end_time = datetime.strptime(args.get('run_Endtime'), '%H:%M:%S').time()

            if run_course_id:
                runs_with_instructors = db.session.query(RunCourse, User).join(User, RunCourse.instructor_ID == User.user_ID).filter(RunCourse.rcourse_ID != run_course_id).all()
            else: 
                # Join RunCourse with User table 
                runs_with_instructors = db.session.query(RunCourse, User).join(User, RunCourse.instructor_ID == User.user_ID).all()

            # List comprehension to filter instructors and create a list of dictionaries
            available_instructors = [
                {
                    "user_ID": user.user_ID,
                    "user_Name": user.user_Name
                    # Add other user details as needed
                }
                for user in User.query.filter(User.role_Name.in_(['Instructor', 'Trainer'])).all()
                if user.user_Name not in [
                    user.user_Name
                    for run_course, user in runs_with_instructors
                    if run_course.run_Startdate <= end_date and run_course.run_Enddate >= start_date
                    and run_course.run_Endtime >= start_time and run_course.run_Starttime <= end_time
                ]
            ]

            # Return the list of available instructors in the desired format
            return jsonify(
                {   
                    "code": 200,
                    "data": {
                        "available_instructors": available_instructors
                    }
                }
            )

    
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {
                    "code": 500, 
                    "message": "Failed to retrieve available instructors: " + str(e)
                }
            )

# ==================== LOGIN FUNCTIONS ====================#
# login()
# verify_email()
# register()
# forgot_password()
# reset_password()

# login() -----------------------------------------
login_model = api.model("login_model", {
    "email" : fields.String(description="email", required=True),
    "password" : fields.String(description="password", required=True)
})
@api.route("/login", methods=["POST"])
@api.doc(description = "Login")

class Login(Resource):
    @api.expect(login_model)
    def post(self):
        # get inputted email and password
        data = request.get_json()
        email = data['email']
        password = data['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        print(hashed_password)

        # compare input and database, then display results
        try:
            user = User.query.filter_by(user_Email=email).first()
            db.session.close()
            if user:
                if bcrypt.check_password_hash(user.user_Password, password):
                    # store user details in session
                    session['user_ID'] = user.user_ID
                    # app.logger.info("In flask:", session['user_ID'])
                    
                    return json.loads(json.dumps({"message":"Login successful"})), 200
                
                else:
                    return json.loads(json.dumps({"Message": "Invalid username or password"}, default=str)), 404

            else:
                return json.loads(json.dumps({"Message": "Email does not exist"}, default=str)), 404

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500
        
# verify_email() -----------------------------------------
verify_email_model = api.model("verify_email_model", {
    "email" : fields.String(description="email", required=True)
})
@api.route("/verify_email", methods=["POST"])
@api.doc(description = "Verify email")

class VerifyEmail(Resource):
    @api.expect(verify_email_model)
    def post(self):
        # get inputted email
        data = request.get_json()
        email = data['email']

        # check if email already exists, else send verification email
        try:
            user = User.query.filter_by(user_Email=email).first()
            if user:
                db.session.close()
                return json.loads(json.dumps({"Message": "You already have an account with us."}, default=str)), 404
            
            else:
                self.send_email(email)
                db.session.close()
                return json.loads(json.dumps({"message":"Verification email sent"})), 200

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500

    def send_email(self, email):
        msg = Message('Welcome to Upskilling Engagement System',
                  sender='upskilling.engagement@outlook.com',
                  recipients=[email])
        msg.html = "<p>Please click the link to verify your email and finish creating your account <a href='http://localhost:8080/t6_ba_dcs_scis_upskilling/registerform?email="+ email +"'>http://localhost:8080/t6_ba_dcs_scis_upskilling/registerform?email="+ email +"</a>.</p>"
        mail.send(msg)
        return "Email sent!"


# user input email-, system send email-, user click link-, user sent to page to input details,
# create user in db-, user can now login-
# email must be transmitted to page to input details, maybe through the link?

# register() ------------------------------------------
register_model = api.model("register_model", {
    "role" : fields.String(description="Role", required=True),
    "fullName" : fields.String(description="User Name", required=True),
    "email" : fields.String(description="Email", required=True),
    "password" : fields.String(description="Password", required=True),
    "confirmpassword" : fields.String(description="Confirm password", required=True),
    "organizationName" : fields.String(description="Organisation Name", required=False),
    "alumni" : fields.Boolean(description="Alumni?", required=False)
})
@api.route("/register", methods=["POST"])
@api.doc(description = "Register")

class Register(Resource):
    @api.expect(register_model)
    def post(self):
        # get inputs
        data = request.get_json()
        print(data)
        password = data['password']
        repassword = data['confirmpassword']

        # check if password is valid
        if password != repassword:
            return json.loads(json.dumps({"Message": "Password is not the same"}, default=str)), 404
        elif len(password) < 8:
            return json.loads(json.dumps({"Message": "Password needs to be at least 8 characters"}, default=str)), 404
        elif not any(char.islower() for char in password):
            return json.loads(json.dumps({"Message": "Password needs at least one lowercase letter"}, default=str)), 404
        elif not any(char.isupper() for char in password):
            return json.loads(json.dumps({"Message": "Password needs at least one uppercase letter"}, default=str)), 404
        elif not any(char.isdigit() for char in password):
            return json.loads(json.dumps({"Message": "Password needs at least one number"}, default=str)), 404
        elif password.isalnum():
            return json.loads(json.dumps({"Message": "Password needs at least one special character"}, default=str)), 404
        
        # check if user alr in db (user reclick link)
        if User.query.filter_by(user_Email=data['email']).first():
            return json.loads(json.dumps({"Message": "Email already exists"}, default=str)), 404
        
        # hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # create user in db
        newUser = User(user_Name=data['fullName'], user_Email=data['email'], user_Password=hashed_password, role_Name=data['role'])
        try:
            db.session.add(newUser)
            
            if data['role'] == 'Trainer':
                user = User.query.filter_by(user_Email=data['email']).first()
                newExternalUser = ExternalUser(user_ID=getattr(user, 'user_ID'), organisation_Name=data['organizationName'], is_Alumni=bool(int(data['alumni'])))
                db.session.add(newExternalUser)
                db.session.commit()
                return json.loads(json.dumps(newExternalUser.json(), default=str)), 200
            
            else:
                db.session.commit()
                return json.loads(json.dumps(newUser.json(), default=str)), 200

            db.session.close()
        
        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500
        
# forgot_password() --------------------------------------
forgot_password_model = api.model("forgot_password_model", {
    "email" : fields.String(description="email", required=True)
})
@api.route("/forgot_password", methods=["POST"])
@api.doc(description = "Send new password email")

class ForgotPassword(Resource):
    @api.expect(forgot_password_model)
    def post(self):
        # get inputted email
        data = request.get_json()
        email = data['email']

        # check if email does not exist, else send email w new password
        try:
            user = User.query.filter_by(user_Email=email).first()
            if not user:
                db.session.close()
                return json.loads(json.dumps({"Message": "Email does not exist"}, default=str)), 404
            
            else:
                self.send_email(email)
                db.session.close()
                return json.loads(json.dumps({"message":"Email sent"})), 200

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500

    def send_email(self, email):
        msg = Message('[Upskilling Engagement System] Reset Password',
                  sender='upskilling.engagement@outlook.com',
                  recipients=[email])
        msg.html = "<p>Please click the link to change your password <a href='http://localhost:8080/t6_ba_dcs_scis_upskilling/resetPassword?email="+ email +"'>http://localhost:8080/t6_ba_dcs_scis_upskilling/resetPassword?email="+ email +"</a>.</p>"
        mail.send(msg)
        return "Email sent!"

# reset_password() ------------------------------------
reset_password_model = api.model("reset_password_model", {
    "password" : fields.String(description="password", required=True),
    "confirmpassword" : fields.String(description="confirm password", required=True),
    "email" : fields.String(description="email", required=True)
})
@api.route("/reset_password", methods=["POST"])
@api.doc(description = "Reset password")

class ResetPassword(Resource):
    @api.expect(reset_password_model)
    def post(self):
        # get inputted data
        data = request.get_json()
        password = data['password']
        confirmpassword = data['confirmpassword']
        email = data['email']

        try:
            if password != confirmpassword:
                return json.loads(json.dumps({"Message": "Password and confirm password does not match"}, default=str)), 404
            
            else:
                user = User.query.filter_by(user_Email=email).first()
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                setattr(user, 'user_Password', hashed_password)
                db.session.commit()
                db.session.close()
                return json.loads(json.dumps({"Message": "Password updated"}, default=str)), 200

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500
        
# retrieve user_ID from session
@api.route("/get_user_id")
class GetRole(Resource):
    def get(self):
        user_ID = session.get('user_ID')
        if user_ID:
            id = User.query.filter_by(user_ID=user_ID).first().user_ID
            db.session.close()
            return id
        else:
            return 'Session not set'

@api.route("/get_user_name")
class GetUserName(Resource):
    def get(self):
        user_ID = session.get('user_ID')
        if user_ID:
            user = User.query.filter_by(user_ID=user_ID).first()
            db.session.close()
            if user:
                user_name = user.user_Name
                return user_name
            else:
                return 'User not found'
        else:
            db.session.close()
            return 'Session not set'

@api.route("/get_role")
class GetRole(Resource):
    def get(self):
        user_ID = session.get('user_ID')
        if user_ID:
            role = User.query.filter_by(user_ID=user_ID).first().role_Name
            db.session.close()
            return role
        
        else:
            db.session.close()
            return 'Session not set'

@api.route("/logout")
class Logout(Resource):
    def get(self):
        user_ID = session.get('user_ID')
        if user_ID:
            session.pop('user_ID', None)  # Remove 'user_ID' from the session
            #return redirect(url_for('logout_page'))
            session.clear()

            return json.loads(json.dumps({"message": "Logged out successfully"})), 200
        else:  
            
            return json.loads(json.dumps({"message": "Logged out not successful"})), 400
        
get_all_coaches = api.parser()
@api.route("/get_all_coaches")
@api.doc(description="Get all instructors and trainers")
class GetAllInstructors(Resource):
    @api.expect(get_all_coaches)
    def get(self):
        coaches = User.query.filter(or_(User.role_Name == 'Instructor', User.role_Name == "Trainer")).all()
        db.session.close()
        
        if coaches:
            coaches_json = [coach.json() for coach in coaches]
            return {"code": 200, "data": {"coaches": coaches_json}}, 200

        return {"code": 404, "message": "No instructors or trainers found"}, 404

get_coach_by_id = api.parser()
get_coach_by_id.add_argument("instructor_id", help="Enter instructor id")
@api.route("/get_coach_by_id")
@api.doc(description="Get instructor or trainer by instructor id")
class GetInstructor(Resource):
    @api.expect(get_coach_by_id)
    def get(self):
        instructorID = get_coach_by_id.parse_args().get("instructor_id")
        coach = User.query.filter_by(user_ID=instructorID).first()
        db.session.close()
        if coach:
            return json.loads(json.dumps(coach.json())), 200

        return json.loads(json.dumps({"message": "There is no such instructor or trainer"})), 404
    

#=========== User Management Functions ===============#
# All Admin
retrieve_admin_parser = api.parser()
retrieve_admin_parser.add_argument("admin_name", help="Enter admin name")


@api.route("/get_all_admin")
@api.doc(description="Get all admin users")
class GetAllAdmin(Resource):
    @api.expect(retrieve_admin_parser)
    def get(self):
        args = retrieve_admin_parser.parse_args()
        admin_name = args.get("admin_name", "")

        try:
            admin_users = User.query.filter_by(role_Name='admin').all()

            if admin_name:
                admin_users = [
                    user for user in admin_users if admin_name.lower() in user.user_Name.lower()]

            if admin_users:
                admin_users_json = []
                user_id = session.get('user_ID')

                if user_id:

                    # Find the user with the matching user_ID from the session
                    user = User.query.filter_by(user_ID=user_id, role_Name='admin').first()

                    if user:
                        user_data = {
                            "user_ID": user.user_ID,
                            "user_Name": user.user_Name,
                            "user_Email": user.user_Email,
                            "role_Name": user.role_Name
                        }

                        admin_users_json.append(user_data)

                # Add other admin users to admin_users_json
                for user in admin_users:
                    # Check if the user is not the same as the one in the session
                    if user_id and user.user_ID != user_id:
                        user_data = {
                            "user_ID": user.user_ID,
                            "user_Name": user.user_Name,
                            "user_Email": user.user_Email,
                            "role_Name": user.role_Name
                        }
                        admin_users_json.append(user_data)

                db.session.close()

                return jsonify({"code": 200, "data": admin_users_json})
            else:
                return jsonify({"code": 404, "message": "No admin users found."})
        except Exception as e:
            return jsonify({"code": 500, "message": "Error occurred while fetching admin users.", "error": str(e)})
# All Students
retrieve_student_parser = api.parser()
retrieve_student_parser.add_argument("student_name", help="Enter student name")
retrieve_student_parser.add_argument(
    "blacklisted", help="Filter by blacklisted status")

# Define the API route for getting all student users


@api.route("/get_all_student")
@api.doc(description="Get all student users")
class GetAllAdmin(Resource):
    @api.expect(retrieve_student_parser)
    def get(self):
        args = retrieve_student_parser.parse_args()
        student_name = args.get("student_name", "")
        # Change to None for better comparison
        blacklisted = args.get("blacklisted", None)

        try:
            students = User.query.filter_by(role_Name='student').all()

            if student_name:
                students = [
                    user for user in students if student_name.lower() in user.user_Name.lower()]

            # Check if blacklisted is specified and is 'True' (case-insensitive)
            if blacklisted is not None:
                if blacklisted.lower() == 'true':
                    students = [user for user in students if Blacklist.query.filter_by(
                        user_ID=user.user_ID).first() is not None]
                elif blacklisted.lower() == 'false':
                    students = [user for user in students if Blacklist.query.filter_by(
                        user_ID=user.user_ID).first() is None]

            if students:
                student_list = []

                for user in students:
                    is_blacklisted = Blacklist.query.filter_by(
                        user_ID=user.user_ID).first() is not None
                    student_data = {
                        'user_ID': user.user_ID,
                        'user_Name': user.user_Name,
                        'user_Email': user.user_Email,
                        'is_blacklisted': is_blacklisted
                    }

                    student_list.append(student_data)

                db.session.close()

                return jsonify({"code": 200, "data": student_list})
            else:
                return jsonify({"code": 404, "message": "No student users found."})
        except Exception as e:
            return jsonify({"code": 500, "message": "Error occurred while fetching student users.", "error": str(e)})


# All Instructors
retrieve_instructors_trainers = api.parser()
retrieve_instructors_trainers.add_argument(
    "instructor_name", help="Enter instructor name")
retrieve_instructors_trainers.add_argument("role_name", help="Enter role name")
retrieve_instructors_trainers.add_argument(
    "organization_name", help="Enter organization")


@api.route("/get_all_instructors_and_trainers")
@api.doc(description="Get all instructors and trainers with organization names")
class GetAllInstructorsAndTrainers(Resource):
    @api.expect(retrieve_instructors_trainers)
    def get(self):
        try:
            args = retrieve_instructors_trainers.parse_args()
            instructor_name = args.get("instructor_name", "")
            role_name = args.get("role_name")
            organization_name = args.get("organization_name", "")

            query = db.session.query(
                User.user_ID,
                User.user_Name,
                User.user_Email,
                db.func.ifnull(ExternalUser.organisation_Name, "SMU").label("organisation_Name"),
                User.role_Name,
            ).select_from(User).outerjoin(ExternalUser, User.user_ID == ExternalUser.user_ID)

            # Add filtering for "Instructor" or "Trainer" roles
            query = query.filter(User.role_Name.in_(["Instructor", "Trainer"]))

            if organization_name == "SMU":
                query = query.filter(ExternalUser.organisation_Name.is_(None))
            elif organization_name:
                query = query.filter(ExternalUser.organisation_Name.like(f"%{organization_name}%"))
                
            if instructor_name:
                query = query.filter(User.user_Name.contains(instructor_name))
            
            if role_name:
                query = query.filter(User.role_Name == role_name)
            
            results = query.all()

            def get_instructor_average_ratings(instructor_ID):
                keywords = ['rate', 'Instructor']  # Define keywords to identify relevant questions
            
                total_ratings = []
                total_questions = 0

                # To retrieve relevant questions and calculate average rating
                relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
                    .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
                    .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
                    .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                    .filter(TemplateAttribute.input_Type == 'Likert Scale') \
                    .filter(func.lower(TemplateAttribute.question).contains(keywords[0])) \
                    .filter(func.lower(TemplateAttribute.question).contains(keywords[1]))

                if instructor_ID:  # Filter by instructor ID if provided
                    relevant_questions = relevant_questions.filter(RunCourse.instructor_ID == instructor_ID)

                relevant_questions = relevant_questions.all()

                for feedback_template, template_attribute in relevant_questions:
                    question_id = template_attribute.template_Attribute_ID
                                    
                    feedback_entries = db.session.query(Feedback) \
                        .filter(Feedback.template_Attribute_ID == question_id)

                    if instructor_ID:
                        feedback_entries = feedback_entries.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                            .filter(RunCourse.instructor_ID == instructor_ID)  # Filter by instructor ID if provided

                    feedback_entries = feedback_entries.all()

                    if feedback_entries:
                        for entry in feedback_entries:
                            if entry.answer.isdigit():
                                total_ratings.append(int(entry.answer))
                                total_questions += 1

                # Calculate the instructor-specific average rating
                if total_ratings and total_questions > 0:
                    instructor_average_rating = round(sum(total_ratings) / total_questions, 2)
                else:
                    instructor_average_rating = 0

                db.session.close()
                
                return instructor_average_rating

            if results:
                result_data = []
                for result in results:
                    instructor_trainer_info = {
                        "user_ID": result[0],
                        "user_Name": result[1],
                        "user_Email": result[2],
                        "organisation_Name": result[3],
                        "role_Name": result[4],
                        "average_rating": get_instructor_average_ratings(result[0])
                    }
                    
                    result_data.append(instructor_trainer_info)

                return jsonify({"code": 200, "data": result_data})

            return jsonify({"code": 404, "message": "No instructors or trainers found"})
        except Exception as e:
            return "Failed. " + str(e), 500


# Student Name
retrieve_student_name = api.parser()
retrieve_student_name.add_argument("user_id", help="Enter user id")


@api.route("/get_student_name")
@api.doc(description="Get student name")
class GetStudentName(Resource):
    @api.expect(retrieve_student_name)
    def get(self):
        args = retrieve_student_name.parse_args()
        user_id = args.get("user_id", "")

        user = User.query.filter_by(user_ID=user_id).first()

        user_name = user.user_Name

        return jsonify({"code": 200, "data": user_name})


# Blacklist Student
retrieve_blacklist_student_id = api.parser()
retrieve_blacklist_student_id.add_argument(
    "user_ids", type=int, action="append", required=True, help="Enter user ids as a list")


@api.route('/blacklist', methods=['POST'])
@api.doc(description="Blacklist Student")
class BlacklistStudent(Resource):
    @api.expect(retrieve_blacklist_student_id)
    def post(self):
        try:
            args = retrieve_blacklist_student_id.parse_args()
            user_ids = args["user_ids"]
            if len(user_ids) >0:

                # Check if all the users with the given IDs exist
                users = User.query.filter(User.user_ID.in_(user_ids)).all()
                existing_user_ids = [user.user_ID for user in users]
                missing_user_ids = set(user_ids) - set(existing_user_ids)

                if missing_user_ids:
                    return jsonify({'code': 404, 'message': f'Users are not found'})

                # Check if any of the users are already blacklisted
                blacklisted_users = Blacklist.query.filter(Blacklist.user_ID.in_(user_ids)).all()
                blacklisted_user_ids = [entry.user_ID for entry in blacklisted_users]

                if blacklisted_user_ids:
                    return jsonify({'code': 400, 'message': f'There are users who are already blacklisted'})

                # Create new blacklist entries for each user
                for user_id in user_ids:
                    blacklist_entry = Blacklist(user_ID=user_id)
                    db.session.add(blacklist_entry)

                db.session.commit()
                db.session.close()

                return jsonify({'code': 200, 'message': 'Users successfully blacklisted'})
            else:
                return jsonify({'code': 400, 'message': f'You did not select any user to be blacklisted'})
        except Exception as e:
            return "Failed. " + str(e), 500


retrieve_blacklist_remove = api.parser()
retrieve_blacklist_remove.add_argument(
    "user_ids", type=int, action="append", required=True, help="Enter user IDs as a list")


@api.route('/remove_from_blacklist', methods=['POST'])
@api.doc(description="Remove Students from Blacklist")
class RemoveFromBlacklist(Resource):
    @api.expect(retrieve_blacklist_student_id)
    def post(self):
        try:
            args = retrieve_blacklist_student_id.parse_args()
            user_ids = args["user_ids"]

            if len(user_ids) >0:

                # Check if any of the users are blacklisted
                blacklisted_users = Blacklist.query.filter(Blacklist.user_ID.in_(user_ids)).all()
                blacklisted_user_ids = [entry.user_ID for entry in blacklisted_users]

                if not blacklisted_user_ids:
                    return jsonify({'code': 400, 'message': f'Users are not blacklisted'})

                # Remove blacklisted entries for each user
                for user_id in user_ids:
                    Blacklist.query.filter_by(user_ID=user_id).delete()

                db.session.commit()
                db.session.close()

                return jsonify({'code': 200, 'message': 'Users successfully removed from blacklist'})
            else:
                return jsonify({'code': 400, 'message': f'You did not select any students to be removed from blacklist'})
        except Exception as e:
            return "Failed. " + str(e), 500
    
# Remove Admin - Update Role Name to "Instructor"
remove_admin_id = api.parser()
remove_admin_id.add_argument("user_ID", help="Enter user id")

@api.route("/remove_admin")
@api.doc(description="Remove admin")
class RemoveAdmin(Resource):
    @api.expect(remove_admin_id)
    def post(self):
        try:
            current_admin_ID = int(session.get('user_ID'))
            user_ID = int(remove_admin_id.parse_args().get("user_ID"))
            print(current_admin_ID,"==",user_ID)
            
            if user_ID == current_admin_ID:
                print("they are equal")
                return json.loads(json.dumps({"message":"You can't remove yourself"})), 200  # Use 400 Bad Request status
            else:
                user = User.query.filter_by(user_ID=user_ID).first()            
                if(user and user.role_Name == "Admin"):
                    try:
                        user.role_Name = "Instructor"         
                        db.session.commit()    
                        db.session.close()             
                        return json.loads(json.dumps({"message":"Admin role changed to 'Instructor'"})), 200
                    except Exception as e:
                        return "Failed to remove admin role. " + str(e), 500

                return json.loads(json.dumps({"message": "There is no such admin user"})), 404

        except Exception as e:
            return "Failed. " + str(e), 500

def generate_random_password(length):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Ensure at least one character from each category
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special_characters),
    ]

    # Fill the rest of the password with random characters
    remaining_length = length - len(password)
    all_characters = lowercase + uppercase + digits + special_characters
    password.extend(secrets.choice(all_characters) for _ in range(remaining_length))

    # Shuffle the password to randomize character positions
    secrets.SystemRandom().shuffle(password)
    
    # Convert the list of characters back to a string
    return ''.join(password)

@api.route("/add_admin", methods=["POST"])
@api.doc(description="Add admin")
class AddAdmin(Resource):
    def post(self):
        try:
            # Get the data for creating a new course from the request body
            new_admin_data = request.json

            user_Email = new_admin_data.get("user_Email")

            existing_user = User.query.filter_by(user_Email=user_Email).first()

            if existing_user:
                return {"message": "Email already exists"}, 409  # Conflict

            # Specify the length of the password you want to generate
            password_length = 12  # You can change this to any length you prefer
            random_password = generate_random_password(password_length)

            # Add the random_password to the new_admin_data dictionary
            new_admin_data["user_Password"] = random_password

            print(new_admin_data)

            new_user = User(**new_admin_data)

            # Add the new course to the database
            db.session.add(new_user)

            # Commit the changes to the database
            db.session.commit()

            user_Name = new_admin_data.get("user_Name")

            self.send_email_to_admin(user_Name, user_Email)

            # Return the newly created course as JSON response
            return json.loads(json.dumps(new_user.json(), default=str)), 201

        except Exception as e:
            print("Error:", str(e))
            return "Failed to create a new user: " + str(e), 500
    
    def send_email_to_admin(self, fullName, email):
        msg = Message("Welcome to Upskilling Engagement System",
                    sender="upskilling.engagement@outlook.com", recipients=[email])
        #Need to change this when we deployed to AWS 
        reset_password_link = f'http://localhost:8080/t6_ba_dcs_scis_upskilling/resetPassword?email={email}'
        """
        msg.html = f'''\
                    <html>
                    <body>
                        <p>Dear {fullName},</p>
                        
                        <p>Welcome to the Upskilling Engagement System! We are delighted to have you on board. Your account has been successfully created, and a temporary password has been set for your security.</p>
                        
                        <p>To ensure the safety of your account, please reset your password before signing in. To reset your password, simply click on the following link: <a href="{reset_password_link}">Reset Password</a></p>
                        
                        <p>Thank you for choosing the Upskilling Engagement System. We look forward to empowering your learning journey!</p>
                        
                        <p>Best Regards,<br>
                        Team6ix</p>
                    </body>
                    </html>
                    ''' 
        """
        msg.html = "<p>Please click the link to change your password <a href='http://localhost:8080/t6_ba_dcs_scis_upskilling/resetPassword?email="+ email +"'>http://localhost:8080/t6_ba_dcs_scis_upskilling/resetPassword?email="+ email +"</a>.</p>"
        mail.send(msg)
        print("success")
        return "Email sent!"
        
#============ Vote Course Functions =================#
promote_to_course = api.parser()
promote_to_course.add_argument("course_id", help="Enter course id")
@api.route('/promote_to_course', methods=["POST"])
@api.doc(description="Promote To Course")
class PromoteToCourse(Resource):
  @api.expect(promote_to_course)
  def post(self):
    try:
      user_role = common.getUserRole()
      if (user_role) != 'Admin':
          return {"message": "Unathorized Access, Failed to promote to course"}, 404 
      args = promote_to_course.parse_args()
      course_id = args.get("course_id")
      vote_course = VoteCourse.query.filter_by(course_ID = course_id).first()
      if vote_course:
        vote_course.vote_Status = 'Offered'
        course = Course.query.filter_by(course_ID = vote_course.course_ID).first()
        if course:
          course.course_Status = 'Active'
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Vote Course is successfully promoted to course", "code": 200})
      else:
        return jsonify({"message": "Vote Course does not exist", "code": 404})
    except Exception as e:
        return jsonify({"message": "Failed " + str(e), "code": 500})
    

retrieve_vote_course = api.parser()
retrieve_vote_course.add_argument("course_id", help="Enter course id")
@api.route("/get_vote_course_by_course_id")
@api.doc(description="Get vote course by course id")
class GetVoteCourse(Resource):
    @api.expect(retrieve_vote_course)
    def get(self):
        courseID = retrieve_vote_course.parse_args().get("course_id")
        vote_course = VoteCourse.query.filter_by(course_ID=courseID).first()
        if vote_course:
            course = Course.query.get(vote_course.course_ID)
            course_category = CourseCategory.query.get(course.coursecat_ID)
            db.session.close()
            
            response_data = {
                "course_ID": course.course_ID,
                "course_Name": course.course_Name,
                "course_Desc": course.course_Desc,
                "coursecat_ID": course.coursecat_ID,
                "coursecat_Name": course_category.coursecat_Name,
                "vote_ID": vote_course.vote_ID
            }
            
            return jsonify(
                {
                    "code": 200,
                    "data": response_data
                }
            )
        return jsonify({"message": "There is no such course", "code": 404})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
