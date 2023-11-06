from operator import or_
from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
from core_features import feedbacktemplate
import json

api = Namespace('feedback', description='Feedback related operations')

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


get_random_reviews_by_rcourse_id = api.parser()
get_random_reviews_by_rcourse_id.add_argument("rcourse_id", help="Enter rcourse id")
get_random_reviews_by_rcourse_id.add_argument("no_of_reviews", help="Enter No. of Review")
@api.route("/get_random_reviews_by_rcourse_id")
@api.doc(description="Get  Random Feedbacks by rcourse id")
class GetRandomReviewsByRCourseId(Resource):
    @api.expect(get_random_reviews_by_rcourse_id)
    def get(self):
      try:
        rcourse_id = get_random_reviews_by_rcourse_id.parse_args().get("rcourse_id")
        no_of_reviews = get_random_reviews_by_rcourse_id.parse_args().get("no_of_reviews")

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
                Feedback.rcourse_ID == rcourse_id,
                Feedback.template_Attribute_ID == template_attribute_id
              )
              .order_by(db.func.random())
              .limit(no_of_reviews)
              .all()
            )
          if random_reviews:
             return {"code": 200, "reviews":[review.json() for review in random_reviews]}, 200

        return {"code": 404, "message": "There are no reviews available currently"}, 404

      except Exception as e:
        return {"code": 404, "message": "Failed " + str(e)}, 404