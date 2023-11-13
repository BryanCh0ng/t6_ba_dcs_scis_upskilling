import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from werkzeug.test import EnvironBuilder

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from core_features.course import *

class TestCreateCourseEndpoint(unittest.TestCase):
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    def _create_request(self, json_data):
        # Helper method to create a Flask request context
        builder = EnvironBuilder(method='POST', data=json.dumps(json_data))
        return self.app.request_context(builder.get_environ())

    @patch('core_features.course.db.session.commit')
    @patch('core_features.course.jsonify')
    @patch('core_features.course.Course.query', autospec=True)  # Ensure that Course.query is treated as a real object
    def test_create_course_success(self, mock_query, mock_jsonify, mock_commit):
        # Arrange
        with self._create_request({"course_Name": "Test Course", "course_Desc": "Description", "coursecat_ID": 1}):
            mock_query.return_value.filter.return_value.first.return_value = None
            mock_commit.return_value = None

            # Act
            response = CreateCourse().post()

        # Assert
        mock_query.assert_called_once()  # Ensure that Course.query is accessed
        mock_query.return_value.filter.assert_called_once()
        mock_commit.assert_called_once()
        mock_jsonify.assert_called_once()

        # Add more assertions based on the expected behavior of your endpoint
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Course created successfully', response.data)

    @patch('core_features.course.Course.query', autospec=True)  # Ensure that Course.query is treated as a real object
    def test_create_course_failure_existing_course(self, mock_query):
        # Arrange
        with self._create_request({"course_Name": "Existing Course", "course_Desc": "Description", "coursecat_ID": 1}):
            existing_course = MagicMock()
            mock_query.return_value.filter.return_value.first.return_value = existing_course

            # Act
            response = CreateCourse().post()

        # Assert
        mock_query.assert_called_once()  # Ensure that Course.query is accessed
        mock_query.return_value.filter.assert_called_once()
        existing_course.json.assert_called_once()

        # Add more assertions based on the expected behavior of your endpoint
        self.assertEqual(response.status_code, 409)
        self.assertIn(b'Course name already exists', response.data)

if __name__ == '__main__':
    unittest.main()