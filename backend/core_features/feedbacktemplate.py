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