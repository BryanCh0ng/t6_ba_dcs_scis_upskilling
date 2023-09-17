from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
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
        template = FeedbackTemplate.query.filter_by(template_ID=templateID).first()
        db.session.close()
        if template:
            return json.loads(json.dumps(template.json())), 200

        return json.loads(json.dumps({"message": "There is no such template"})), 404
    
post_feedback_student = api.parser()
post_feedback_student.add_argument("input_type", help="Enter student input")
post_feedback_student.add_argument("question", help="Enter question")
post_feedback_student.add_argument("template_ID", help="Enter template id")
@api.route("/post_feedback_student")
@api.doc(description="Post feedback template attribute")
class GetTemplate(Resource):
    @api.expect(post_feedback_student)
    def get(self):
        try:
            templateID = get_template_by_id.parse_args().get("template_ID")
            inputType = get_template_by_id.parse_args().get("input_type")
            question = get_template_by_id.parse_args().get("question")
            # TemplateAttributeList = TemplateAttribute.query.filter(TemplateAttribute.template_Attribute_ID.contains("")).all()
            # finalAttribute = TemplateAttributeList[-1]
            # templateAttributeID = finalAttribute.template_Attribute_ID
            newTemplateAttribute = TemplateAttribute(None,question, inputType,templateID)
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
@api.route("/post_feedback_student_feedback_template")
@api.doc(description="Search if template id exists, if does get template, else create new template")
class GetTemplate(Resource):
    @api.expect(post_feedback_student_feedback_template)
    def get(self):

        templateName = get_template_by_id.parse_args().get("template_Name")
        templateID = get_template_by_id.parse_args().get("template_ID")
        current_date = datetime.date.today()

        template = FeedbackTemplate.query.filter_by(template_ID=templateID).first()

        if not template:
            NewFeedbackTemplate = FeedbackTemplate(templateID, templateName, current_date)
            try:
                db.session.add(NewFeedbackTemplate)
                return json.loads(json.dumps(NewFeedbackTemplate.json())), 200
           
            except Exception as e:
                return json.loads(json.dumps({"message": "Failed" + str(e)})), 500
        else:
            return json.loads(json.dumps(template.json())), 200

get_all_template_attributes_by_feedback_template_id = api.parser()
            

