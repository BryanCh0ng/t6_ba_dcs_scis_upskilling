from flask import request, jsonify, session
from core_features import common
from flask_restx import Namespace, Resource
from allClasses import *
from flask_mail import Message
from sqlalchemy.orm import aliased
from sqlalchemy import func
import json
import logging
import secrets
import string
app.logger.setLevel(logging.DEBUG)

api = Namespace('management', description='User Management')

from app import mail, bcrypt

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
        
