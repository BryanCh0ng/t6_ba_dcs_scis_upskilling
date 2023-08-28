from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('feedbacktemplate', description='Feedback template related operations')

# ==================== USER FUNCTIONS ====================#
# get_templates()

get_templates = api.parser()
@api.route("/get_templates")
@api.doc(description="Get all feedback templates")
class GetTemplates(Resource):
    @api.expect(get_templates)
    def get(self):
        templates = FeedbackTemplate.query.all()
        db.session.close()
        
        if templates:
            templates_json = [template.json() for template in templates]
            return {"code": 200, "data": {"templates": templates_json}}, 200

        return {"code": 404, "message": "No templates found"}, 404