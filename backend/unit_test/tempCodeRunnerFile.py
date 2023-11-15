    # def test_get_template_pass(self):
    #     request_body = {
    #     "rcourse_id": 1,  # Assuming the rcourse_id value is 1 for all feedback entries
    #     "template_id": 1,  # Assuming the template_id value is 1 for all feedback entries
    #     "user_id": 2,  # Assuming the user_id value is 1 for all feedback entries
    #     "common_questions_data": [
    #         {"attribute_id": 4, "answer": "Self-introspection of the concepts taught in class"},
    #         {"attribute_id": 5, "answer": "Slower pace in class"},
    #         {"attribute_id": 6, "answer": "5"}
    # ]
    # }   
    #     json_request_body = json.dumps(request_body)
    #     with self.app.test_request_context(data=json_request_body, content_type='application/json'): 
    #         response = GetTemplate().post()
    #         print (response)
    #         self.assertEqual(response[1], 200)