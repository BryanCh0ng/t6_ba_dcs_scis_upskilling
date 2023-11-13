import unittest
from unittest.mock import patch
from flask import Flask, json

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from core_features.course import *

class TestCourse(unittest.TestCase):
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_addition(self):
        with self.app.test_request_context(json={"first": 5, "second": 10}):
            # Act
            response = Addition().post()

            # Assert
            self.assertEqual(response, 15)
    
    def test_get_all_courses_filter_search(self):
        # Arrange
        with self.app.test_request_context("/retrieve_all_courses_filter_search"):
            # Act
            response = GetAllCoursesFilterSearch().get()

            # Assert
            self.assertEqual(response.status_code, 200)
            # Add more assertions based on the expected behavior of your endpoint


if __name__ == '__main__':
    unittest.main()