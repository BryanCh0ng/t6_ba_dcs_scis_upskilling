import unittest

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from allClasses import *

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(
            user_Name = "John",
            user_Email = "jonathan.2020@smu.edu.sg",
            user_Password = "john123",
            role_Name = "Student"
        )

    def tearDown(self):
        self.user = None

    def test_json(self):
        self.assertEqual(self.user.json(), {
                "user_ID": None,
                "user_Name": "John",
                "user_Email": "jonathan.2020@smu.edu.sg",
                "user_Password": "john123",
                "role_Name": "Student"
            }
        )


if __name__ == "__main__":
    unittest.main()
