from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc, func
from core_features import common
from core_features import feedbacktemplate
import json

api = Namespace('feedback', description='Feedback related operations')

post_feedback_student = api.parser()
@api.route("/post_feedback_student" ,methods=["POST", "GET"])
@api.doc(description="Submit Student Feedback")
class GetTemplate(Resource):
    @api.expect(post_feedback_student)
    def post(self):
        new_student_feedback = request.json
        courseID = new_student_feedback.get("rcourse_id")
        templateID = new_student_feedback.get("template_id")
        userID = new_student_feedback.get("user_id")
        data = new_student_feedback.get("data")
        common_questions_data = new_student_feedback.get("common_questions_data")

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
                
                db.session.rollback()
                return False
       
        template = Feedback.query.filter(Feedback.feedback_Template_ID==templateID,Feedback.submitted_By == userID, Feedback.rcourse_ID == courseID ).first()

        if not template:
            try:
                for eachdata in data:
                   AttributeID = eachdata.get("attribute_id")
                   answer = eachdata.get("answer")
                   NewFeedback =Feedback( None, templateID, userID, AttributeID, answer, courseID)
                   db.session.add(NewFeedback)
                   db.session.commit()
                   db.session.close()

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
                db.session.close()
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
        
        return {"code": 404, "message": "Failed" + str(e)}, 404


get_random_reviews_by_rcourse_id = api.parser()
get_random_reviews_by_rcourse_id.add_argument("rcourse_id", help="Enter rcourse id")
get_random_reviews_by_rcourse_id.add_argument("course_id", help="Enter course id")
get_random_reviews_by_rcourse_id.add_argument("no_of_reviews", help="Enter No. of Review")
@api.route("/get_random_reviews_by_rcourse_id")
@api.doc(description="Get  Random Feedbacks by rcourse id")
class GetRandomReviewsByRCourseId(Resource):
    @api.expect(get_random_reviews_by_rcourse_id)
    def get(self):
      try:
        rcourse_id = get_random_reviews_by_rcourse_id.parse_args().get("rcourse_id")
        course_id = get_random_reviews_by_rcourse_id.parse_args().get("course_id")
        no_of_reviews = get_random_reviews_by_rcourse_id.parse_args().get("no_of_reviews")

        if rcourse_id:
          template_attribute_query = db.session.query(
            TemplateAttribute,
          ).filter(
            TemplateAttribute.question == 'Any Feedbacks for the course',
            TemplateAttribute.template_ID == None,
            TemplateAttribute.input_Type == 'Text Field'
          ).first()
          
          
          if template_attribute_query:
            random_reviews = (
                db.session.query(
                  Feedback,
                ).filter(
                  Feedback.rcourse_ID == rcourse_id,
                  Feedback.template_Attribute_ID == template_attribute_query.template_Attribute_ID,
                  Feedback.answer != ""
                )
                .order_by(db.func.random())
                .limit(no_of_reviews)
                .all()
              )
            
            if random_reviews:
              
              db.session.close()
              return {"code": 200, "reviews":[review.json() for review in random_reviews]}, 200
            return {"code": 202, "message": "There are no reviews available currently"}, 202

        if course_id:
          rcourse_ids = db.session.query(RunCourse.rcourse_ID).filter(RunCourse.course_ID == course_id).all()
          rcourse_id_list = [result[0] for result in rcourse_ids]
         

          if rcourse_id_list:
            template_attribute_query = db.session.query(
              TemplateAttribute,
            ).filter(
              TemplateAttribute.question == 'Any Feedbacks for the course',
              TemplateAttribute.template_ID == None,
              TemplateAttribute.input_Type == 'Text Field'
            ).first()
            
            if template_attribute_query:
              template_attribute_id = template_attribute_query.template_Attribute_ID
              random_reviews = (
                  db.session.query(
                    Feedback,
                  ).filter(
                    Feedback.rcourse_ID.in_(rcourse_id_list),
                    Feedback.template_Attribute_ID == template_attribute_id,
                    Feedback.answer != ""
                  )
                  .order_by(db.func.random())
                  .limit(no_of_reviews)
                  .all()
                )
              
              if random_reviews:
                db.session.close()
                return {"code": 200, "reviews":[review.json() for review in random_reviews]}, 200

          return {"code": 202, "message": "There are no feedbacks available currently"}, 202

      except Exception as e:
       
        return {"code": 404, "message": "Failed " + str(e)}, 404
      
