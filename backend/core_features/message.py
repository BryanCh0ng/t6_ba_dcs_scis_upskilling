from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('message', description='Contact us page related operations')

# ==================== CONTACT US FUNCTIONS ====================#
# get_all_msg()
# create_new_msg()
# update_msg()

# create_new_msg()
create_msg_model = api.model("create_msg_model", {
    "user_ID" : fields.Integer(description="User ID", required=True),
    "msg_Subject" : fields.String(description="Message subject", required=True),
    "msg_Body" : fields.String(description="Message body", required=True),
    "msg_Datetime" : fields.DateTime(description="Message date & time", required=True)
})

@api.route("/create_new_msg", methods=["POST"])
@api.doc(description="Creates new message record")
class CreateNewMsg(Resource):
    @api.expect(create_msg_model)
    def post(self):
        data = request.get_json()
        msg = Message(**data)

        try:
            db.session.add(msg)
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": msg.json(),
                    "message": "Message record has been successfully created!"
                }
            )
        
        
        except Exception as e:
            return "Failed" + str(e), 500