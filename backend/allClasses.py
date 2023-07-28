from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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

################## Staff Class Creation ##################
class Staff(db.Model):
    __tablename__ = 'staff'

    staff_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    staff_FName = db.Column(db.String(50), nullable=False)
    staff_LName = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    account = db.Column(db.Integer, db.ForeignKey('accounts.account_Name'), nullable=False)

    def __init__(self, staff_ID, staff_FName, staff_LName, dept, email, account):
        self.staff_ID = staff_ID
        self.staff_FName = staff_FName
        self.staff_LName = staff_LName
        self.dept = dept        
        self.email = email
        self.account = account   

    def json(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
