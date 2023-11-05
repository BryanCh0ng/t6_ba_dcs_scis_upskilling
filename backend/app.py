import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api, Resource
from allClasses import *
from os import environ
from core_features.course import api as course
from core_features.coursecat import api as coursecat
from core_features.proposedcourse import api as proposedcourse
from core_features.runcourse import api as runcourse
from core_features.user import api as user
from core_features.contactus import api as contactus
from core_features.registration import api as registration
from core_features.votecourse import api as votecourse
from core_features.feedbacktemplate import api as feedbacktemplate
from core_features.dashboard import api as dashboard
from core_features.recommender import api as recommender
from core_features.feedback import api as feedback
from core_features.common import api as common
from core_features.feedback import api as feedback
from core_features.lesson import api as lesson
# from core_features.attendance import api as attendance
from flask_mail import Mail
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api(
    app,
    default="Backend",
    version="1.0",
    title="SCIS-UPSKILLING-Backend",
    description="",
)
api.add_namespace(course)
api.add_namespace(coursecat)
api.add_namespace(proposedcourse)
api.add_namespace(runcourse)
api.add_namespace(user)
api.add_namespace(contactus)
api.add_namespace(registration)
api.add_namespace(votecourse)
api.add_namespace(feedbacktemplate)
api.add_namespace(dashboard)
api.add_namespace(recommender)
api.add_namespace(feedback)
api.add_namespace(common)
api.add_namespace(feedback)
api.add_namespace(lesson)
# api.add_namespace(attendance)

CORS(app, supports_credentials=True)
# ==================== CONNECTING TO DATABASE ====================#
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_endpoint = os.getenv("DB_ENDPOINT")
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_endpoint}"
app.config["CORS_ALLOW_CREDENTIALS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'ashSDFSDFbiuoqewiort123!@*U&!&*(@^)'
app.config['SQLALCHEMY_POOL_SIZE'] = 30
# app.config['SQLALCHEMY_POOL_SIZE'] = 2
# app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)

# ==================== Mail and Bcrypt ====================#
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'  # Your email server
app.config['MAIL_PORT'] = 587  # Port for sending emails
app.config['MAIL_USE_TLS'] = True  # Use TLS for security
app.config['MAIL_USERNAME'] = 'upskilling.engagement@outlook.com'
app.config['MAIL_PASSWORD'] = 'Team6ix!2023'
#app.config['MAIL_DEFAULT_SENDER'] = 'noreply@live.com'  # Default sender email

# app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'  # Your email server
# app.config['MAIL_PORT'] = 587  # Port for sending emails
# app.config['MAIL_USE_TLS'] = True  # Use TLS for security
# app.config['MAIL_USERNAME'] = 'upskilling_engagement@outlook.com'
# app.config['MAIL_PASSWORD'] = 'Team6ix!'

mail = Mail(app)
bcrypt = Bcrypt(app)

from core_features.usermanagement import api as usermanagement
api.add_namespace(usermanagement)

# ==================== TEST FUNCTIONS ====================
test_parser = api.parser()
test_parser.add_argument("number1", help="First number to add")
test_parser.add_argument("number2", help="Second number to add")
@api.route("/test_endpoint", methods=["GET","POST"])
@api.doc(description="Adds 2 numbers. Just testing the endpoint.")
class Test(Resource):
    @api.expect(test_parser)
    def get(self):
        number1 = test_parser.parse_args().get("number1")
        number2 = test_parser.parse_args().get("number2")
        
        try:
            return jsonify({
                    "code": 200,
                    "data": (int(number1) + int(number2))
                })

        except:
            return jsonify({
                    "code": 404,
                    "message": "Error bro"
                }), 404

# ====================  FUNCTIONS ====================#        
if __name__ == "__main__":
    app.run(debug=True, port=5000)
