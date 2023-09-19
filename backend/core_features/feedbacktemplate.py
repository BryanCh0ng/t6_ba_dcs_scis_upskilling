from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
import datetime
from allClasses import *
from sqlalchemy import asc
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
      db.session.close()
      
      if templates:
        templates_json = [template.json() for template in templates]
        return {"code": 200, "data": {"templates": templates_json}}, 200

      return {"code": 404, "message": "No templates found"}, 404

get_template_by_id = api.parser()
get_template_by_id.add_argument("template_id", help="Enter template id")
@api.route("/get_template_by_id")
@api.doc(description="Get template by tempate id")
class GetTemplate(Resource):
    @api.expect(get_template_by_id)
    def get(self):
        templateID = get_template_by_id.parse_args().get("template_id")
        query = db.session.query(
            FeedbackTemplate,
            TemplateAttribute,
            LikertScale,
        ).select_from(FeedbackTemplate).join(
            TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID
        ).join(
            LikertScale, TemplateAttribute.template_Attribute_ID == LikertScale.template_Attribute_ID
        ).filter(
            FeedbackTemplate.template_ID == templateID
        ).order_by(
            asc(LikertScale.position)
        )
        template_query = query.all()
        db.session.close()
        if template_query:
          template_data = {
              'feedback_template_name': None,
              'template_id': None,
              'created_on': None,
              'data': []
          }
          question_dict = {}
          for template, attribute, likert_scale in template_query:
            if attribute.template_Attribute_ID not in template_data:
              if template_data['feedback_template_name'] is None:
                template_data['feedback_template_name'] = template.template_Name
                template_data['template_id'] = template.template_ID
                template_data['created_on'] = format_date_time(template.created_On)

              if attribute.question in question_dict:
                question_dict[attribute.question]['inputOptions'].append({
                    'id': likert_scale.likert_Scale_ID,
                    'position': likert_scale.position,
                    'option': likert_scale.textlabel
                })
              else:
                question_data = {
                  'question': attribute.question,
                  'selectedInputType': attribute.input_Type,
                  'inputOptions': [{
                      'id': likert_scale.likert_Scale_ID,
                      'position': likert_scale.position,
                      'option': likert_scale.textlabel
                  }],
                }
                question_dict[attribute.question] = question_data


          template_data['data'] = list(question_dict.values())
          return {"code": 200, "data": {"templates": template_data}}, 200

        return {"code": 404, "message": "There is no such template"}, 404
    


post_feedback_student = api.parser()
post_feedback_student.add_argument("input_type", help="Enter student input")
post_feedback_student.add_argument("question", help="Enter question")
post_feedback_student.add_argument("template_ID", help="Enter template id")
@api.route("/post_feedback_student", methods=["POST","GET"])
@api.doc(description="Post feedback template attribute")
class GetTemplate(Resource):
    @api.expect(post_feedback_student)
    def get(self):

        args = post_feedback_student.parse_args()
        templateID = args.get("template_ID")
        inputType = args.get("input_type")
        question = args.get("question")
        try:
            
            # TemplateAttributeList = TemplateAttribute.query.filter(TemplateAttribute.template_Attribute_ID.contains("")).all()
            # finalAttribute = TemplateAttributeList[-1]
            # templateAttributeID = finalAttribute.template_Attribute_ID + 1
            newTemplateAttribute = TemplateAttribute( None  ,question, inputType,templateID)
            db.session.add(newTemplateAttribute)

            # Commit the changes to the database
            db.session.commit()

            # Return the newly created course as JSON response
            return json.loads(json.dumps(newTemplateAttribute.json(), default=str)), 201
        
        
        except Exception as e:
            print("Error:", str(e))
            return "Failed to create a new feedback attribute: " + str(e), 500
        

    
post_feedback_student_feedback_template = api.parser()
post_feedback_student_feedback_template.add_argument("template_Name", help="Enter template name")
post_feedback_student_feedback_template.add_argument("template_ID", help="Enter template id")
@api.route("/post_feedback_student_feedback_template" ,methods=["POST", "GET"])
@api.doc(description="Search if template id exists, if does get template, else create new template")
class GetTemplate(Resource):
    @api.expect(post_feedback_student_feedback_template)
    def get(self):

        templateName = post_feedback_student_feedback_template.parse_args().get("template_Name")
        templateID = post_feedback_student_feedback_template.parse_args().get("template_ID")
        current_date = datetime.now().strftime('%d-%m-%Y')


        template = FeedbackTemplate.query.filter_by(template_ID=templateID).first()

        if not template:
            NewFeedbackTemplate = FeedbackTemplate(templateID, templateName, current_date)
            try:
                db.session.add(NewFeedbackTemplate)
                return json.loads(json.dumps(NewFeedbackTemplate.json())), 200
           
            except Exception as e:
                return json.loads(json.dumps({"message": "Failed" + str(e)})), 500
        else:
            return {"message": "Template ID already exists"}, 409


def format_date_time(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, time):
        return value.strftime('%H:%M:%S')
    else:
        return None