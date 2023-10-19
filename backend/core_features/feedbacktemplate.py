from operator import or_
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from datetime import datetime, date, time
from allClasses import *
from sqlalchemy import asc
from core_features import common
import json

api = Namespace('feedbacktemplate', description='Feedback template related operations')

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
            return {"code": 404, "message": str(e)}, 404
    
@api.route("/post_feedback_template", methods=["POST"])
@api.doc(description="Post feedback template attribute")
class CreateFeedbackTemplate(Resource):
    def post(self):
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
              "feedback_start_date": common.format_date_time(runcourse.run_Startdate) #TO CHANGE TO FEEDBACK START DATE AFTERWARDS
            })

        if courses_no_template:
          for runcourse in courses_no_template:
            course_name_no_template.append({
              'run_Name': runcourse.run_Name,
              'rcourse_id': runcourse.rcourse_ID,
              "feedback_start_date": common.format_date_time(runcourse.run_Startdate) #TO CHANGE TO FEEDBACK START DATE AFTERWARDS
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
                      elif course_record.template_ID != template_id and course_record.run_Startdate > datetime.now().date(): #TO CHANGE TO FEEDBACK START DATE
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