# For specific run course 
retrieve_runcourse_id = api.parser()
retrieve_runcourse_id.add_argument("course_ID", help="Enter course_ID")
retrieve_runcourse_id.add_argument("runcourse_ID", help="Enter runcourse_ID")

@api.route("/get_feedback_for_runcourse")
@api.doc(description="Runcourse feedback")
class RunCourseFeedback(Resource):
    @api.expect(retrieve_runcourse_id)
    def get(self):
        try:
            args = retrieve_runcourse_id.parse_args()
            course_ID = args.get("course_ID", "")
            runcourse_ID = args.get("runcourse_ID", "")
            
            feedback_dict = {}
            unique_questions = {}

            if course_ID:
                # Check if the course exists
                course = Course.query.get(course_ID)
                if course is None:
                    return jsonify({'message': 'Course not found.', 'code': 404})
                
                # Retrieve the associated course's name
                course_name = course.course_Name
                
                # Query feedback for run courses associated with the course
                run_courses = RunCourse.query.filter_by(course_ID=course_ID).all()
                feedback = Feedback.query.filter(Feedback.rcourse_ID.in_([run_course.rcourse_ID for run_course in run_courses])).all()

            elif runcourse_ID:
                # Check if the run course exists
                runcourse = RunCourse.query.get(runcourse_ID)
                if runcourse is None:
                    return jsonify({'message': 'Run course not found.', 'code': 404})

                # Retrieve the associated run course's name
                run_name = runcourse.run_Name
                
                # Query feedback for the specified run course
                feedback = Feedback.query.filter_by(rcourse_ID=runcourse_ID).all()

            else:
                return jsonify({'message': 'No course or run course ID provided.', 'code': 400})

            if feedback:
                for entry in feedback:
                    submitted_by = entry.submitted_By
                    answers = entry.answer
                    template_attribute_id = entry.template_Attribute_ID

                    # Retrieve the associated question for this feedback entry
                    question = TemplateAttribute.query.get(template_attribute_id).question

                    # Collect the question in the dictionary of unique questions
                    unique_questions[template_attribute_id] = question

                    if submitted_by not in feedback_dict:
                        if course_ID:
                            feedback_dict[submitted_by] = {
                                'submitted_By': submitted_by,
                                'answers': [],
                                'course_name': course_name
                            }
                        elif runcourse_ID:
                            feedback_dict[submitted_by] = {
                                'submitted_By': submitted_by,
                                'runcourse_ID': runcourse_ID,
                                'run_name': run_name,
                                'answers': [],
                            }

                    feedback_dict[submitted_by]['answers'].append(answers)

                # Convert the dictionary of unique questions to a list of dictionaries
                unique_questions_list = [{"template_attribute_id": k, "question": v} for k, v in unique_questions.items()]

                # Convert the dictionary values to a list
                feedback_list = list(feedback_dict.values())

                db.session.close()

                return jsonify({'data': feedback_list, 'questions': unique_questions_list, 'code': 200})

            else:
                return jsonify({'message': 'No feedback found for this course or run course.', 'code': 404})
              
        except Exception as e:
            return jsonify({"message": "Failed " + str(e), "code": 500})

# For specific course and instructor 
retrieve_course_instructor = api.parser()
retrieve_course_instructor.add_argument("course_ID", help="Enter course ID")
retrieve_course_instructor.add_argument("instructor_ID", help="Enter instructor ID")

