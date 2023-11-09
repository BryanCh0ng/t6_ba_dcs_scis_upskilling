from flask import request, jsonify, redirect, url_for, session
from flask_restx import Namespace, Resource, fields
from allClasses import *
from flask_mail import Message
import json
import logging
from sqlalchemy import or_
app.logger.setLevel(logging.DEBUG)

api = Namespace('user', description='Login related operations')

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

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
        from app import mail, bcrypt
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
                    
                    return json.loads(json.dumps({"code": 200, "message":"Login successful"})), 200
                
                else:
                    return json.loads(json.dumps({"code": 404, "Message": "Invalid username or password"}, default=str)), 404

            else:
                return json.loads(json.dumps({"code": 404, "Message": "Email does not exist"}, default=str)), 404

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
                return json.loads(json.dumps({"code": 404, "Message": "You already have an account with us."}, default=str)), 404
            
            else:
                self.send_email(email)
                db.session.close()
                return json.loads(json.dumps({"code": 200, "message":"Verification email sent"})), 200

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500

    def send_email(self, email):
        from app import mail, bcrypt
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
        from app import mail, bcrypt
        # get inputs
        data = request.get_json()
        print(data)
        password = data['password']
        repassword = data['confirmpassword']

        # check if password is valid
        if password != repassword:
            return json.loads(json.dumps({"code": 404, "message": "Password is not the same"}, default=str)), 404
        elif len(password) < 8:
            return json.loads(json.dumps({"code": 404, "message": "Password needs to be at least 8 characters"}, default=str)), 404
        elif not any(char.islower() for char in password):
            return json.loads(json.dumps({"code": 404, "message": "Password needs at least one lowercase letter"}, default=str)), 404
        elif not any(char.isupper() for char in password):
            return json.loads(json.dumps({"code": 404, "message": "Password needs at least one uppercase letter"}, default=str)), 404
        elif not any(char.isdigit() for char in password):
            return json.loads(json.dumps({"code": 404, "message": "Password needs at least one number"}, default=str)), 404
        elif password.isalnum():
            return json.loads(json.dumps({"code": 404, "message": "Password needs at least one special character"}, default=str)), 404
        
        # check if user alr in db (user reclick link)
        if User.query.filter_by(user_Email=data['email']).first():
            return json.loads(json.dumps({"code": 404, "message": "Email already exists"}, default=str)), 404
        
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
                return json.loads(json.dumps({"code": 404, "message": "Email does not exist"}, default=str)), 404
            
            else:
                self.send_email(email)
                db.session.close()
                return json.loads(json.dumps({"code": 200, "message":"Email sent"})), 200

        except Exception as e:
            db.session.rollback()
            return "Failed: " + str(e), 500

    def send_email(self, email):
        from app import mail, bcrypt
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
        from app import mail, bcrypt
        # get inputted data
        data = request.get_json()
        password = data['password']
        confirmpassword = data['confirmpassword']
        email = data['email']

        try:
            if password != confirmpassword:
                return json.loads(json.dumps({"code": 404, "message": "Password and confirm password does not match"}, default=str)), 404
            
            else:
                user = User.query.filter_by(user_Email=email).first()
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                setattr(user, 'user_Password', hashed_password)
                db.session.commit()
                db.session.close()
                return json.loads(json.dumps({"code": 200, "message": "Password updated"}, default=str)), 200

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

            return json.loads(json.dumps({"code": 200, "message": "Logged out successfully"})), 200
        else:  
            
            return json.loads(json.dumps({"code": 400, "message": "Logged out not successful"})), 400
        
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

        return json.loads(json.dumps({"code": 404, "message": "There is no such instructor or trainer"})), 404