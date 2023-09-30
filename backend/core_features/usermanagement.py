from flask import request, jsonify, session
from core_features import common
from flask_restx import Namespace, Resource
from allClasses import *
import json
from sqlalchemy.orm import aliased
from sqlalchemy import func
import logging
app.logger.setLevel(logging.DEBUG)

api = Namespace('management', description='User Management')

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
                admin_users = [user for user in admin_users if admin_name.lower() in user.user_Name.lower()]

            if admin_users:
                admin_users_json = []

                for user in admin_users:
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
retrieve_student_parser.add_argument("blacklisted", help="Filter by blacklisted status")

# Define the API route for getting all student users
@api.route("/get_all_student")
@api.doc(description="Get all student users")
class GetAllAdmin(Resource):
    @api.expect(retrieve_student_parser)
    def get(self):
        args = retrieve_student_parser.parse_args()
        student_name = args.get("student_name", "")
        blacklisted = args.get("blacklisted", None)  # Change to None for better comparison

        try:
            students = User.query.filter_by(role_Name='student').all()

            if student_name:
                students = [user for user in students if student_name.lower() in user.user_Name.lower()]

            # Check if blacklisted is specified and is 'True' (case-insensitive)
            if blacklisted is not None:
                if blacklisted.lower() == 'true':
                    students = [user for user in students if Blacklist.query.filter_by(user_ID=user.user_ID).first() is not None]
                elif blacklisted.lower() == 'false':
                    students = [user for user in students if Blacklist.query.filter_by(user_ID=user.user_ID).first() is None]

            if students:
                student_list = []

                for user in students:
                    is_blacklisted = Blacklist.query.filter_by(user_ID=user.user_ID).first() is not None
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
retrieve_instructors_trainers.add_argument("instructor_name", help="Enter instructor name")
retrieve_instructors_trainers.add_argument("role_name", help="Enter role name")
retrieve_instructors_trainers.add_argument("organization_name", help="Enter organization")

@api.route("/get_all_instructors_and_trainers")
@api.doc(description="Get all instructors and trainers with organization names")
class GetAllInstructorsAndTrainers(Resource):
    @api.expect(retrieve_instructors_trainers)
    def get(self):
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
            keywords = ['rate', 'instructor']  # Define keywords to identify relevant questions
        
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

        user = User.query.filter_by(user_ID = user_id).first()

        user_name =  user.user_Name
        

        return jsonify({"code": 200, "data": user_name})


# Blacklist Student
retrieve_blacklist_student_id = api.parser()
retrieve_blacklist_student_id.add_argument("user_ids", type=int, action="append", required=True, help="Enter user ids as a list")

@api.route('/blacklist', methods=['POST'])
@api.doc(description="Blacklist Student")
class BlacklistStudent(Resource):
    @api.expect(retrieve_blacklist_student_id)
    def post(self):
        args = retrieve_blacklist_student_id.parse_args()
        user_ids = args["user_ids"]

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
            return jsonify({'code': 400, 'message': f'there are users who are already blacklisted'})

        # Create new blacklist entries for each user
        for user_id in user_ids:
            blacklist_entry = Blacklist(user_ID=user_id)
            db.session.add(blacklist_entry)

        db.session.commit()
        db.session.close()

        return jsonify({'code': 200, 'message': 'Users successfully blacklisted'})

retrieve_blacklist_remove = api.parser()
retrieve_blacklist_remove.add_argument("user_ids", type=int, action="append", required=True, help="Enter user IDs as a list")

@api.route('/remove_from_blacklist', methods=['POST'])
@api.doc(description="Remove Students from Blacklist")
class RemoveFromBlacklist(Resource):
    @api.expect(retrieve_blacklist_student_id)
    def post(self):
        args = retrieve_blacklist_student_id.parse_args()
        user_ids = args["user_ids"]

        # Check if any of the users are blacklisted
        blacklisted_users = Blacklist.query.filter(Blacklist.user_ID.in_(user_ids)).all()
        blacklisted_user_ids = [entry.user_ID for entry in blacklisted_users]

        if not blacklisted_user_ids:
            return jsonify({'code': 400, 'message': f'Users are not blacklisted'})

        # Remove blacklisted entries for each user
        for user_id in user_ids:
            Blacklist.query.filter_by(user_ID=user_id).delete()

        db.session.commit()

        return jsonify({'code': 200, 'message': 'Users successfully removed from blacklist'})