import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api, Resource
from allClasses import *
from core_features.contactus import api as contactus

app = Flask(__name__)
api = Api(
    app,
    default="Backend",
    version="1.0",
    title="SCIS-UPSKILLING-Backend",
    description="",
)
api.add_namespace(contactus)


CORS(app, supports_credentials=True)
# ==================== CONNECTING TO DATABASE ====================#
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_endpoint = os.getenv("DB_ENDPOINT")
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_endpoint}"
app.config["CORS_ALLOW_CREDENTIALS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['SQLALCHEMY_POOL_SIZE'] = 2
# app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)
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