@api.route("/get_feedback_for_course_and_instructor")
@api.doc(description="course feedback")
class RunCourseFeedback(Resource):
    @api.expect(retrieve_course_instructor)
    def get(self):
        try:
            args = retrieve_course_instructor.parse_args()
            course_ID = args.get("course_ID", "")
            instructor_ID = args.get("instructor_ID", "")

            feedback_dict = {}
            questions = []  # Use a list to store unique questions as dictionaries

            query = (
                db.session.query(
                    RunCourse.course_ID,
                    Feedback.submitted_By,
                    Feedback.template_Attribute_ID,  # Include the template attribute ID
                    func.group_concat(Feedback.answer).label("answers"),
                    TemplateAttribute.template_Attribute_ID,  # Include the template attribute ID
                    TemplateAttribute.question,
                )
                .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
            )

            if course_ID:
                query = query.filter(RunCourse.course_ID == course_ID)

            if instructor_ID:
                query = query.filter(RunCourse.instructor_ID == instructor_ID)

            # Group feedback by "submitted_by", "template_attribute_id," and "rcourse_ID," and aggregate answers into an array
            feedback = (
                query
                .group_by(Feedback.submitted_By, Feedback.template_Attribute_ID, Feedback.rcourse_ID)
                .all()
            )

            if feedback:
                instructor_name = None  # Initialize the instructor name

                # Get the instructor's name from the User table
                instructor = User.query.get(instructor_ID)
                if instructor:
                    instructor_name = instructor.user_Name

                for entry in feedback:
                    course_id = entry.course_ID
                    submitted_by = entry.submitted_By
                    answers = entry.answers
                    template_attribute_id = entry.template_Attribute_ID  # Retrieve the template attribute ID
                    question = entry.question

                    # Create a unique key for the dictionary using course_ID and submitted_By
                    key = (course_id, submitted_by)

                    if key not in feedback_dict:
                        # Retrieve the associated course's name by querying the Course table
                        course = Course.query.get(course_id)
                        course_name = course.course_Name if course else None

                        feedback_dict[key] = {
                            'course_ID': course_id,
                            'course_Name': course_name,
                            'submitted_By': submitted_by,
                            'instructor_Name': instructor_name,
                            'answers': [],
                        }

                    feedback_dict[key]['answers'].append(answers)

                    # Check if the question already exists in the list
                    question_found = next((q for q in questions if q["template_attribute_id"] == template_attribute_id), None)

                    if not question_found:
                        # If the question doesn't exist, add it to the list
                        questions.append({
                            "template_attribute_id": template_attribute_id,
                            "question": question,
                        })

                # Convert the dictionary values to a list
                feedback_list = list(feedback_dict.values())

                db.session.close()

                return jsonify({'data': feedback_list, 'questions': questions, 'code': 200})

            else:
                return jsonify({'message': 'No feedback found for this course and instructor.', 'code': 404})
        except Exception as e:
            return jsonify({"message": "Failed " + str(e), "code": 500})

#Get all feedback 
get_feedback = api.parser()

get_feedback.add_argument("course_ID", help="Enter course ID")
get_feedback.add_argument("coursecat_ID", help="Enter course category ID")
get_feedback.add_argument("rcourse_ID", help="Enter run course ID")
get_feedback.add_argument("instructor_ID", help="Enter instructor ID")
get_feedback.add_argument("run_Startdate", help="Enter run start date")
get_feedback.add_argument("run_Enddate", help="Enter run end date")

@api.route("/get_feedback")
@api.doc(description="Get feedback")
class GetFeedback(Resource):
    @api.expect(get_feedback)
    def get(self):
        try: 
            # Parse the course_ID from the request arguments
            args = get_feedback.parse_args()
            courseID = args.get("course_ID", "")
            coursecatID = args.get("coursecat_ID", "")
            rcourseID = args.get("rcourse_ID", "")
            instructorID = args.get("instructor_ID", "")
            start_date = args.get('run_Startdate', "")
            end_date = args.get("run_Enddate", "")

            formatted_start_date = None
            formatted_end_date = None

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute, CourseCategory, User)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  
                .join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)  
                .join(User, RunCourse.instructor_ID == User.user_ID)
                .filter(or_(func.lower(TemplateAttribute.question).like("%instructor%"), func.lower(TemplateAttribute.question).like("%course%")))
                .filter(or_(TemplateAttribute.input_Type == "Text Field", TemplateAttribute.input_Type == "Likert Scale"))
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
                        
            if filtered_results:
                # Define the header variable (an array of selected fields including coursecat_Name)
                header = ["Course Name", "Course Category", "Run Name", "Run Start Date", "Run End Date", "Instructor Name", "Question", "Answer"]

                # Create a 2D array containing data for selected fields from filtered_results
                answers = []
                for result in filtered_results:
                    # Format startdate and enddate to dd/mm/yyyy
                    start_date_formatted = result.RunCourse.run_Startdate.strftime('%d/%m/%Y')
                    end_date_formatted = result.RunCourse.run_Enddate.strftime('%d/%m/%Y')

                    answer_row = [
                        result.Course.course_Name,
                        result.CourseCategory.coursecat_Name,
                        result.RunCourse.run_Name,
                        start_date_formatted,
                        end_date_formatted,
                        result.User.user_Name,
                        result.TemplateAttribute.question,
                        result.Feedback.answer
                    ]
                    answers.append(answer_row)

                return jsonify(
                    {
                        "code": 200,
                        "header": header,
                        "answers": answers
                    }
                )

            return jsonify(
                {
                    "code": 400,
                    "message": "No course feedbacks found"
                }
            )

        except Exception as e:
            
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retrieve course feedbacks: " + str(e)
                }
            )
